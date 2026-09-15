#!/usr/bin/env python3
"""渲染结果校验：CI 与本地共用。

三件事：
  1. 复用 sync_stars 的字段白名单，确认没有任何内容型字段进入会被提交的文件。
  2. 每个活跃条目都必须出现在 README 中（防止渲染漏项）。
  3. README 中标记为「私有」的条目数必须与数据层一致（防止两边口径漂移）。

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
README_FILE = ROOT / "README.md"
ASSETS = ("overview-light.svg", "overview-dark.svg")

# 「私有」标记只认可条目行上的那一处。README 其他位置（概览说明、统计文字）
# 也可能出现「私有」二字，用整串计数会把它们误算进条目数。
ENTRY_MARKER = re.compile(r"^- \*\*\[[^\]]+\]\([^)]+\)\*\*[^\n]*`私有`", re.M)


def main() -> int:
    problems: list[str] = []

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

    print(f"数据层：{len(repos)} 条记录，活跃 {len(active)} 条，其中私有 {len(priv_data)} 条")
    print(f"字段白名单：{len(PUBLISHABLE_FIELDS)} 个字段")
    print(f"README 中 `私有` 标记：{marker_count} 处")
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
