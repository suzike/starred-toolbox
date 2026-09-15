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
| **classic PAT** | `repo` | 本地实测可用（本机 `gh` 的 token 含 `repo` + `workflow`，成功读到全部 65 个 Star，含 10 个私有仓）。但 `repo` 是较宽的权限，会给到私有仓库的读写能力 |
| **fine-grained PAT**（推荐） | Account permissions: **Starring → Read**；Repository permissions: **Metadata → Read**，仓库范围选 **All repositories** | 权限最小化。GitHub REST 文档明确列出 `GET /user/starred` 需要 `Starring` 的 read 权限；`Metadata` 是读取仓库基础信息所必需 |

两点诚实标注：

- **本机没有独立的 fine-grained token 可测，所以「fine-grained 一定能读到私有仓库」我无法在此确认。** 配置完后请跑一次下面的自检命令验证，不要直接假定成功。
- 关于只有 `read:user`（不含 `repo`）的 classic token 能否看到私有仓库，我未能找到可引用的官方明确表述，也无法在本机验证。**不要在需要私有条目时这样配**。

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
4. 把 `force_reanalyze` 勾上（首次运行需要，用来把已有的占位解读替换成模型输出）
5. 运行完成后，README 会自动更新并提交

之后每天 UTC 22:00（北京时间早 6:00）自动同步，无需干预。

> **未配置 `STAR_TOKEN` 时，定时任务会跳过而不是失败。** 工作流第一步会检查凭据，
> 缺失时输出一条 warning 并结束，避免每天发送失败通知。

---

## 五、本地运行

想在本机验证而不动仓库：

```bash
# Windows PowerShell
$env:STAR_TOKEN = "你的 token"
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
| `--render-only` | 跳过网络请求，仅用本地数据重新渲染 README |
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

### 如何自查

```bash
python scripts/sync_stars.py --check-publishable   # 字段白名单
python scripts/validate_render.py                  # 渲染一致性 + 白名单
```

CI 每次同步都会跑 `validate_render.py`，边界被突破时工作流直接失败，不会提交。

### 想改回「私有仓库完全不列出」

编辑 `data/config.json`，把 `publish_private` 改为 `false`，再跑一次同步。
此时私有仓库会被**同时**从 README.md 与 `data/stars.json` 中剔除——
只在渲染时过滤是不够的，因为 `data/stars.json` 同样会被提交。

> 注意历史残留：如果私有仓库信息曾经进入过 Git 提交历史，改配置无法撤回它。
> 需要重写历史（本地未推送时直接重建 `.git` 最简单）。
