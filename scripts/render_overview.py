#!/usr/bin/env python3
"""概览卡渲染：把收藏统计与分布画成一张自包含 SVG。

为什么自己画而不是用现成方案：
  - 分布类信息（各分类的相对占比）徽章服务表达不了，需要真正的条形图。
  - 自绘 SVG 是矢量、无外部依赖、无网络请求，样式完全可控，能同时产出
    浅色与深色两版，适配 GitHub 的 prefers-color-scheme 切换。
  - 所有文本（含中文）都以文本节点写入，由客户端渲染，不依赖服务端字体。

版式：单张卡片，自上而下三段，用一条细分隔线切开
  1. 指标行 —— 收录总数 / 分类数 / 自研数 / 私有数，大号数字 + 小号标签
  2. 分类分布 —— 横向条形，长度按最大项归一化（不是按总量，这样类别之间
     的相对关系更直观）
  3. 语言分布 —— 胶囊标签流式排布。语言名短、种类多，用条形图要占十几行，
     换成胶囊后同样信息只占两行，且视觉重量明显低于上面的主图，
     信息层级自然拉开。

设计上是刻意克制的：单一强调色（不用渐变）、无阴影、无装饰线，
所有对比靠字号、字重和灰度层级建立。

隐私边界：本模块只接收「标签 + 计数」二元组。标签来自 taxonomy.json 的
分类标题、编程语言名与调用方传入的固定文案，不含任何与单个仓库相关的
信息。SVG 中不会出现单个私有仓库的名称、描述或链接。

仅依赖 Python 标准库。
"""

from __future__ import annotations

from pathlib import Path

# --- 栅格常量 --------------------------------------------------------------
# 宽度取 880：GitHub README 正文在宽屏下的容器宽度约 830～900px，这个值
# 既能填满容器又几乎不会被放大模糊（SVG 缩放不失真，但字号比例会变）。
WIDTH = 880
PAD = 32
CONTENT_W = WIDTH - PAD * 2

# 指标行
KPI_NUM_SIZE = 23
KPI_LABEL_SIZE = 11.5
KPI_NUM_DROP = 23            # 块顶 -> 数字基线
KPI_NUM_TO_LABEL = 20        # 数字基线 -> 标签基线
KPI_TO_DIVIDER = 26          # 标签基线 -> 分隔线
DIVIDER_TO_SECTION = 28      # 分隔线 -> 下一段标题基线

# 段落标题
TITLE_SIZE = 14
TITLE_DROP = 11              # 段顶 -> 标题基线
TITLE_TO_ROWS = 18           # 标题基线 -> 首个条形行中心

# 条形行
# 标签右对齐紧贴条形起点，而不是左对齐。分类名长度差异很大（「编程学习与
# 计算机基础」11 字 vs「其他」2 字），左对齐时短标签后面会空出一大段，
# 看起来像排版没对齐。右对齐是水平条形图的标准做法：标签列右边缘与条形
# 起点形成一条明确的分界线，视线从标签到条形不用跨越空白。
LABEL_SIZE = 13
LABEL_W = 240                # 13px 下最长分类名约 221px，留有余量
BAR_GAP = 14                 # 标签列与条形之间的空隙
BAR_H = 6                    # 细条形比粗条形更接近「数据条」而不是「进度条」
ROW_H = 25
VALUE_W = 46                 # 右侧数字所占宽度（右对齐）
SECTION_GAP = 26             # 上一段末尾 -> 下一段顶

# 胶囊标签
CHIP_H = 26
CHIP_FONT = 12
CHIP_PAD = 11
CHIP_NUM_GAP = 9
CHIP_GAP_X = 8
CHIP_GAP_Y = 8

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', "
        "'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif")

THEMES = {
    "light": {
        "bg": "#FFFFFF",
        "border": "#E4E9F0",
        "divider": "#EEF1F6",
        "accent": "#4F46E5",
        "kpi_num": "#0F172A",
        "kpi_label": "#94A3B8",
        "title": "#0F172A",
        "label": "#475569",
        "value": "#0F172A",
        "chip_bg": "#F4F6FA",
        "chip_border": "",
        "chip_text": "#566174",
        "chip_num": "#0F172A",
    },
    "dark": {
        "bg": "#0D1117",
        "border": "#30363D",
        "divider": "#21262D",
        "accent": "#818CF8",
        "kpi_num": "#E6EDF3",
        "kpi_label": "#7D8590",
        "title": "#E6EDF3",
        "label": "#A9B2BD",
        "value": "#E6EDF3",
        "chip_bg": "#161B22",
        "chip_border": "#30363D",
        "chip_text": "#A9B2BD",
        "chip_num": "#E6EDF3",
    },
}


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def _text_width(s: str, size: float) -> float:
    """粗略估算文本像素宽度。

    SVG 无法在生成阶段测量真实字宽，用 em 系数近似：中日韩字符与全角标点按
    1.0em，ASCII 约 0.56em，空格 0.30em。只用于排布胶囊与判断是否截断，
    不参与条形定位，因此少量误差不会影响版式。
    """
    w = 0.0
    for ch in s:
        o = ord(ch)
        if o >= 0x2E80 or o in (0x2014, 0x2018, 0x2019, 0x201C, 0x201D, 0x2026):
            w += 1.0
        elif ch == " ":
            w += 0.30
        else:
            w += 0.56
    return w * size


def _fit(s: str, size: float, max_w: float) -> str:
    """超宽时截断并加省略号，保证标签不会压到条形上。"""
    if _text_width(s, size) <= max_w:
        return s
    ell = "…"
    budget = max_w - _text_width(ell, size)
    out = ""
    for ch in s:
        if _text_width(out + ch, size) > budget:
            break
        out += ch
    return out.rstrip() + ell


def _t(x: float, y: float, s: str, size: float, fill: str,
       weight: str = "", anchor: str = "") -> str:
    extra = ""
    if weight:
        extra += f' font-weight="{weight}"'
    if anchor:
        extra += f' text-anchor="{anchor}"'
    return (f'<text x="{x:.1f}" y="{y:.1f}" font-family="{FONT}" '
            f'font-size="{size}" fill="{fill}"{extra}>{_esc(str(s))}</text>')


def _chip_width(label: str, count: int) -> float:
    num = str(count)
    # 数字用 600 字重，比常规体略宽，系数从 0.56 上调到 0.62
    return (CHIP_PAD * 2 + _text_width(label, CHIP_FONT)
            + CHIP_NUM_GAP + len(num) * CHIP_FONT * 0.62)


def _chip_layout(items: list[tuple[str, int]], max_w: float) -> list[list[tuple]]:
    """把 (标签, 计数) 排成多行胶囊，返回 [[(label, count, width), ...], ...]。"""
    rows: list[list[tuple]] = []
    cur: list[tuple] = []
    cur_w = 0.0
    for label, n in items:
        w = _chip_width(label, n)
        if cur and cur_w + CHIP_GAP_X + w > max_w:
            rows.append(cur)
            cur, cur_w = [], 0.0
        if cur:
            cur_w += CHIP_GAP_X
        cur.append((label, n, w))
        cur_w += w
    if cur:
        rows.append(cur)
    return rows


def render_overview_svg(payload: dict, theme: str = "light") -> str:
    """生成概览 SVG。

    payload:
      kpis       [(值, 标签), ...]       例如 [("65", "已收录仓库"), ...]
      categories [(标签, 计数), ...]     需调用方预先按计数降序排好
      languages  [(标签, 计数), ...]     同上
    """
    c = THEMES.get(theme, THEMES["light"])
    kpis = list(payload.get("kpis") or [])
    cats = list(payload.get("categories") or [])
    langs = list(payload.get("languages") or [])
    chip_rows = _chip_layout(langs, CONTENT_W) if langs else []

    # --- 高度预算：自上而下走一遍光标，再据此声明画布尺寸 ---
    cursor = PAD
    kpi_num_baseline = kpi_label_baseline = divider_y = 0.0
    if kpis:
        kpi_num_baseline = cursor + KPI_NUM_DROP
        kpi_label_baseline = kpi_num_baseline + KPI_NUM_TO_LABEL
        divider_y = kpi_label_baseline + KPI_TO_DIVIDER
        cursor = divider_y + DIVIDER_TO_SECTION

    cat_title_baseline = cat_first_center = 0.0
    if cats:
        cat_title_baseline = cursor + TITLE_DROP
        cat_first_center = cat_title_baseline + TITLE_TO_ROWS
        cursor = cat_first_center + (len(cats) - 1) * ROW_H + BAR_H / 2

    lang_title_baseline = chips_top = 0.0
    if chip_rows:
        cursor += SECTION_GAP
        lang_title_baseline = cursor + TITLE_DROP
        chips_top = lang_title_baseline + 17
        cursor = (chips_top + len(chip_rows) * CHIP_H
                  + (len(chip_rows) - 1) * CHIP_GAP_Y)

    height = int(round(cursor + PAD))

    out: list[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" '
        f'aria-label="{_esc("收藏概览：指标、分类分布与语言分布")}">'
    )
    out.append(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="14" '
        f'fill="{c["bg"]}" stroke="{c["border"]}"/>'
    )

    # --- 1. 指标行 ---
    if kpis:
        col_w = CONTENT_W / len(kpis)
        for i, (value, label) in enumerate(kpis):
            x = PAD + i * col_w
            out.append(_t(x, kpi_num_baseline, value, KPI_NUM_SIZE,
                          c["kpi_num"], weight="600"))
            out.append(_t(x, kpi_label_baseline, label, KPI_LABEL_SIZE,
                          c["kpi_label"]))
        out.append(
            f'<line x1="{PAD}" y1="{divider_y:.1f}" x2="{WIDTH - PAD}" '
            f'y2="{divider_y:.1f}" stroke="{c["divider"]}"/>'
        )

    # --- 2. 分类分布 ---
    if cats:
        peak = max(n for _, n in cats) or 1
        bar_x = PAD + LABEL_W + BAR_GAP
        bar_max = WIDTH - PAD - VALUE_W - bar_x
        out.append(_t(PAD, cat_title_baseline, "分类分布", TITLE_SIZE,
                      c["title"], weight="600"))
        for i, (label, n) in enumerate(cats):
            cy = cat_first_center + i * ROW_H
            w = max(BAR_H, bar_max * n / peak)
            out.append(_t(PAD + LABEL_W, cy + 4.5,
                          _fit(label, LABEL_SIZE, LABEL_W),
                          LABEL_SIZE, c["label"], anchor="end"))
            out.append(
                f'<rect x="{bar_x:.1f}" y="{cy - BAR_H / 2:.1f}" '
                f'width="{w:.1f}" height="{BAR_H}" rx="{min(BAR_H / 2, w / 2):.1f}" '
                f'fill="{c["accent"]}"/>'
            )
            out.append(_t(WIDTH - PAD, cy + 4.5, n, LABEL_SIZE,
                          c["value"], weight="600", anchor="end"))

    # --- 3. 语言分布 ---
    if chip_rows:
        out.append(_t(PAD, lang_title_baseline, "语言分布", TITLE_SIZE,
                      c["title"], weight="600"))
        stroke = (f' stroke="{c["chip_border"]}"' if c["chip_border"] else "")
        for ri, row in enumerate(chip_rows):
            x = PAD
            y = chips_top + ri * (CHIP_H + CHIP_GAP_Y)
            for label, n, w in row:
                out.append(
                    f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" '
                    f'height="{CHIP_H}" rx="{CHIP_H / 2}" '
                    f'fill="{c["chip_bg"]}"{stroke}/>'
                )
                base = y + CHIP_H / 2 + 4.3
                out.append(_t(x + CHIP_PAD, base, label, CHIP_FONT, c["chip_text"]))
                out.append(_t(x + w - CHIP_PAD, base, n, CHIP_FONT,
                              c["chip_num"], weight="600", anchor="end"))
                x += w + CHIP_GAP_X

    out.append("</svg>")
    return "\n".join(out)


def write_overview_assets(assets_dir: Path, payload: dict) -> list[Path]:
    """写出浅色 / 深色两版 SVG，返回文件路径列表。"""
    assets_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for theme in ("light", "dark"):
        path = assets_dir / f"overview-{theme}.svg"
        path.write_text(render_overview_svg(payload, theme), encoding="utf-8")
        written.append(path)
    return written
