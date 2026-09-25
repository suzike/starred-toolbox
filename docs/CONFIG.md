# 配置说明

同步脚本依赖两类凭据。**两者都只以 GitHub Actions Secret 的形式存在，不进入代码库。**

> **先读这一条。** 本仓库是公开仓库，而 `publish_private: true` 表示**私有仓库会以
> 名称、描述、链接、星数、语言等元数据形式公开列出**。这是明确设定的边界：
> 基本信息可对外展示，仓库内容（代码、文件、README 正文）不对外释放。
> 内容不释放不是靠约定，而是靠 `scripts/sync_stars.py` 的 `PUBLISHABLE_FIELDS`
> 白名单强制约束，以及脚本从不调用任何内容型接口。详见文末[七、边界与隐私](#七边界与隐私)。

---

## 一、`STAR_TOKEN` —— 读取你的 Star 列表

### 为什么不能用内置的 `GITHUB_TOKEN`

Actions 自动注入的 `GITHUB_TOKEN` 作用域**被限制在当前仓库**，它无法读取账号级别的 Star 列表。必须单独创建一个 Personal Access Token。

### 关键前提：token 必须能看到私有仓库

私有条目要出现在归档里，token 就必须有读取私有仓库的权限。这是最容易配错的一步。

| 方案 | 所需权限 | 说明 |
|---|---|---|
| **classic PAT** | `repo` | 实测可用（本机 `gh` 的 token 含 `repo` + `workflow`，读到全部 76 个 Star，含 11 个私有仓）。但 `repo` 较宽，会给出私有仓库的**读写**能力 |
| **fine-grained PAT**（推荐） | Account permissions: **Starring → Read**；Repository permissions: **Metadata → Read**，仓库范围选 **All repositories** | 权限最小化。GitHub REST 文档明确列出 `GET /user/starred` 需要 `Starring` 的 read 权限；`Metadata` 是读取仓库基础信息所必需 |

**fine-grained 的实测结论（重要）**：它的 Resource owner **只能选一个账号**。
选了个人 `suzike` 的令牌，`GET /repos/suzike-dev/xxx` 对组织 `suzike-dev` 名下
的私有仓一律返回 **404**，结果就是 76 个 Star 只读到 65 个——少的恰好是那 11 个
组织私有仓。这不是权限勾错了，是令牌作用域的硬限制，靠改权限解决不了。
解法见下一节 `STAR_TOKEN_ORG`。

### 自检（配置后务必先跑这一步）

```bash
python scripts/sync_stars.py --verify-token
```

输出会列出：可见的 Star 总数、其中私有仓库的数量与名称。**如果私有仓库数量是 0 而你确实 Star 过私有仓库，说明 token 权限不足**，同步会静默漏掉它们。

### 创建步骤

1. 打开 https://github.com/settings/tokens
2. 按上表选择 classic 或 fine-grained，勾选对应权限
3. 有效期按需选择（建议 90 天，到期后重新生成并更新 Secret）
4. 生成后立刻复制，token 只显示一次

### 写入仓库

仓库页面 → **Settings** → **Secrets and variables** → **Actions** → **New repository secret**

| Name | Value |
|---|---|
| `STAR_TOKEN` | 上一步生成的 token |

---

## 一之二、`STAR_TOKEN_ORG` —— 组织名下的私有仓库（可选）

**什么时候需要**：你有 Star 的私有仓库属于某个**组织**（例如 `suzike-dev`），
而主令牌的 Resource owner 是个人账号。

**为什么必须再来一个**：fine-grained PAT 的 Resource owner 只能选一个账号，
选了个人就看不见组织的私有仓（见上一节实测）。要两边都覆盖，只能再建一个
Resource owner 为该组织的令牌，脚本会把两份结果按仓库名合并。

### 创建步骤

1. https://github.com/settings/tokens → **Generate new token (fine-grained)**
2. **Resource owner** 选你的**组织**（不是个人账号）
3. Repository access 选 **All repositories**
4. Permissions → Account: **Starring → Read**；Repository: **Metadata → Read**
5. 写入 Secret：

| Name | Value |
|---|---|
| `STAR_TOKEN_ORG` | 该组织令牌 |

> 不配也能跑：此时只同步主令牌看得见的仓库。组织私有仓若**已经在**归档里，
> 脚本会保留它们并在日志里告警，**不会**因为读不到就当成取消星标删掉。
> 影响的只是「以后新 Star 的组织私有仓不会自动进来」。

---

## 二、`LLM_API_KEY` —— 生成中文归类与解读

归档中每一条的「这是什么」和「什么时候用得上」都由大模型生成。脚本使用 OpenAI 兼容的 `chat/completions` 接口，因此任何兼容该协议的服务都能用。

### 以 DeepSeek 为例

1. 打开 https://platform.deepseek.com/api_keys
2. 创建 API key 并复制

### 写入仓库

同上路径，新增一个 Secret：

| Name | Value |
|---|---|
| `LLM_API_KEY` | 你的 DeepSeek API key |

> **不配也能跑。** 缺少该 key 时脚本自动降级为规则归类 + GitHub 官方描述，流程完整可用，
> 只是归类质量明显下降、描述多为英文。拿到 key 后跑一次 `--reanalyze-all` 即可整体重做。

---

## 三、可选配置（Repository Variables）

不需要的话可以完全不设置，脚本内置了默认值。

仓库页面 → **Settings** → **Secrets and variables** → **Actions** → **Variables** 标签页 → **New repository variable**

| Name | 默认值 | 说明 |
|---|---|---|
| `LLM_BASE_URL` | `https://api.deepseek.com` | 换用其他服务时改这里，例如 `https://api.moonshot.cn/v1` |
| `LLM_MODEL` | `deepseek-chat` | 模型名 |
| `LLM_BATCH` | `8` | 每次请求处理多少个仓库。调小可降低单次失败的影响面 |

改用其他服务只需设置这两个变量，代码无需改动：

| 服务 | `LLM_BASE_URL` | `LLM_MODEL` |
|---|---|---|
| DeepSeek | `https://api.deepseek.com` | `deepseek-chat` |
| 月之暗面 Kimi | `https://api.moonshot.cn/v1` | `moonshot-v1-8k` |
| 阿里通义 | `https://dashscope.aliyuncs.com/compatible-mode/v1` | `qwen-plus` |
| OpenAI | `https://api.openai.com/v1` | `gpt-4o-mini` |

---

## 四、首次启用

Secret 配好之后：

1. 进入 **Actions** 标签页
2. 左侧选择 **同步 Star 归档**
3. 点击 **Run workflow**
4. `force_reanalyze` **不要勾**（原因见下）
5. 运行完成后，README 会自动更新并提交

之后**每小时**自动同步一次（cron 定在每小时第 17 分钟，避开整点排队高峰），
点完星标最迟一小时内就会出现在归档里，无需干预。

**为什么做不到「点完立刻更新」**：GitHub 没有提供「用户 star 了某个仓库」的
webhook 事件（`watch` 事件只在别人 star 你的仓库时触发），所以拿不到事件驱动，
只能轮询。每小时是 GitHub 定时任务下比较稳妥的频率上限。

想立刻看到结果，可以手动跑：仓库 **Actions** → **同步 Star 归档** →
**Run workflow**。

**无变化时不会产生提交**：脚本会比较运行前后的数据，只有当收录内容真的变了
才推进 `last_sync` 并提交。否则每小时都会多出一个只差时间戳的噪音 commit。

### 为什么首次不要勾 `force_reanalyze`

`force_reanalyze` 会**无视缓存，对全部条目重新调用一次大模型**（当前 76 条）。
现有 `data/stars.json` 里已经写好了每条的中文解读，标记为 `analyzed_by: bootstrap`。
脚本判定「需要重新解读」的条件是 `what` 为空，或 `analyzed_by == "rule"`
（即上一次是关键词兜底）。`bootstrap` 不满足这两个条件，因此正常同步不会重做它们——
勾上反而会白花 76 次调用。

只有在这两种情况下才需要勾：

- 换了模型或改了归类标准，想整体重做一遍；
- 此前的解读确认是规则兜底的，想替换成模型输出。

也可以只重做单条：本地把该条的 `analyzed_by` 改成 `"rule"`，下次同步会单独重做。

### 两条凭据缺失时的行为差异

| 缺失的 Secret | 行为 |
|---|---|
| `STAR_TOKEN` | 工作流第一步输出 **warning** 并**跳过整个任务**，不会失败。这是为了避免在还没配好凭据时每天收到失败通知 |
| `LLM_API_KEY` | 任务照常运行，但输出一条 **notice**，归类退化为关键词规则、解读退化为 GitHub 官方描述。**此时仍然会正常提交 README**，容易误以为「AI 归类已经生效」 |
| `STAR_TOKEN_ORG` | 任务照常运行，只在日志里输出「N 个私有仓库读不到，已保留」。后果是**以后新 Star 的组织私有仓不会自动进来** |

### 判断自动化是否真的在跑

**不要看 run 的 conclusion。** 凭据缺失时工作流第一步会输出 warning 并跳过
后续全部步骤，但 **job 仍以 success 结束**——实测连续 10 次运行全部显示
success，`last_sync` 却 10 天没变过。这个「跳过不算失败」的设计避免了每天
发失败邮件，代价是故障从运行状态里看不出来。

唯一可靠的指标是 `data/stars.json` 的 **`last_sync` 是否随运行时间更新**。

---

## 五、本地运行

想在本机验证而不动仓库：

```bash
# Windows PowerShell
$env:STAR_TOKEN = "你的 token"
$env:STAR_TOKEN_ORG = "组织令牌（可选）"
$env:LLM_API_KEY = "你的 key"
python scripts/sync_stars.py
```

常用参数：

| 参数 | 作用 |
|---|---|
| `--verify-token` | 只检查 token 能读到什么，特别是私有仓库是否可见 |
| `--check-publishable` | 只校验 `data/stars.json` 是否只含可公开字段，不写任何文件 |
| `--dry-run` | 只打印流程，不写任何文件 |
| `--no-llm` | 强制规则归类，用于验证流程连通性（不消耗 API 额度） |
| `--limit N` | 本次最多处理 N 条，便于小批量试跑 |
| `--render-only` | 跳过网络请求，仅用本地数据重新渲染 README **与 `assets/` 下的分布图** |
| `--reanalyze-all` | 强制全部重新解读（需要 LLM key） |

完整校验（CI 与本地同一套）：

```bash
python scripts/validate_render.py
```

---

## 六、常见问题

**同步后 README 没变化？**
说明 Star 列表没有变动，或 `data/stars.json` 已是最新。Actions 日志里会打印「新增 / 待补充解读 / 已取消星标」三项计数。

**私有仓库没出现在归档里？**
先跑 `--verify-token`。绝大多数情况是 token 权限不足，读不到私有仓库。

**模型输出被降级成官方描述了？**
说明 LLM 调用失败，脚本会自动降级并继续，不会中断整个同步。查看 Actions 日志中 `LLM 调用失败，本批降级处理` 那一行。这些条目在下次运行时会被自动重试（`analyzed_by` 字段会留在 `stars.json` 里）。

**换了模型想重新生成全部解读？**
在 Actions 里手动触发并把 `force_reanalyze` 勾上，或本地跑 `python scripts/sync_stars.py --reanalyze-all`。

**取消 Star 之后条目还在？**
不会。脚本会把该条目标记为 `starred_active: false` 并从 README 中移除，但保留在 `stars.json` 里——这样你重新 Star 时不必再花一次模型调用。

**Star 数量很多，一次调用处理得完吗？**
脚本按 `LLM_BATCH`（默认 8）分批，批次之间会 sleep 1 秒。日常每天新增通常只有几条，额度消耗很低。

---

## 七、边界与隐私

本仓库是**公开仓库**，`publish_private: true`。边界按「公开什么 / 不公开什么」分成两层，两层都是代码级硬约束。

### 公开的部分：元数据

私有仓库在 README 中以**名称、描述、链接、星数、语言**形式列出，并带 `私有` 标记。
这些是基本信息，也是明确选择公开的部分。链接对无权限的访问者会返回 404。

### 不公开的部分：仓库内容

**脚本从不读取、也从不写入任何仓库内容。** 具体保证方式：

1. **接口层**：`STAR_QUERY` 只请求 Star 列表的元数据字段（`nameWithOwner`、`description`、
   `stargazerCount`、`primaryLanguage`、`repositoryTopics` 等），
   请求体中没有任何 content / object / blob / raw 字段。
   脚本的全部网络调用只有两类：GitHub GraphQL（读 Star 元数据）与 LLM 接口（生成解读文本）。

2. **写入层**：可提交字段由 `PUBLISHABLE_FIELDS` 白名单强制约束。
   每次写盘前调用 `assert_publishable()`，出现白名单以外的字段会直接报错退出。
   若新增字段名中含有 `readme` / `content` / `file` / `blob` / `code` 等词，
   报错信息会单独点名。这意味着任何字段扩展都被迫经过一次「能不能公开」的判断。

3. **可见性层**：脚本对仓库可见性**没有任何写操作**。
   你的私有仓库不会因为本工具变成公开仓库。

4. **产物层**：概览图在设计上只接收聚合数据（分类名与计数、语言名、颜色），
   函数签名里根本没有传入单个仓库的入口。这条边界另有机械校验兜底——
   `validate_render.py` 会读取两张 SVG，逐个比对全部活跃条目的名称与描述，
   命中任意一个即判定失败。校验通过时会打印实际比对的字符串数量，
   避免「看起来有校验、其实没跑」。

### 如何自查

```bash
python scripts/sync_stars.py --check-publishable   # 字段白名单
python scripts/validate_render.py                  # 六项校验（含概览图聚合边界）
```

CI 每次同步都会跑 `validate_render.py`，边界被突破时工作流直接失败，不会提交。

### 想改回「私有仓库完全不列出」

编辑 `data/config.json`，把 `publish_private` 改为 `false`，再跑一次同步。
此时私有仓库会被**同时**从 README.md 与 `data/stars.json` 中剔除——
只在渲染时过滤是不够的，因为 `data/stars.json` 同样会被提交。

> 注意历史残留：如果私有仓库信息曾经进入过 Git 提交历史，改配置无法撤回它。
> 需要重写历史（本地未推送时直接重建 `.git` 最简单）。

---

## 八、README 的构成与生成物

README 全部由脚本生成，**没有任何一段是手工写的**。改样式必须改渲染代码，
直接编辑 README.md 会在下次同步时被覆盖。

### 页面结构

| 区块 | 生成位置 | 说明 |
|---|---|---|
| 概览卡 | `render_overview.py` | 一张 SVG 里放三段：指标行（收录数/分类数/自研数/私有数）+ 分类分布条形 + 语言分布胶囊。浅色/深色两版 |
| 目录 | `render_readme()` | HTML 表格，两列并排，11 个分类压到 6 行 |
| 最近加入 | `render_readme()` | 按 `starred_at` 倒序取前 5 条，列出分类、语言与星标日期 |
| 分类正文 | `render_readme()` | 每条 3 行：名称 + 状态标记 + 淡灰元信息 / 这是什么 / 什么时候用 |
| 我的自研项目 | `render_readme()` | `self_owners` 名下仓库的快捷索引，双列排布 |
| 运行状态 | `render_readme()` | 放在页脚 `<details>` 里的折叠区，含 Actions 动态徽章与最后同步时间 |

### 概览卡的几条视觉规则

都是有意为之，改动前先读一遍：

- **条形色深按「数值」映射，不是按「排名」。** 计数相同的两行必须同色，
  否则颜色会承载一个它并不代表的含义（同为 7 的两类深浅不同，会被读成两类有差别）。
  长度和色深是同一个数字的两种表达。
- **语言胶囊带圆点，色值取自 GitHub Linguist 官方定义**（`data/language_colors.json`，
  从 `github/linguist` 的 `languages.yml` 提取）。语言色是行业约定色，属语义色，
  不是装饰色；圆点直径仅 7px，视觉重量低到不会与主图争注意力。
  深色主题下暗色语言（如 C 的 `#555555`）会看不见，所以圆点带一圈极淡描边。
- **「未标注」排在语言列表最后，且用中性灰圆点。** 它不是一种语言，
  按计数混排会让人误读成第三大技术栈。
- **卡片宽度固定为 850px。** 实测 GitHub 仓库首页的 README 正文栏宽在 840～860px
  之间，且**不随浏览器窗口变宽而变宽**（1920px 窗口下实测 839px，1280px 窗口下 854px）。
  取中值让卡片在各种窗口下都正好铺满、且几乎不缩放。

设计上另有两条成文的否决项：

- **不用 shields.io 做静态数值徽章。** 早先版本顶部有 4 个静态徽章 + 1 个动态徽章，
  结果是收录数在徽章、概览图、页脚三处各出现一次，顶部还并排着 5 个颜色互不相干的
  小色块互相抢注意力。现在静态数值统一交给概览卡，只有「同步是否还活着」留在页脚，
  因为那一项必须用动态徽章。
- **目录不用 `████` 方块字符做占比条。** 方块的颜色继承正文字色，无法控制；不同平台的
  方块字形宽度也不一致，条目一多就参差不齐。改用双列表格后既省一半高度，也没有对齐问题。

### `assets/` 是生成物

`assets/overview-light.svg` 与 `assets/overview-dark.svg` 每次渲染都会重新生成，
由 `write_overview_assets()` 写出，并在工作流里随 README 一起提交。
**不要手工编辑**，下次同步会覆盖。

`data/language_colors.json` 是唯一的例外——它**不是生成物**，是手工维护的静态配置：
语言名 → 官方色值的映射表，供概览卡的语言圆点取色。色值取自 GitHub Linguist 的
`lib/linguist/languages.yml`（用 `gh api -H "Accept: application/vnd.github.raw"
repos/github/linguist/contents/lib/linguist/languages.yml` 拉取后解析）。
想调整某个语言的颜色，直接改这个文件即可；表里没有的语言会回退为中性灰圆点，
文件缺失或格式异常也不会让同步失败。

README 里用 `<picture>` 引用这两份图，让 GitHub 跟随用户主题自动切换：

```html
<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/overview-dark.svg">
  <img alt="收藏概览：收录总数、分类分布与语言分布" src="assets/overview-light.svg">
</picture>
```

实测 GitHub 会原样保留这段结构，图片走仓库 raw 路径（不经 camo 代理），
因此更新后立即可见，不存在缓存滞后。

### 为什么自己画 SVG

- 分布信息（11 个分类的相对占比）徽章服务表达不了，需要真正的条形图。
- 自绘 SVG 无外部依赖、无网络请求、矢量清晰，样式完全可控。
- 想把图换成别的形式，只改 `scripts/render_overview.py` 即可，
  `sync_stars.py` 只负责传「标签 + 计数」，不关心画法。
- 渲染层只接收「标签 + 计数」与「语言名 → 颜色」两种输入，不接触任何单个仓库的数据。
  这条边界由 `validate_render.py` 的第 5 条检查兜底。

### 目录表格的列宽为什么写像素值

GitHub 的表格是 `width:100%` + `table-layout:auto`，百分比列宽只作为建议值参与分配，
实测会被内容比例带偏——右列的「Agent 扩展、Skills 与工具协议」被压到容不下，
在线上折成了两行。改成 `width="320"` / `width="60"` 后，分类名列拿到明确的最小宽度，
不再折行。

### 本地预览的局限（重要）

`_work/make_preview2.py` 那套做法是「用 GitHub 的 `/markdown` 接口渲染 + 套一层
github-markdown-css」，它能反映 GitHub 对 Markdown 和 HTML 的**解析与清洗**结果，
但**不能**反映线上真实的 CSS 布局。

已经踩过一次：`github-markdown-css` 里表格是 `display:block; width:max-content`，
表格只按内容宽度撑开；而 GitHub 线上是 `width:100%`，表格铺满正文栏。
两者行为不同，曾据此得出「目录表格没占满」的错误结论，并差点把表格改成列表。
预览脚本里已经覆盖回接近线上的行为，但**表格类版式的最终判断必须抓线上页面截图**：

```bash
chrome --headless=new --screenshot=out.png --window-size=1280,1500 \
       --virtual-time-budget=25000 https://github.com/<user>/<repo>
```

无头浏览器默认取 `prefers-color-scheme: dark`，所以抓到的页面会渲染深色版图表——
这正好也顺带验证了 `<picture>` 的主题切换确实生效。

### 改了渲染逻辑之后

本地先跑一遍再提交，两条命令即可完成验证：

```bash
python scripts/sync_stars.py --render-only   # 重新生成 README 与 assets/
python scripts/validate_render.py            # 六项校验，见下
```

`validate_render.py` 会检查六件事：

1. 字段白名单（没有内容型字段进入会被提交的文件）
2. 每个活跃条目都出现在 README 里（防渲染漏项）
3. README 中 `私有` 标记数与数据层口径一致
4. 概览图既存在于磁盘、又被 README 引用（防裂图）
5. **概览图里没有出现任何单个仓库的名称或描述**（防聚合图泄漏具体条目）
6. 语言色表的色值都是合法十六进制（防圆点静默消失）

第 5、6 条是为了让「概览图只承载聚合信息」这条设计承诺有代码级保证，
而不只是注释里的约定。输出里会打印实际扫描过的 SVG 数与比对的字符串数，
这样「静默通过」和「因路径写错而根本没执行」可以区分开。

CI 每次同步都会跑这套校验，不通过则不会提交。
