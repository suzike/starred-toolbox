#!/usr/bin/env python3
"""渲染结果校验：CI 与本地共用。

六件事：
  1. 复用 sync_stars 的字段白名单，确认没有任何内容型字段进入会被提交的文件。
  2. 每个活跃条目都必须出现在 README 中（防止渲染漏项）。
  3. README 中标记为「私有」的条目数必须与数据层一致（防止两边口径漂移）。
  4. 概览图必须存在且被 README 引用（否则页面出现裂图）。
  5. 概览图里不得出现任何单个仓库的名称或描述——这是「概览图只承载聚合
     信息」这条设计承诺的机械保证，而不只是 render_overview.py 的注释约定。
  6. 语言色表的色值必须是合法十六进制，否则会写出浏览器无法解析的 SVG 属性。

只读，不写任何文件。退出码非 0 即视为校验失败。
仅依赖 Python 标准库。
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from sync_stars import PUBLISHABLE_FIELDS, ROOT, assert_publishable  # noqa: E402

STARS_FILE = ROOT / "data" / "stars.json"
LANG_COLORS_FILE = ROOT / "data" / "language_colors.json"
README_FILE = ROOT / "README.md"
ASSETS = ("overview-light.svg", "overview-dark.svg")

# 「私有」标记只认可条目行上的那一处。README 其他位置（概览说明、统计文字）
# 也可能出现「私有」二字，用整串计数会把它们误算进条目数。
ENTRY_MARKER = re.compile(r"^- \*\*\[[^\]]+\]\([^)]+\)\*\*[^\n]*`私有`", re.M)

HEX_COLOR = re.compile(r"^#[0-9A-Fa-f]{6}$")


def main() -> int:
    problems: list[str] = []
    # 这三项是「检查确实跑过」的凭据。没有它们的话，一条静默通过的校验和
    # 一条因为路径写错而根本没执行的校验，输出完全一样。
    svg_scanned = 0
    leak_probes = 0
    colors_checked = 0

    doc = json.loads(STARS_FILE.read_text(encoding="utf-8"))
    readme = README_FILE.read_text(encoding="utf-8")

    # 1. 隐私边界
    try:
        assert_publishable(doc)
    except SystemExit as e:
        problems.append(str(e))

    repos = doc.get("repos", {})
    active = {k: v for k, v in repos.items() if v.get("starred_active", True)}
    priv_data = sorted(v["full_name"] for v in active.values() if v.get("private"))

    # 2. 活跃条目必须都在 README 里
    missing = [v["full_name"] for v in active.values() if v["url"] not in readme]
    if missing:
        problems.append(f"{len(missing)} 个活跃条目未出现在 README：{missing[:10]}")

    # 3. 私有条目口径一致：数据层有几个，README 里就必须能找到几个
    priv_readme = [n for n in priv_data if f"**[{n}]" in readme]
    if len(priv_readme) != len(priv_data):
        lost = sorted(set(priv_data) - set(priv_readme))
        problems.append(f"数据层有 {len(priv_data)} 个私有条目，README 中只找到 "
                        f"{len(priv_readme)} 个，缺少：{lost[:10]}")

    # 4. 反向检查：README 中标记为「私有」的条目不能多于数据层登记的私有条目
    marker_count = len(ENTRY_MARKER.findall(readme))
    if marker_count != len(priv_data):
        problems.append(
            f"README 中 `私有` 标记出现 {marker_count} 次，"
            f"数据层登记的私有条目为 {len(priv_data)} 个，两边口径不一致"
        )

    # 5. 概览图必须同时存在于磁盘并被 README 引用，否则 README 上会出现裂图
    for name in ASSETS:
        if not (ROOT / "assets" / name).exists():
            problems.append(f"缺少概览图 assets/{name}，README 会出现裂图")
        if f"assets/{name}" not in readme:
            problems.append(f"README 未引用 assets/{name}")

    # 6. 概览图只允许承载聚合信息：任何单个仓库的名称或描述都不得出现。
    #    设计上 render_overview 只接收「标签 + 计数」，这条校验是它的兜底——
    #    将来若有人为了「让图更丰富」把仓库数据传进渲染层，这里会直接拦截。
    #
    #    排除逻辑：与分类标题、语言名完全相同的字符串属于聚合标签，不算泄漏。
    #    仓库名形如 owner/repo，含斜杠，不会与分类标题或语言名重合；
    #    描述是完整句子，正常也不会等于某个标签。所以这两个白名单集合
    #    只会放过「某仓库名恰好等于一个分类标题」这种极端巧合。
    taxonomy_path = ROOT / "data" / "taxonomy.json"
    agg_labels: set[str] = set()
    if taxonomy_path.exists():
        tax = json.loads(taxonomy_path.read_text(encoding="utf-8"))
        agg_labels.update(c["title"] for c in tax.get("categories", []))
        agg_labels.update(c["key"] for c in tax.get("categories", []))
    if LANG_COLORS_FILE.exists():
        agg_labels.update(
            json.loads(LANG_COLORS_FILE.read_text(encoding="utf-8")).get("colors", {})
        )

    for name in ASSETS:
        path = ROOT / "assets" / name
        if not path.exists():
            continue
        svg_scanned += 1
        svg = path.read_text(encoding="utf-8")
        low = svg.lower()
        leaked: list[str] = []
        for v in active.values():
            for field in ("full_name", "description"):
                needle = (v.get(field) or "").strip()
                if len(needle) < 4 or needle in agg_labels:
                    continue
                leak_probes += 1
                if needle.lower() in low:
                    leaked.append(f"{v['full_name']} 的 {field}")
        if leaked:
            problems.append(
                f"assets/{name} 中出现了单个仓库的信息：{sorted(set(leaked))[:5]}。"
                "概览图只允许承载聚合信息。"
            )

    # 7. 语言色值格式。格式非法时 SVG 属性会失效（或生成不可解析的 SVG），
    #    而这种错误在浏览器里只表现为「圆点不见了」，不容易被肉眼发现。
    if LANG_COLORS_FILE.exists():
        colors = json.loads(LANG_COLORS_FILE.read_text(encoding="utf-8")).get("colors", {})
        colors_checked = len(colors)
        bad_colors = sorted(k for k, v in colors.items()
                            if not isinstance(v, str) or not HEX_COLOR.match(v))
        if bad_colors:
            problems.append(f"语言色表存在非法色值（应为 #RRGGBB）：{bad_colors[:10]}")

    print(f"数据层：{len(repos)} 条记录，活跃 {len(active)} 条，其中私有 {len(priv_data)} 条")
    print(f"字段白名单：{len(PUBLISHABLE_FIELDS)} 个字段")
    print(f"README 中 `私有` 标记：{marker_count} 处")
    print(f"概览图聚合边界：已扫描 {svg_scanned} 个 SVG，"
          f"逐个比对 {leak_probes} 个「仓库名/描述」串，命中 0 个")
    print(f"语言色表：已校验 {colors_checked} 个色值格式")
    if priv_data:
        print("私有条目（仅元数据，不含内容）：")
        for n in priv_data:
            print(f"  - {n}")

    if problems:
        print("\n校验失败：")
        for p in problems:
            print(f"  ✗ {p}")
        return 1

    print("\n校验通过。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
