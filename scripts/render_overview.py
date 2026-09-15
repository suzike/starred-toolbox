#!/usr/bin/env python3
"""概览图渲染：把分类/语言分布画成自包含 SVG。

为什么自己画而不是用第三方徽章服务：
  - 分布类信息（11 个分类的相对占比）徽章服务表达不了，需要真正的条形图。
  - 自绘 SVG 是矢量、无外部依赖、无网络请求，样式完全可控，能同时产出
    浅色与深色两版，适配 GitHub 的 prefers-color-scheme 切换。
  - 所有文本（含中文）都以文本节点写入，由客户端渲染，不依赖服务端字体。

隐私边界：本模块只接收「标签 + 计数」二元组，调用方传入的标签一律来自
taxonomy.json 的分类标题或编程语言名，不含任何仓库内容。SVG 中不会出现
单个私有仓库的名称、描述或链接。

仅依赖 Python 标准库。
"""

from __future__ import annotations

from pathlib import Path

# 画布几何。数值经过测算：标签列 268px 可容纳最长分类标题
# 「MATLAB / Simulink 与基于模型的设计」（约 221px @13px），留有余量。
WIDTH = 880
PAD = 28
HEADER_H = 46
ROW_H = 26
BAR_H = 13
SECTION_GAP = 34
LABEL_W = 268
BAR_X = PAD + LABEL_W + 18
BAR_W = 452
VALUE_X = WIDTH - PAD
COUNT_X = VALUE_X - 40
LABEL_SIZE = 13
TITLE_SIZE = 15
SUB_SIZE = 12

FONT = ("-apple-system, BlinkMacSystemFont, 'Segoe UI', 'PingFang SC', "
        "'Hiragino Sans GB', 'Microsoft YaHei', 'Helvetica Neue', Arial, sans-serif")

THEMES = {
    "light": {
        "bg": "#FFFFFF",
        "border": "#E4E9F2",
        "title": "#0F172A",
        "sub": "#8A94A6",
        "label": "#334155",
        "count": "#475569",
        "value": "#94A3B8",
        "track": "#EFF2F7",
        "divider": "#EDF0F5",
        "grad_from": "#4F7DF3",
        "grad_to": "#8E6BF2",
    },
    "dark": {
        "bg": "#0D1117",
        "border": "#222A36",
        "title": "#E6EDF3",
        "sub": "#7D8590",
        "label": "#C9D1D9",
        "count": "#AFB8C1",
        "value": "#7D8590",
        "track": "#1B222C",
        "divider": "#1F2631",
        "grad_from": "#5B8DEF",
        "grad_to": "#9E7BF5",
    },
}


def _esc(s: str) -> str:
    return (s.replace("&", "&amp;").replace("<", "&lt;")
             .replace(">", "&gt;").replace('"', "&quot;"))


def _text_width(s: str, size: float) -> float:
    """粗略估算文本像素宽度。

    SVG 无法在生成阶段测量真实字宽，用 em 系数近似：中日韩字符与全角标点按
    1.0em，ASCII 约 0.56em，空格 0.30em。只用于判断是否需要截断，不参与定位，
    因此少量误差不会影响版式。
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


def render_overview_svg(sections: list[dict], theme: str = "light") -> str:
    """生成概览 SVG。

    sections: [{"title": "分类分布", "note": "11 个分类", "rows": [("标签", 15), ...]}]
    rows 需调用方预先排好序（通常按计数降序）。
    """
    c = THEMES.get(theme, THEMES["light"])
    height = PAD * 2
    for i, sec in enumerate(sections):
        height += HEADER_H + len(sec["rows"]) * ROW_H
        if i < len(sections) - 1:
            height += SECTION_GAP

    out: list[str] = []
    out.append(
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        f'viewBox="0 0 {WIDTH} {height}" role="img" '
        f'aria-label="{_esc(" 与 ".join(s["title"] for s in sections))}">'
    )
    out.append("<defs>")
    out.append(
        f'<linearGradient id="bar" x1="0" y1="0" x2="1" y2="0">'
        f'<stop offset="0%" stop-color="{c["grad_from"]}"/>'
        f'<stop offset="100%" stop-color="{c["grad_to"]}"/>'
        f"</linearGradient>"
    )
    out.append("</defs>")
    out.append(
        f'<rect x="0.5" y="0.5" width="{WIDTH - 1}" height="{height - 1}" rx="12" '
        f'fill="{c["bg"]}" stroke="{c["border"]}"/>'
    )

    y = PAD
    for si, sec in enumerate(sections):
        rows = sec["rows"]
        peak = max((n for _, n in rows), default=1) or 1

        out.append(
            f'<text x="{PAD}" y="{y + 16}" font-family="{FONT}" font-size="{TITLE_SIZE}" '
            f'font-weight="600" fill="{c["title"]}">{_esc(sec["title"])}</text>'
        )
        if sec.get("note"):
            out.append(
                f'<text x="{VALUE_X}" y="{y + 16}" text-anchor="end" font-family="{FONT}" '
                f'font-size="{SUB_SIZE}" fill="{c["sub"]}">{_esc(sec["note"])}</text>'
            )

        base = y + HEADER_H
        for ri, (label, n) in enumerate(rows):
            center = base + ri * ROW_H
            by = center - BAR_H / 2
            w = max(2.0, BAR_W * n / peak)
            out.append(
                f'<text x="{PAD}" y="{center + 4.5}" font-family="{FONT}" '
                f'font-size="{LABEL_SIZE}" fill="{c["label"]}">'
                f'{_esc(_fit(label, LABEL_SIZE, LABEL_W))}</text>'
            )
            out.append(
                f'<rect x="{BAR_X}" y="{by}" width="{BAR_W}" height="{BAR_H}" rx="6.5" '
                f'fill="{c["track"]}"/>'
            )
            out.append(
                f'<rect x="{BAR_X}" y="{by}" width="{w:.1f}" height="{BAR_H}" rx="6.5" '
                f'fill="url(#bar)"/>'
            )
            pct = round(100 * n / sum(x for _, x in rows)) if rows else 0
            out.append(
                f'<text x="{COUNT_X}" y="{center + 4.5}" text-anchor="end" '
                f'font-family="{FONT}" font-size="{LABEL_SIZE}" font-weight="600" '
                f'fill="{c["count"]}">{n}</text>'
            )
            out.append(
                f'<text x="{VALUE_X}" y="{center + 4.5}" text-anchor="end" '
                f'font-family="{FONT}" font-size="11.5" fill="{c["value"]}">{pct}%</text>'
            )

        y = base + len(rows) * ROW_H
        if si < len(sections) - 1:
            out.append(
                f'<line x1="{PAD}" y1="{y + SECTION_GAP / 2:.1f}" x2="{VALUE_X}" '
                f'y2="{y + SECTION_GAP / 2:.1f}" stroke="{c["divider"]}"/>'
            )
            y += SECTION_GAP

    out.append("</svg>")
    return "\n".join(out)


def write_overview_assets(assets_dir: Path, sections: list[dict]) -> list[Path]:
    """写出浅色 / 深色两版 SVG，返回文件路径列表。"""
    assets_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for theme in ("light", "dark"):
        path = assets_dir / f"overview-{theme}.svg"
        path.write_text(render_overview_svg(sections, theme), encoding="utf-8")
        written.append(path)
    return written
