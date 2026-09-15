#!/usr/bin/env python3
"""starred-toolbox 同步脚本。

拉取 GitHub Star -> 与本地数据层比对 -> 对新增仓库调用 LLM 归类与解读
-> 回写 data/stars.json -> 渲染 README.md。

设计约束：
  1. 收录来源唯一，只有「你 Star 过的仓库」会进入 README，不做任何主动发现。
  2. 增量处理，已解读过的仓库不会重复调用 LLM。
  3. 无 LLM key 时自动降级为规则归类 + 官方描述，脚本仍可完整跑通。
  4. 隐私边界（元数据层 + 可见性层，两层都是硬约束）：
     - 元数据层：只读取 Star 列表的元数据字段，从不请求仓库文件、README
       正文或代码内容——STAR_QUERY 里没有任何 content / object / blob 字段。
       可写入仓库的字段由 PUBLISHABLE_FIELDS 白名单强制约束，写入前会调用
       assert_publishable 校验，出现白名单以外的字段直接报错退出。
     - 可见性层：本脚本从不对仓库可见性做任何写操作（无任何 visibility 变更调用）。
     publish_private=true 时，私有仓库以「名称 + 描述 + 链接 + 星数 + 语言」等
     元数据形式公开列出（用户明确接受的边界）；此时仍不抓取任何内容。
     publish_private=false 时，私有仓库被同时从 README.md 与 data/stars.json
     中剔除，不会落入任何会被提交的文件。
仅依赖 Python 标准库。
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import quote

# 同目录模块。脚本直接运行时 sys.path[0] 即 scripts/；
# validate_render.py 导入本模块前也已把 scripts/ 插入 sys.path。
from render_overview import write_overview_assets

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
ASSETS_DIR = ROOT / "assets"
CONFIG_FILE = DATA_DIR / "config.json"
TAXONOMY_FILE = DATA_DIR / "taxonomy.json"
STARS_FILE = DATA_DIR / "stars.json"
README_FILE = ROOT / "README.md"

GH_TOKEN = os.environ.get("STAR_TOKEN") or os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN") or ""
LLM_KEY = os.environ.get("LLM_API_KEY", "").strip()
# 用 or 而非 get 默认值：Actions 中未定义的 vars 会传入空字符串，
# 空字符串会让 get(key, default) 拿不到默认值。
LLM_BASE = (os.environ.get("LLM_BASE_URL") or "https://api.deepseek.com").rstrip("/")
LLM_MODEL = os.environ.get("LLM_MODEL") or "deepseek-chat"
LLM_BATCH = int(os.environ.get("LLM_BATCH") or "8")

# --- 可公开字段白名单 -------------------------------------------------------
# 这是「私有仓库只公开基本信息、不释放仓库内容」的机械保证，而不是一条注释约定。
# 白名单内全部是仓库元数据（名称、链接、描述、星数、语言、topics 等）与本脚本
# 自己生成的解读文本；任何内容型字段（README 正文、文件、代码、blob）都不在其中。
# 一旦有代码试图写入白名单以外的字段，assert_publishable 会在写盘前直接报错退出，
# 从而强制每一次字段扩展都经过一次「这个字段能不能公开」的人工判断。
PUBLISHABLE_FIELDS = frozenset({
    # 来自 GraphQL 元数据接口
    "full_name", "url", "description", "stars", "language", "topics",
    "license", "private", "archived", "fork", "pushed_at", "starred_at",
    # 本脚本自身生成
    "starred_active", "category", "what", "why", "analyzed_at", "analyzed_by",
})

# stars.json 顶层允许出现的键
PUBLISHABLE_DOC_FIELDS = frozenset({
    "version", "login", "last_sync", "repos",
    "excluded_private",  # 仅一个计数，不含任何单个仓库的信息
})

# 字段名里出现这些词，说明它很可能是内容型字段，报错时单独点名
CONTENT_FIELD_HINTS = ("readme", "content", "body", "file", "blob",
                       "tree", "code", "text", "raw", "patch", "diff")


def assert_publishable(stars_doc: dict) -> None:
    """写盘前校验：拒绝任何白名单以外的字段，防止内容型数据混入提交。"""
    unknown_doc = set(stars_doc) - PUBLISHABLE_DOC_FIELDS
    if unknown_doc:
        raise SystemExit(
            f"stars.json 顶层出现未登记字段 {sorted(unknown_doc)}。"
            "请先判断其是否可公开，再显式加入 PUBLISHABLE_DOC_FIELDS。"
        )

    bad: dict[str, list[str]] = {}
    for key, repo in stars_doc.get("repos", {}).items():
        extra = set(repo) - PUBLISHABLE_FIELDS
        if extra:
            bad[repo.get("full_name", key)] = sorted(extra)
    if not bad:
        return

    risky = sorted({f for fields in bad.values() for f in fields
                    if any(h in f.lower() for h in CONTENT_FIELD_HINTS)})
    detail = "; ".join(f"{n} -> {f}" for n, f in list(bad.items())[:5])
    more = f"（另有 {len(bad) - 5} 个条目，已省略）" if len(bad) > 5 else ""
    msg = (f"已阻止写入：{len(bad)} 个条目含有白名单以外的字段。{detail}{more}")
    if risky:
        msg += (f"\n其中 {risky} 疑似内容型字段，可能把仓库正文带进提交，"
                "必须在确认可公开后才能加入 PUBLISHABLE_FIELDS。")
    raise SystemExit(msg)

STAR_QUERY = """
query($cursor: String) {
  viewer {
    login
    starredRepositories(first: 100, after: $cursor,
                        orderBy: {field: STARRED_AT, direction: DESC}) {
      totalCount
      pageInfo { hasNextPage endCursor }
      edges {
        starredAt
        node {
          nameWithOwner
          url
          description
          stargazerCount
          isArchived
          isPrivate
          isFork
          pushedAt
          primaryLanguage { name }
          repositoryTopics(first: 20) { nodes { topic { name } } }
          licenseInfo { spdxId }
        }
      }
    }
  }
}
"""

SYSTEM_PROMPT = """你是工程知识管理助手，为一位汽车热管理与智能驾驶软件工程师维护个人 GitHub 星标归档库。

你会收到一批 GitHub 仓库的元数据，需要为每一个输出归类与解读。要求：

1. category 必须从给定分类列表中精确选择一个 key，不得自创、不得拼接。
   判断依据是「这个仓库本质上是做什么的」，而不是它用了什么技术。
   例如一个用 Electron 写的 RSS 阅读器应归入 productivity，而不是因为它用 JS 就归入别处。

2. what 用一句中文说明这是什么工具/资源，20-40 字，客观陈述，不要评价。
   正确：「在终端中自主完成代码修改与 Git 操作的编码智能体。」
   错误：「非常强大的终端编码神器。」

3. why 用一句中文说明什么时候用得上它，20-50 字，从使用者视角出发。
   正确：「需要一个可本地部署、不绑定厂商的编码 Agent 时。」
   若确实看不出用途，写「信息有限，待补充。」

禁止使用「强大」「优秀」「最佳」「神器」「领先」等评价性词汇。
只输出 JSON，不要任何解释文字。"""


def log(msg: str) -> None:
    print(msg, flush=True)


def http_json(url: str, headers: dict, payload: dict | None = None, timeout: int = 90) -> dict:
    data = json.dumps(payload).encode("utf-8") if payload is not None else None
    req = urllib.request.Request(url, data=data, headers=headers,
                                 method="POST" if data else "GET")
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return json.loads(resp.read().decode("utf-8"))


def gh_graphql(query: str, variables: dict | None = None, retries: int = 3) -> dict:
    if not GH_TOKEN:
        raise SystemExit("缺少 STAR_TOKEN / GITHUB_TOKEN 环境变量，无法读取 Star 列表。")
    for attempt in range(retries):
        try:
            out = http_json(
                "https://api.github.com/graphql",
                {
                    "Authorization": f"bearer {GH_TOKEN}",
                    "Content-Type": "application/json",
                    "User-Agent": "starred-toolbox-sync",
                    "Accept": "application/json",
                },
                {"query": query, "variables": variables or {}},
            )
            if "errors" in out:
                raise RuntimeError(f"GraphQL 错误: {out['errors']}")
            return out["data"]
        except urllib.error.HTTPError as e:
            body = e.read().decode("utf-8", "replace")[:300]
            if attempt == retries - 1:
                raise SystemExit(f"GitHub API 失败 HTTP {e.code}: {body}")
            log(f"  GitHub API 重试 ({attempt + 1}/{retries}) HTTP {e.code}")
            time.sleep(3 * (attempt + 1))
    raise SystemExit("GitHub API 不可达。")


def fetch_all_stars() -> tuple[str, dict[str, dict]]:
    """返回 (login, {full_name_lower: repo_dict})。"""
    login = ""
    repos: dict[str, dict] = {}
    cursor = None
    page = 0
    while True:
        data = gh_graphql(STAR_QUERY, {"cursor": cursor})
        viewer = data["viewer"]
        login = viewer["login"]
        block = viewer["starredRepositories"]
        for edge in block["edges"]:
            n = edge["node"]
            name = n["nameWithOwner"]
            repos[name.lower()] = {
                "full_name": name,
                "url": n["url"],
                "description": (n.get("description") or "").strip(),
                "stars": n["stargazerCount"],
                "language": (n.get("primaryLanguage") or {}).get("name") or "",
                "topics": sorted(t["topic"]["name"] for t in n["repositoryTopics"]["nodes"]),
                "license": (n.get("licenseInfo") or {}).get("spdxId") or "",
                "private": n["isPrivate"],
                "archived": n["isArchived"],
                "fork": n["isFork"],
                "pushed_at": (n.get("pushedAt") or "")[:10],
                "starred_at": edge["starredAt"],
            }
        page += 1
        log(f"  已拉取第 {page} 页，累计 {len(repos)} / {block['totalCount']}")
        if not block["pageInfo"]["hasNextPage"]:
            break
        cursor = block["pageInfo"]["endCursor"]
    return login, repos


def rule_category(repo: dict, taxonomy: dict) -> str:
    """无 LLM 时的关键词兜底归类。"""
    text = " ".join([
        repo.get("full_name", "").lower(),
        (repo.get("description") or "").lower(),
        " ".join(repo.get("topics", [])).lower(),
    ])
    rules = [
        ("automotive", ("canoe", "canape", "ecu", "can-", "uds", "lin", "doip",
                        "autosar", "vehicle", "thermal", "calibration", "pid")),
        ("matlab-mbd", ("matlab", "simulink", "stateflow", "model-based", "mbd")),
        ("knowledge-rag", ("rag", "knowledge", "wiki", "graphrag", "lightrag", "memory")),
        ("agent-tooling", ("mcp", "skill", "plugin", "sidebar", "toolkit")),
        ("ai-agent", ("agent", "autogpt", "autonomous", "coding assistant")),
        ("learning", ("tutorial", "course", "book", "learn", "handbook", "题解",
                      "教程", "学习", "入门", "指南")),
        ("ml-framework", ("framework", "pytorch", "tensorflow", "paddle", "inference")),
        ("content-creation", ("stable-diffusion", "video", "image generat", "写作", "design")),
        ("productivity", ("rss", "reader", "viewer", "monitor", "trend", "zotero")),
        ("methodology", ("spec-driven", "sdd", "workflow", "guidance", "handbook")),
    ]
    for key, words in rules:
        if any(w in text for w in words):
            return key
    return "other"


def llm_batch(repos: list[dict], taxonomy: dict, retries: int = 3) -> dict[str, dict]:
    """批量归类与解读，返回 {full_name_lower: {category, what, why}}。"""
    cats = "\n".join(
        f"- {c['key']}: {c['title']} —— {c['desc']}" for c in taxonomy["categories"]
    )
    items = []
    for i, r in enumerate(repos, 1):
        items.append(
            f"{i}. full_name: {r['full_name']}\n"
            f"   官方描述: {r['description'] or '(无)'}\n"
            f"   语言: {r['language'] or '未知'} | topics: {', '.join(r['topics']) or '无'}"
        )
    user_prompt = (
        f"分类列表：\n{cats}\n\n"
        f"待归类仓库（{len(repos)} 个）：\n" + "\n".join(items) + "\n\n"
        "输出 JSON 对象，格式：\n"
        '{"results":[{"full_name":"<原样返回>","category":"<key>",'
        '"what":"<中文20-40字>","why":"<中文20-50字>"}]}\n'
        f"results 必须恰好包含 {len(repos)} 项，顺序与输入一致。"
    )

    for attempt in range(retries):
        try:
            out = http_json(
                f"{LLM_BASE}/chat/completions",
                {
                    "Authorization": f"Bearer {LLM_KEY}",
                    "Content-Type": "application/json",
                },
                {
                    "model": LLM_MODEL,
                    "messages": [
                        {"role": "system", "content": SYSTEM_PROMPT},
                        {"role": "user", "content": user_prompt},
                    ],
                    "temperature": 0.2,
                    "response_format": {"type": "json_object"},
                },
            )
            content = out["choices"][0]["message"]["content"]
            parsed = json.loads(content)
            valid_keys = {c["key"] for c in taxonomy["categories"]}
            result = {}
            for row in parsed.get("results", []):
                key = (row.get("full_name") or "").lower()
                cat = row.get("category", "other")
                result[key] = {
                    "category": cat if cat in valid_keys else "other",
                    "what": (row.get("what") or "").strip(),
                    "why": (row.get("why") or "").strip(),
                }
            if result:
                return result
            raise RuntimeError("LLM 返回结果为空")
        except Exception as e:
            if attempt == retries - 1:
                log(f"  LLM 调用失败，本批降级处理: {e}")
                return {}
            log(f"  LLM 重试 ({attempt + 1}/{retries}): {e}")
            time.sleep(5 * (attempt + 1))
    return {}


def slugify(title: str) -> str:
    s = title.lower().strip()
    s = re.sub(r"[^\w\s-]", "", s, flags=re.UNICODE)
    s = re.sub(r"\s+", "-", s)
    return s


def load_json(path: Path, default: dict) -> dict:
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as e:
        raise SystemExit(f"{path} 不是合法 JSON: {e}")


def fmt_stars(n: int) -> str:
    if n >= 1000:
        return f"{n / 1000:.1f}k".replace(".0k", "k")
    return str(n)


def shields(label: str, message: str, color: str, logo: str = "") -> str:
    """构造 shields.io 静态徽章 URL。

    徽章内容是 SVG 文本节点，由客户端渲染，中文不会被服务端字体限制。
    需要注意 shields 的转义规则：`-` 复用为分隔符，`_` 复用为空格，
    因此出现在 label/message 里的这两个字符都要各自重复一次。
    """
    def part(s: str) -> str:
        return quote(s.replace("-", "--").replace("_", "__").replace(" ", "_"))

    url = f"https://img.shields.io/badge/{part(label)}-{part(message)}-{color}?style=flat-square"
    if logo:
        url += f"&logo={quote(logo)}&logoColor=white"
    return url


def build_overview_sections(repos: dict, taxonomy: dict) -> list[dict]:
    """汇总用于概览图的两个分布：分类分布与语言分布。

    只输出「标签 + 计数」，标签来自 taxonomy 的分类标题或语言名，
    不含任何与单个仓库相关的信息。
    """
    cats = taxonomy["categories"]
    active = [r for r in repos.values() if r.get("starred_active", True)]

    cat_count: dict[str, int] = {}
    for r in active:
        key = r.get("category", "other")
        cat_count[key] = cat_count.get(key, 0) + 1
    cat_rows = [(c["title"], cat_count[c["key"]])
                for c in cats if cat_count.get(c["key"])]
    cat_rows.sort(key=lambda x: (-x[1], x[0]))

    lang_count: dict[str, int] = {}
    for r in active:
        lang = r.get("language") or "未标注"
        lang_count[lang] = lang_count.get(lang, 0) + 1
    lang_rows = sorted(lang_count.items(), key=lambda x: (-x[1], x[0]))[:8]

    return [
        {
            "title": "分类分布",
            "note": f"{len(cat_rows)} 个分类 · {len(active)} 个条目",
            "rows": cat_rows,
        },
        {
            "title": "语言分布",
            "note": f"共 {len(lang_count)} 种 · 取前 {len(lang_rows)}",
            "rows": lang_rows,
        },
    ]


def render_readme(stars_doc: dict, taxonomy: dict, cfg: dict) -> str:
    repos = {k: v for k, v in stars_doc["repos"].items() if v.get("starred_active", True)}
    cats = taxonomy["categories"]
    login = stars_doc.get("login", "")

    grouped: dict[str, list[dict]] = {c["key"]: [] for c in cats}
    for r in repos.values():
        grouped.setdefault(r.get("category", "other"), []).append(r)

    for key in grouped:
        grouped[key].sort(key=lambda x: (-x["stars"], x["full_name"].lower()))

    total = len(repos)
    priv_count = sum(1 for r in repos.values() if r.get("private"))
    present = [c for c in cats if grouped.get(c["key"])]
    last_sync = stars_doc.get("last_sync", "")

    self_owners = [o.lower() for o in cfg.get("self_owners", [])]
    mine = sorted(
        (r for r in repos.values()
         if r["full_name"].split("/")[0].lower() in self_owners),
        key=lambda x: x["full_name"].lower(),
    )

    out: list[str] = []
    out.append("# Starred Toolbox")
    out.append("")

    # 徽章行。放在 H1 之后、正文之前，作为一眼可读的状态摘要。
    # 前四个是静态徽章（数值由脚本写入 URL），最后一个是 GitHub Actions 的
    # 动态徽章——它能直接反映「定时同步是否还在正常工作」，是这条自动化链路
    # 唯一的可视化健康指示。
    badges = [
        f"![收录 {total} 个仓库]({shields('收录', f'{total} 个仓库', '4F7DF3')})",
        f"![{len(present)} 个分类]({shields('分类', f'{len(present)} 个', '8E6BF2')})",
    ]
    if mine:
        badges.append(f"![自研 {len(mine)} 个]({shields('自研', f'{len(mine)} 个', '5B8DEF')})")
    if last_sync:
        badges.append(
            f"![最后同步 {last_sync}]({shields('同步', last_sync.split(' ')[0], '64748B')})"
        )
    repo_slug = cfg.get("repo", "")
    if repo_slug:
        badges.append(
            f"![定时同步状态](https://github.com/{repo_slug}"
            "/actions/workflows/sync-stars.yml/badge.svg?branch=main)"
        )
    out.append(" ".join(badges))
    out.append("")
    out.append("> 我在 GitHub 星标的工具与资源归档。来源只有一个：**我的 Star**。")
    out.append("> 未经星标的内容不会出现在这里。归类与解读由脚本自动生成。")
    out.append("")
    if priv_count and cfg.get("publish_private"):
        out.append(
            f"<sub>其中 {priv_count} 个为本人的私有仓库。此处只列出名称、描述与链接等"
            "基本信息，其代码与文件内容不对外释放，点击链接需要对应访问权限。</sub>"
        )
    elif stars_doc.get("excluded_private"):
        out.append(
            f"<sub>另有 {stars_doc['excluded_private']} 个私有仓库收藏未列出："
            "本归档不写入私有仓库的名称、描述或链接，也不改变其可见性。</sub>"
        )
    out.append("")

    # 概览：分布图 + 最近加入。图由 scripts/render_overview.py 生成，
    # 浅色/深色两版通过 <picture> 随 GitHub 主题切换。
    out.append("## 概览")
    out.append("")
    out.append("<picture>")
    out.append('  <source media="(prefers-color-scheme: dark)" '
               'srcset="assets/overview-dark.svg">')
    out.append('  <img alt="分类分布与语言分布" src="assets/overview-light.svg">')
    out.append("</picture>")
    out.append("")
    if last_sync:
        out.append(f"<sub>最后同步：{last_sync}</sub>")
        out.append("")

    recent = sorted(repos.values(),
                    key=lambda x: x.get("starred_at") or "", reverse=True)[:5]
    if recent:
        out.append("### 最近加入")
        out.append("")
        out.append("| 仓库 | 分类 | 星标于 |")
        out.append("| :--- | :--- | :--- |")
        for r in recent:
            cat_title = next((c["title"] for c in cats
                              if c["key"] == r.get("category")), "其他")
            out.append(f"| [{r['full_name']}]({r['url']}) | {cat_title} | "
                       f"{(r.get('starred_at') or '')[:10]} |")
        out.append("")

    # 目录：表格形式，`占比` 列用方块字符近似条形，比纯文本列表更容易看出重心。
    out.append("## 目录")
    out.append("")
    out.append("| 分类 | 数量 | 占比 |")
    out.append("| :--- | ---: | :--- |")
    peak = max((len(grouped[c["key"]]) for c in present), default=1)
    for c in present:
        n = len(grouped[c["key"]])
        blocks = "█" * max(1, round(16 * n / peak))
        out.append(f"| [{c['title']}](#{slugify(c['title'])}) | {n} | `{blocks}` |")
    out.append("")
    if mine:
        out.append(f"<sub>另有 [我的自研项目](#我的自研项目) 快捷索引，共 {len(mine)} 个。</sub>")
        out.append("")

    # 分类正文
    for c in present:
        items = grouped[c["key"]]
        out.append(f"## {c['title']}")
        out.append("")
        out.append(f"<sub>共 {len(items)} 个 · [返回目录](#目录)</sub>")
        out.append("")
        for r in items:
            owner = r["full_name"].split("/")[0].lower()
            marks = []
            if r.get("language"):
                marks.append(f"`{r['language']}`")
            marks.append(f"`★ {fmt_stars(r['stars'])}`")
            if r.get("private"):
                marks.append("`私有`")
            if r.get("archived"):
                marks.append("`已归档`")
            if owner in self_owners:
                marks.append("`自研`")
            out.append(f"- **[{r['full_name']}]({r['url']})** {' '.join(marks)}")
            if r.get("what"):
                out.append(f"  {r['what']}")
            if r.get("why"):
                out.append(f"  <sub>↳ {r['why']}</sub>")
        out.append("")

    # 自研项目索引
    if mine:
        out.append("## 我的自研项目")
        out.append("")
        out.append("以下仓库同时出现在上方对应分类中，此处仅作快捷索引。")
        out.append("")
        out.append("| 仓库 | 所属分类 |")
        out.append("| :--- | :--- |")
        for r in mine:
            cat_title = next(
                (c["title"] for c in cats if c["key"] == r.get("category")), "其他"
            )
            out.append(f"| [{r['full_name']}]({r['url']}) | {cat_title} |")
        out.append("")

    out.append("---")
    out.append("")
    out.append("[返回目录](#目录)")
    out.append("")
    out.append("<details>")
    out.append("<summary>这个归档是怎么运转的</summary>")
    out.append("")
    out.append("- 唯一来源是本账号的 Star 列表，由 GitHub Actions 每天定时拉取，"
               "不做任何主动发现。")
    out.append("- 新增条目会调用大模型归类并生成「这是什么 / 什么时候用」两句解读；"
               "没有配置模型密钥时降级为规则归类。")
    out.append("- 私有仓库只公开名称、描述与链接等元数据，"
               "同步脚本从不请求仓库文件、README 正文或代码内容。")
    out.append("- 取消 Star 后，条目会在下次同步时移出列表。")
    out.append("")
    out.append("<sub>本文件与 `assets/` 下的分布图均由 `scripts/sync_stars.py` 自动生成，"
               "请勿手工编辑。</sub>")
    out.append("")
    out.append("</details>")
    out.append("")
    return "\n".join(out)


def emit_outputs(stars_doc: dict, taxonomy: dict, cfg: dict, dry_run: bool = False) -> None:
    """渲染并写出 README 与概览图。dry_run 时只计算不落盘。"""
    content = render_readme(stars_doc, taxonomy, cfg)
    active = {k: v for k, v in stars_doc["repos"].items()
              if v.get("starred_active", True)}
    sections = build_overview_sections(active, taxonomy)
    if dry_run:
        log("  [dry-run] 未写入文件")
        return
    for path in write_overview_assets(ASSETS_DIR, sections):
        log(f"  已写入 {path.relative_to(ROOT)}")
    README_FILE.write_text(content, encoding="utf-8")
    log(f"  已写入 {README_FILE.relative_to(ROOT)}（{len(content)} 字符）")


def main() -> int:
    ap = argparse.ArgumentParser(description="同步 GitHub Star 到归档 README")
    ap.add_argument("--dry-run", action="store_true", help="只打印将要执行的动作，不写文件")
    ap.add_argument("--no-llm", action="store_true", help="强制禁用 LLM，使用规则归类")
    ap.add_argument("--limit", type=int, default=0, help="本次最多处理多少个新增仓库")
    ap.add_argument("--render-only", action="store_true", help="跳过同步，仅重新渲染 README")
    ap.add_argument("--reanalyze-all", action="store_true",
                    help="强制对所有条目重新归类与解读（需要 LLM key）")
    ap.add_argument("--verify-token", action="store_true",
                    help="只检查 STAR_TOKEN 能读到哪些 Star，并报告私有仓库是否可见")
    ap.add_argument("--check-publishable", action="store_true",
                    help="只校验 data/stars.json 是否只含可公开字段，不写任何文件")
    args = ap.parse_args()

    if args.check_publishable:
        doc = load_json(STARS_FILE, {})
        assert_publishable(doc)
        repos = doc.get("repos", {})
        priv = sum(1 for v in repos.values() if v.get("private"))
        log(f"校验通过：{len(repos)} 条记录全部只含可公开字段（白名单 "
            f"{len(PUBLISHABLE_FIELDS)} 个），其中私有仓库 {priv} 条。")
        return 0

    if args.reanalyze_all and not LLM_KEY:
        raise SystemExit("--reanalyze-all 需要 LLM_API_KEY，否则只会用规则覆盖现有解读。")

    taxonomy = load_json(TAXONOMY_FILE, {})
    if not taxonomy.get("categories"):
        raise SystemExit(f"缺少分类定义：{TAXONOMY_FILE}")
    cfg = load_json(CONFIG_FILE, {})
    stars_doc = load_json(STARS_FILE, {
        "version": 1, "login": "", "last_sync": "", "repos": {}
    })
    stars_doc.setdefault("repos", {})

    use_llm = bool(LLM_KEY) and not args.no_llm

    if args.verify_token:
        log("检查 STAR_TOKEN 的读取范围")
        login, remote = fetch_all_stars()
        priv = sorted(k for k, v in remote.items() if v.get("private"))
        log(f"  账号: {login}")
        log(f"  可见 Star 总数: {len(remote)}")
        log(f"  其中私有仓库: {len(priv)}")
        for k in priv:
            log(f"    - {remote[k]['full_name']}")
        if not priv:
            log("  提示：未读到任何私有仓库。若你确实 Star 过私有仓库，说明该 token "
                "缺少读取私有仓库的权限，同步会漏掉它们。")
            log("        classic token 需 repo scope；fine-grained 需 "
                "Starring: read + Metadata: read 且覆盖私有仓库。")
        return 0

    if args.render_only:
        assert_publishable(stars_doc)
        log(f"重新渲染 README 与概览图（{len(stars_doc['repos'])} 条数据）")
        emit_outputs(stars_doc, taxonomy, cfg)
        return 0

    log("步骤 1/4：拉取 Star 列表")
    login, remote = fetch_all_stars()
    stars_doc["login"] = login
    log(f"  账号 {login}，共 {len(remote)} 个 Star")

    local = stars_doc["repos"]

    # 隐私边界：私有仓库默认不进入任何会被提交的文件。
    # 关键点是「两层都要剔除」——README 是渲染产物，data/stars.json 同样会被提交，
    # 只在渲染层过滤等于把名称和描述留在了仓库里。宁可下次重新分析，也不落盘。
    publish_private = bool(cfg.get("publish_private", False))
    excluded_private = 0
    if not publish_private:
        priv_remote = [k for k, v in remote.items() if v.get("private")]
        excluded_private = len(priv_remote)
        for k in priv_remote:
            remote.pop(k, None)
        # 历史遗留清理：早期版本可能已经把私有仓库写进过 stars.json
        priv_local = [k for k, v in local.items() if v.get("private")]
        for k in priv_local:
            local.pop(k, None)
        if excluded_private or priv_local:
            log(f"  隐私策略生效：排除远端 {excluded_private} 个私有仓库，"
                f"清理本地历史记录 {len(priv_local)} 条")
    stars_doc["excluded_private"] = excluded_private

    # 新增：远端有、本地无，或本地缺解读
    new_keys = [k for k in remote if k not in local]
    unanalyzed = [
        k for k in remote
        if k in local and (
            not local[k].get("what")
            # 之前用规则兜底归类的条目，一旦拿到 LLM key 就自动重做
            or (use_llm and local[k].get("analyzed_by") == "rule")
        )
    ]

    # 取消星标：本地标记 active 但远端已不存在
    unstarred = [k for k, v in local.items()
                 if v.get("starred_active", True) and k not in remote]

    log(f"  新增 {len(new_keys)} 条，待补充解读 {len(unanalyzed)} 条，已取消星标 {len(unstarred)} 条")

    for k in unstarred:
        local[k]["starred_active"] = False
        log(f"    - 取消星标，移出列表: {local[k]['full_name']}")

    # 同步元数据（stars / archived / pushed_at 等会变化）
    for k, fresh in remote.items():
        if k in local:
            keep = {f: local[k].get(f)
                    for f in ("category", "what", "why", "analyzed_at", "analyzed_by")}
            local[k].update(fresh)
            local[k].update({f: v for f, v in keep.items() if v is not None})
            local[k]["starred_active"] = True
        else:
            local[k] = dict(fresh, starred_active=True)

    # 需要 LLM 处理的
    if args.reanalyze_all:
        targets = [v for v in local.values() if v.get("starred_active", True)]
    else:
        targets = [local[k] for k in new_keys + unanalyzed]
    if args.limit:
        targets = targets[: args.limit]

    if targets:
        log(f"步骤 2/4：归类与解读（{len(targets)} 条，"
            f"{'LLM ' + LLM_MODEL if use_llm else '规则模式'}）")
        for i in range(0, len(targets), LLM_BATCH):
            batch = targets[i: i + LLM_BATCH]
            if use_llm:
                result = llm_batch(batch, taxonomy)
            else:
                result = {}
            for r in batch:
                key = r["full_name"].lower()
                got = result.get(key)
                if got and got.get("what"):
                    r.update(got)
                    r["analyzed_by"] = "llm"
                else:
                    r["category"] = rule_category(r, taxonomy)
                    r["what"] = r["description"] or "（暂无描述）"
                    r["why"] = ""
                    r["analyzed_by"] = "rule"
                r["analyzed_at"] = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
            log(f"  已处理 {min(i + LLM_BATCH, len(targets))}/{len(targets)}")
            if use_llm and i + LLM_BATCH < len(targets):
                time.sleep(1)

    # 未解读的远端项兜底归类
    for k, v in local.items():
        if v.get("starred_active", True) and not v.get("category"):
            v["category"] = rule_category(v, taxonomy)
            v["what"] = v.get("what") or v.get("description") or "（暂无描述）"

    stars_doc["last_sync"] = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    active = sum(1 for v in local.values() if v.get("starred_active", True))
    log(f"步骤 3/4：写回数据层（活跃 {active} / 累计 {len(local)}）")
    # 写盘前的最后一道闸：只允许白名单字段进入会被提交的文件
    assert_publishable(stars_doc)
    if not args.dry_run:
        STARS_FILE.write_text(
            json.dumps(stars_doc, ensure_ascii=False, indent=2, sort_keys=True),
            encoding="utf-8",
        )

    log("步骤 4/4：渲染 README 与概览图")
    emit_outputs(stars_doc, taxonomy, cfg, dry_run=args.dry_run)

    log("完成。")
    return 0


if __name__ == "__main__":
    sys.exit(main())
