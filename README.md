# Starred Toolbox

> 我在 GitHub 星标的工具与资源归档。收录来源只有一个：**我的 Star**。
> 未经星标的内容不会出现在这里；归类与解读由脚本自动生成。

<sub>10 个私有仓库仅公开名称、描述与链接等基本信息，代码与文件内容不对外释放，点击链接需要对应的访问权限。</sub>

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="assets/overview-dark.svg">
  <img alt="收藏概览：收录总数、分类分布与语言分布" src="assets/overview-light.svg">
</picture>

## 目录

<table width="100%">
<tr><td width="320"><a href="#ai-agent-与编码智能体">AI Agent 与编码智能体</a></td><td width="60" align="right">28</td><td width="320"><a href="#agent-扩展skills-与工具协议">Agent 扩展、Skills 与工具协议</a></td><td width="60" align="right">37</td></tr>
<tr><td width="320"><a href="#知识库rag-与记忆">知识库、RAG 与记忆</a></td><td width="60" align="right">12</td><td width="320"><a href="#matlab-simulink-与基于模型的设计">MATLAB / Simulink 与基于模型的设计</a></td><td width="60" align="right">8</td></tr>
<tr><td width="320"><a href="#汽车电子车载测试与控制">汽车电子、车载测试与控制</a></td><td width="60" align="right">9</td><td width="320"><a href="#内容创作与多媒体生成">内容创作与多媒体生成</a></td><td width="60" align="right">16</td></tr>
<tr><td width="320"><a href="#信息聚合与效率工具">信息聚合与效率工具</a></td><td width="60" align="right">19</td><td width="320"><a href="#编程学习与计算机基础">编程学习与计算机基础</a></td><td width="60" align="right">21</td></tr>
<tr><td width="320"><a href="#机器学习与深度学习框架">机器学习与深度学习框架</a></td><td width="60" align="right">6</td><td width="320"><a href="#工程方法论与研发流程">工程方法论与研发流程</a></td><td width="60" align="right">2</td></tr>
<tr><td width="320"><a href="#其他">其他</a></td><td width="60" align="right">8</td><td width="320"></td><td width="60"></td></tr>
</table>

<sub>另有 [我的自研项目](#我的自研项目) 快捷索引，共 23 个。</sub>

## 最近加入

| 仓库 | 分类 | 语言 | 星标于 |
| :--- | :--- | :--- | ---: |
| [Tianyu199509/DeskBox](https://github.com/Tianyu199509/DeskBox) | 信息聚合与效率工具 | C# | 2026-11-12 |
| [agentes-chat/agentes-chat](https://github.com/agentes-chat/agentes-chat) | AI Agent 与编码智能体 | TypeScript | 2026-11-12 |
| [UniXNU/UniXNU](https://github.com/UniXNU/UniXNU) | 其他 | Python | 2026-11-11 |
| [jackwener/Kaze](https://github.com/jackwener/Kaze) | 信息聚合与效率工具 | JavaScript | 2026-11-11 |
| [pingdotgg/t3code](https://github.com/pingdotgg/t3code) | 其他 | TypeScript | 2026-11-10 |

## AI Agent 与编码智能体

<sub>28 个 · [返回目录](#目录)</sub>

- **[deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)** <sub>TypeScript · ★ 281k</sub>
  插件化的 DeepSeek 智能体运行时，一切能力皆以插件形式接入。
  <sub>想基于 DeepSeek 模型搭建可扩展的编码智能体时。</sub>
- **[Significant-Gravitas/AutoGPT](https://github.com/Significant-Gravitas/AutoGPT)** <sub>Python · ★ 188k</sub>
  可自主拆解并执行任务的开源 AI 智能体框架。
  <sub>想研究自主 Agent 的早期实现思路时。</sub>
- **[stablyai/orca](https://github.com/stablyai/orca)** <sub>TypeScript · ★ 124.8k</sub>
  多编码智能体编排平台，可在桌面、移动与远程运行多个 Agent。
  <sub>需要同时调度 Claude Code 等多个编码 Agent 并统一管理时。</sub>
- **[OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)** <sub>TypeScript · ★ 93.5k</sub>
  可自主完成编码、调试与多步开发任务的 AI 智能体平台。
  <sub>需要让 AI 独立接手开发任务、减少人工逐步操作时。</sub>
- **[666ghj/MiroFish](https://github.com/666ghj/MiroFish)** <sub>Python · ★ 85.6k</sub>
  通用群体智能引擎，用于多主体行为建模与预测。
  <sub>需要做群体行为仿真或预测类建模时。</sub>
- **[alibaba/open-code-review](https://github.com/alibaba/open-code-review)** <sub>Go · ★ 51.2k</sub>
  结合确定性流水线与 LLM Agent 的代码审查工具，支持行级评论与多语言规则集。
  <sub>需要在 CI 或本地对仓库做自动化代码审查并定位具体代码行时。</sub>
- **[THU-MAIC/OpenMAIC](https://github.com/THU-MAIC/OpenMAIC)** <sub>TypeScript · ★ 43.5k</sub>
  多智能体驱动的交互式课堂，一键生成沉浸式学习体验。
  <sub>关注多智能体在教育场景如何落地时。</sub>
- **[codewhale-hq/Codewhale](https://github.com/codewhale-hq/Codewhale)** <sub>Rust · ★ 41.2k</sub>
  用 Rust 编写的开源终端编码智能体，支持多模型与多智能体编排。
  <sub>需要在本地终端运行、可自行部署并接入自有模型的编码 Agent 时。</sub>
- **[can1357/oh-my-pi](https://github.com/can1357/oh-my-pi)** <sub>TypeScript · ★ 39k</sub>
  集成 IDE 能力的终端编码智能体，支持多模型提供商与 MCP。
  <sub>需要在终端里用自有订阅驱动编码 Agent 并接入编辑器时。</sub>
- **[deepseek-ai/dsh-superagent-prototype](https://github.com/deepseek-ai/dsh-superagent-prototype)** <sub>TypeScript · ★ 23.1k</sub>
  面向更自主智能体系统的原型实现，探索多步任务自主执行能力。
  <sub>需要研究或参考自主 Agent 系统架构设计时。</sub>
- **[milind-soni/OpenMausBot](https://github.com/milind-soni/OpenMausBot)** <sub>TypeScript · ★ 22.6k</sub>
  开源自托管的 AI 智能体平台，为机器人提供可操作的虚拟机环境。
  <sub>需要自建可让智能体在虚拟机中执行计算机操作任务的环境时。</sub>
- **[ccch1mneyyy/dsh-Go](https://github.com/ccch1mneyyy/dsh-Go)** <sub>Dart · ★ 22.6k</sub>
  将 DeepSeek Harness 编码智能体移植到手机端运行的 Flutter 应用。
  <sub>需要在手机上运行编码 Agent 或远程操控电脑上的 Agent 时。</sub>
- **[AndyMik90/Aperant](https://github.com/AndyMik90/Aperant)** <sub>TypeScript · ★ 14.6k</sub>
  支持跨多个会话自主推进任务的 AI 编码智能体。
  <sub>需要 Agent 在长周期任务上持续工作、而不是单轮对话时。</sub>
- **[CopilotKit/OpenBot](https://github.com/CopilotKit/OpenBot)** <sub>TypeScript · ★ 12.2k</sub>
  开源 AI 同事系统，每个智能体拥有独立浏览器、文件与工具环境。
  <sub>需要让智能体在隔离环境中自主操作浏览器和文件执行多步任务时。</sub>
- **[zai-org/ZCode](https://github.com/zai-org/ZCode)** <sub>TypeScript · ★ 8.7k</sub>
  Z.ai 推出的编码智能体运行框架，支持扩展。
  <sub>需要接入或试用 Z.ai 的编码 Agent 能力时。</sub>
- **[wangzan101/Mika](https://github.com/wangzan101/Mika)** <sub>Kotlin · ★ 8.6k</sub>
  运行在 Android 手机上的端侧 AI 智能体，可自动操作 App 与网页完成任务。
  <sub>需要在手机上让 AI 代为操作应用、处理跨 App 任务时。</sub>
- **[vastsa/PI-Desktop](https://github.com/vastsa/PI-Desktop)** <sub>TypeScript · ★ 8k</sub>
  本地优先的 AI 编码智能体桌面应用，含 Rust 核心与可安装插件。
  <sub>希望在本机运行可扩展、数据不外传的编码 Agent 桌面端时。</sub>
- **[Fei2411/DS-Bot](https://github.com/Fei2411/DS-Bot)** <sub>JavaScript · ★ 7.7k</sub>
  面向 DeepSeek Harness 的长期运行多机器人团队，支持机器人互发消息与群聊。
  <sub>想搭建多个长期在线、可互相协作对话的机器人时。</sub>
- **[nightly-labs/openbot](https://github.com/nightly-labs/openbot)** <sub>TypeScript · ★ 7.7k</sub>
  本地优先的桌面工作台，为多个编码智能体提供独立工作区、任务队列与协作。
  <sub>需要在本机同时运行并调度 Codex、Claude 等多个智能体协同完成任务时。</sub>
- **[KunAgent/Kun](https://github.com/KunAgent/Kun)** <sub>TypeScript · ★ 6.4k</sub>
  本地优先的 AI 智能体工作台，覆盖编码、写作、设计与研究，统一 GUI 与 TUI 运行时。
  <sub>想要一个统一入口承载多种 Agent 任务、且数据留在本机时。</sub>
- **[nano-muse/nanoMuse](https://github.com/nano-muse/nanoMuse)** <sub>Swift · ★ 3.5k</sub>
  跨手机、桌面与浏览器的开源个人智能体，可执行任务并保留记忆。
  <sub>想要一个跨设备运行、能记住你并在不可逆操作前确认的个人 Agent 时。</sub>
- **[agentes-chat/agentes-chat](https://github.com/agentes-chat/agentes-chat)** <sub>TypeScript · ★ 1.4k</sub>
  可自托管的团队聊天平台，人类与多个 AI Agent 在频道和私信中协作。
  <sub>希望团队与接入 MCP 工具的 AI Agent 在同一聊天环境协同工作时。</sub>
- **[zqiren/Orbital](https://github.com/zqiren/Orbital)** <sub>Python · ★ 986</sub>
  面向自主智能体的编排与管理框架，强调上下文归用户所有、智能体可替换。
  <sub>需要搭建多智能体协作系统并自行掌控上下文与记忆时。</sub>
- **[abcwyc/pi-agent-desktop](https://github.com/abcwyc/pi-agent-desktop)** <sub>TypeScript · ★ 923</sub>
  跨平台桌面端 AI 编码智能体，无需配置环境或使用终端命令即可开始编码。
  <sub>希望以桌面应用形式使用编码 Agent、不想折腾命令行环境时。</sub>
- **[sandroandric/AgentHandover](https://github.com/sandroandric/AgentHandover)** <sub>Python · ★ 703</sub>
  观察用户操作习惯，转成可自改进的技能并交接给编码智能体。
  <sub>想让 Agent 学会你的固定工作方式、不必每次重复交代时。</sub>
- **[yicheng47/runner](https://github.com/yicheng47/runner)** <sub>Rust · ★ 518</sub>
  在真实终端中让多个编码智能体协作完成同一任务的编排工具。
  <sub>希望同时调度 Claude Code、Codex 等多个编码 Agent 处理同一任务时。</sub>
- **[suzike/agentic-island](https://github.com/suzike/agentic-island)** `自研` <sub>TypeScript · ★ 13</sub>
  常驻 Windows 顶部的 AI 编码智能体监控与审批面板，兼作个人工作台。
  <sub>想让多个 Agent 的运行状态与待审批请求集中可见时。</sub>
- **[suzike-dev/IntentOS](https://github.com/suzike-dev/IntentOS)** `私有` `自研` <sub>Python · ★ 1</sub>
  规范驱动的嵌入式研发平台，含多 Agent 协作与门禁治理。
  <sub>想用 Spec 驱动方式组织嵌入式软件研发流程时。</sub>

## Agent 扩展、Skills 与工具协议

<sub>37 个 · [返回目录](#目录)</sub>

- **[morluto/rea](https://github.com/morluto/rea)** <sub>TypeScript · ★ 459.2k</sub>
  为 Agent 提供逆向工程能力的工具集，可分析应用行为与原生二进制文件。
  <sub>需要让编码 Agent 借助 Ghidra 等工具做二进制反汇编与静态分析时。</sub>
- **[mattpocock/skills](https://github.com/mattpocock/skills)** <sub>Shell · ★ 324.3k</sub>
  作者从个人 .agents 目录整理出的面向工程师的 Agent Skills 集合。
  <sub>想参考他人实际使用的编码 Agent 技能配置时。</sub>
- **[affaan-m/ECC](https://github.com/affaan-m/ECC)** <sub>JavaScript · ★ 302.8k</sub>
  为 Claude Code、Codex 等编码智能体提供技能、记忆与安全扩展的优化框架。
  <sub>需要给现有编码 Agent 补充技能、记忆与安全约束时。</sub>
- **[DietrichGebert/ponytail](https://github.com/DietrichGebert/ponytail)** <sub>JavaScript · ★ 190.7k</sub>
  让 AI 编码代理遵循 YAGNI、少写代码的 Agent 技能插件。
  <sub>希望代理减少冗余代码、避免过度设计时。</sub>
- **[nextlevelbuilder/ui-ux-pro-max-skill](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill)** <sub>Python · ★ 149.4k</sub>
  为 AI 代理提供多平台专业 UI/UX 设计能力的技能。
  <sub>让编码代理生成界面时具备设计规范与布局能力时。</sub>
- **[addyosmani/agent-skills](https://github.com/addyosmani/agent-skills)** <sub>JavaScript · ★ 117.4k</sub>
  面向 AI 编码智能体的生产级工程技能集合。
  <sub>想给 Agent 补上成熟工程实践、减少低级失误时。</sub>
- **[Leonxlnx/taste-skill](https://github.com/Leonxlnx/taste-skill)** <sub>JavaScript · ★ 115.5k</sub>
  用于约束 AI 生成内容风格、避免通用化设计的 Agent 技能。
  <sub>觉得代理产出的前端设计千篇一律、想改善审美时。</sub>
- **[cathrynlavery/diagram-design](https://github.com/cathrynlavery/diagram-design)** <sub>HTML · ★ 67k</sub>
  面向多种编码 Agent 的图表设计技能集，输出自包含 HTML 与 SVG 图。
  <sub>想让编码 Agent 按统一风格生成架构图或数据可视化时。</sub>
- **[yetone/magpie](https://github.com/yetone/magpie)** <sub>Go · ★ 36.5k</sub>
  在 macOS 菜单栏为编码 Agent 切换与配置不同大模型后端的工具。
  <sub>想让 Codex、Claude Code 等 Agent 接入 DeepSeek、Kimi 等模型时。</sub>
- **[alchaincyf/huashu-design](https://github.com/alchaincyf/huashu-design)** <sub>HTML · ★ 29.5k</sub>
  面向编码 Agent 的 HTML 原生设计技能，可生成网页、原型、PPTX 与信息图。
  <sub>需要在 Claude Code、Cursor 等 Agent 中直接产出可交付设计稿时。</sub>
- **[wheresryan22/anatomy](https://github.com/wheresryan22/anatomy)** <sub>JavaScript · ★ 27.3k</sub>
  将技术构想转为可交互等距机械图的 Claude Code 技能，输出 SVG 与可选 WebGL 着色器。
  <sub>需要为文档、文章或落地页快速生成机械结构示意图时。</sub>
- **[vercel-labs/agent-desktop](https://github.com/vercel-labs/agent-desktop)** <sub>Rust · ★ 23.7k</sub>
  让 AI Agent 通过命令行调用桌面无障碍接口操作 macOS 应用的计算机使用工具。
  <sub>需要让 Agent 自动化操作桌面软件或构建桌面自动化流程时。</sub>
- **[citrolabs/ego-lite](https://github.com/citrolabs/ego-lite)** <sub>JavaScript · ★ 22.9k</sub>
  为 AI 智能体提供浏览器自动化能力的工具，可共享已登录的浏览器状态。
  <sub>需要让 Codex 或 Claude Code 等智能体操作浏览器且不影响自己正常使用时。</sub>
- **[HKUSTDial/Supervisor-Skills](https://github.com/HKUSTDial/Supervisor-Skills)** <sub>Python · ★ 12.5k</sub>
  将科研指导经验封装为可调用 AI 技能，覆盖选题到论文投稿流程。
  <sub>需要按步骤推进科研选题、写作与投稿时，可调用这套技能辅助。</sub>
- **[dsh-market/dsh-market](https://github.com/dsh-market/dsh-market)** <sub>TypeScript · ★ 12.4k</sub>
  DeepSeek Harness 的可视化插件市场，支持浏览、搜索与一键安装插件。
  <sub>需要为 DeepSeek Harness 查找并安装插件、扩展其能力时。</sub>
- **[jakubkrehel/skills](https://github.com/jakubkrehel/skills)** <sub>Markdown · ★ 12.2k</sub>
  一组用于辅助构建界面设计的 Agent Skills 集合。
  <sub>让编码 Agent 按规范产出界面代码或设计稿时使用。</sub>
- **[Tencent/BrowserSkill](https://github.com/Tencent/BrowserSkill)** <sub>TypeScript · ★ 10.4k</sub>
  让 AI Agent 使用真实已登录浏览器的 CLI 与扩展工具。
  <sub>希望 Agent 在后台自动化浏览器而不打断当前工作时。</sub>
- **[Jakeschincariol/replica-skill](https://github.com/Jakeschincariol/replica-skill)** <sub>Python · ★ 9.3k</sub>
  一套面向 Claude 的 Agent Skills 集合，用于逆向分析、重建并测试现有应用。
  <sub>想让编码 Agent 按固定流程复刻某个应用或排查其缺陷时。</sub>
- **[yang0/handraw-style](https://github.com/yang0/handraw-style)** <sub>HTML · ★ 7.7k</sub>
  提供手绘风格编号画廊与双语提示词的 Agent Skill 资源。
  <sub>需要让 Agent 生成手绘风格图像或提示词时使用。</sub>
- **[ranxianglei/billion-context](https://github.com/ranxianglei/billion-context)** <sub>TypeScript · ★ 7.4k</sub>
  面向长会话的上下文压缩插件，减少 token 占用并支持小窗口运行。
  <sub>长时间连续对话或上下文超出窗口、需要节省 token 成本时。</sub>
- **[alchaincyf/huashu-art-motion](https://github.com/alchaincyf/huashu-art-motion)** <sub>JavaScript · ★ 6.9k</sub>
  提供35种艺术风格与9种解说语法的动画生成 Skill，用代码驱动画面动效。
  <sub>需要为 Agent 增加艺术动画生成能力，或制作带解说的动态视觉内容时。</sub>
- **[Tencent/teamai-cli](https://github.com/Tencent/teamai-cli)** <sub>TypeScript · ★ 5.8k</sub>
  面向团队场景的 AI 命令行工具。
  <sub>官方描述较简短，具体用法待补充。</sub>
- **[omdsh-dev/DSH-better-sidebar](https://github.com/omdsh-dev/DSH-better-sidebar)** <sub>TypeScript · ★ 5.2k</sub>
  可扩展的侧边栏底座，内置文件编辑、终端、Git 与子代理页面。
  <sub>想给 DeepSeek Harness 增加自定义侧边栏能力时。</sub>
- **[MarkusPfundstein/mcp-obsidian](https://github.com/MarkusPfundstein/mcp-obsidian)** <sub>Python · ★ 4.5k</sub>
  通过 Obsidian 本地 REST API 插件读写笔记的 MCP 服务器。
  <sub>希望让 AI 助手直接检索和编辑本地 Obsidian 笔记库时。</sub>
- **[anywhere-labs/Agents-Anywhere](https://github.com/anywhere-labs/Agents-Anywhere)** <sub>TypeScript · ★ 3.4k</sub>
  跨设备的开源 Agent 工作台，可远程控制 Claude Code、Codex 等编码智能体。
  <sub>需要在多台设备间远程调度和统一管理本地编码 Agent 时。</sub>
- **[NarratorAI-Studio/narrator-ai-cli-skill](https://github.com/NarratorAI-Studio/narrator-ai-cli-skill)** <sub>★ 3.2k</sub>
  封装 narrator-ai-cli 的 Agent Skill，供 Claude、Codex 等工具调用生成视频解说。
  <sub>想让编码 Agent 直接调用命令行完成影视解说或短剧配音生成时。</sub>
- **[shaobeichen/dsh-pocket](https://github.com/shaobeichen/dsh-pocket)** <sub>JavaScript · ★ 3k</sub>
  把电脑上运行的 DeepSeek Harness Web 服务通过二维码同步到手机访问的插件。
  <sub>需要在手机上远程查看和操作电脑端 DeepSeek Harness 时使用。</sub>
- **[arjun988/blender-skills](https://github.com/arjun988/blender-skills)** <sub>TypeScript · ★ 2.9k</sub>
  面向 Blender 的 Agent Skills 集合，通过 MCP 串联从粗模到引擎导出的制作流程。
  <sub>用 Cursor 或 Claude Code 等 Agent 辅助 Blender 建模与导出时，可加载这套技能。</sub>
- **[yaojingang/yao-meta-skill](https://github.com/yaojingang/yao-meta-skill)** <sub>Python · ★ 2.7k</sub>
  面向可复用 Agent Skills 的工程化、评估、治理与可移植性框架。
  <sub>需要为团队建立 Agent 技能规范、评估与治理流程时。</sub>
- **[alchaincyf/huashu-motion](https://github.com/alchaincyf/huashu-motion)** <sub>JavaScript · ★ 2.7k</sub>
  为编码 Agent 提供生成商业级产品宣传片的技能包，含配乐与画面局部修改。
  <sub>需要让编码 Agent 直接产出产品宣传视频并按画面指定位置修改时。</sub>
- **[imxv/Pretty-mermaid-skills](https://github.com/imxv/Pretty-mermaid-skills)** <sub>JavaScript · ★ 1.6k</sub>
  为 AI Agent 提供生成并渲染 Mermaid 图表为 SVG 或终端 ASCII 的技能包。
  <sub>需要让编码 Agent 自动输出流程图、架构图等文档配图时。</sub>
- **[alchaincyf/huashu-chrome](https://github.com/alchaincyf/huashu-chrome)** <sub>JavaScript · ★ 595</sub>
  通过 MCP 与 Chrome 扩展让 AI Agent 操控带登录态的浏览器。
  <sub>需要让 Agent 操作已登录的网页、复用现有会话时。</sub>
- **[alchaincyf/huashu-report](https://github.com/alchaincyf/huashu-report)** <sub>Python · ★ 494</sub>
  面向机构级研究报告生成的 Agent Skill，含报告原型与图表流水线。
  <sub>需要让 Agent 按规范产出结构化研究报告与图表时。</sub>
- **[oil-oil/dsh-oil-ui](https://github.com/oil-oil/dsh-oil-ui)** <sub>JavaScript · ★ 247</sub>
  Oil UI 的 DeepSeek Harness 原生插件，可自动切换本地安装的 Oil UI Pro。
  <sub>在 DeepSeek Harness 中使用 Oil UI 并需要自动切换本地 Pro 版本时。</sub>
- **[suzike/dsh-freestyle-theme](https://github.com/suzike/dsh-freestyle-theme)** `自研` <sub>TypeScript · ★ 12</sub>
  为 DeepSeek Harness 提供 OKLCH 主题与可视化主题设计器的插件，支持跨重启持久化。
  <sub>需要自定义 DeepSeek Harness 界面配色并保存主题设置时使用。</sub>
- **[suzike-dev/polarion-mcp-server](https://github.com/suzike-dev/polarion-mcp-server)** `私有` `自研` <sub>TypeScript · ★ 1</sub>
  面向 Polarion SOAP 接口的带权限管控 MCP server。
  <sub>想让 AI 安全访问 Polarion 需求管理数据时。</sub>
- **[suzike-dev/polarion-super-sidebar](https://github.com/suzike-dev/polarion-super-sidebar)** `自研` <sub>HTML · ★ 1</sub>
  为 Polarion 提供本地 Agent、富文本与工程画板协作的侧边栏扩展，支持工作项写回与追溯。
  <sub>需要在 Polarion 需求管理界面内接入本地 Agent 辅助编辑与追溯时。</sub>

## 知识库、RAG 与记忆

<sub>12 个 · [返回目录](#目录)</sub>

- **[thedotmack/claude-mem](https://github.com/thedotmack/claude-mem)** <sub>TypeScript · ★ 117k</sub>
  为编码 Agent 记录会话过程并压缩存储，在后续会话中注入相关上下文的记忆工具。
  <sub>希望 Agent 跨会话保留项目上下文、避免重复交代背景时。</sub>
- **[opendatalab/MinerU](https://github.com/opendatalab/MinerU)** <sub>Python · ★ 83.7k</sub>
  将 PDF、Office 等复杂文档解析为 Markdown/JSON 的文档抽取工具。
  <sub>需要把文档转成结构化文本供 RAG 或 Agent 工作流使用时。</sub>
- **[Tencent/WeKnora](https://github.com/Tencent/WeKnora)** <sub>Go · ★ 37.4k</sub>
  把原始文档转成可检索的 RAG、推理智能体与自维护 Wiki 的开源知识平台。
  <sub>需要把私有文档沉淀成可问答知识库、且希望自行部署时。</sub>
- **[opendataloader-project/opendataloader-pdf](https://github.com/opendataloader-project/opendataloader-pdf)** <sub>Java · ★ 30.3k</sub>
  开源 PDF 解析工具，将 PDF 转为带坐标、表格与标记的 Markdown、JSON 等结构化数据。
  <sub>需要把 PDF 文档转成可检索结构化数据以构建 RAG 或做无障碍处理时。</sub>
- **[nashsu/llm_wiki](https://github.com/nashsu/llm_wiki)** <sub>TypeScript · ★ 21.7k</sub>
  把文档自动整理成互链知识库的跨平台桌面应用。
  <sub>同上，两者描述一致，此为星标数更高的版本。</sub>
- **[chaitin/PandaWiki](https://github.com/chaitin/PandaWiki)** <sub>TypeScript · ★ 10.5k</sub>
  大模型驱动的开源知识库系统，支持产品文档、技术文档、FAQ 与博客搭建。
  <sub>需要自建带 AI 问答与搜索能力的团队文档或知识库时。</sub>
- **[xerrors/Yuxi](https://github.com/xerrors/Yuxi)** <sub>Python · ★ 7.7k</sub>
  可私有部署的多租户知识智能体平台，整合 RAG、知识图谱与多智能体。
  <sub>需要在自有服务器上搭建带权限管理的企业知识问答与检索系统时。</sub>
- **[tianma-if/edgeever](https://github.com/tianma-if/edgeever)** <sub>TypeScript · ★ 3.2k</sub>
  支持即时同步与原生 MCP 的 AI 知识库，可替代印象笔记或 Obsidian。
  <sub>需要自建或部署在 Cloudflare 上的个人笔记与知识管理库时。</sub>
- **[SourceWeft/SourceWeft](https://github.com/SourceWeft/SourceWeft)** <sub>TypeScript · ★ 475</sub>
  可自托管的 AI 工作站，整合智能体、技能、MCP 与带引用的知识库问答。
  <sub>希望用自有模型和基础设施搭建带引用来源的文档问答与知识库时。</sub>
- **[0xCoach/TaoSheng](https://github.com/0xCoach/TaoSheng)** <sub>Kotlin · ★ 390</sub>
  安卓端全天录音转写、声纹认人并由大模型整理为待办与记忆的应用。
  <sub>想把日常对话自动记录成个人记忆与待办，且数据只留在手机本地时。</sub>
- **[zenghui-li/yuxi](https://github.com/zenghui-li/yuxi)** <sub>Python · ★ 183</sub>
  集成 LightRAG 知识库与知识图谱的多租户 Agent Harness 平台。
  <sub>需要为自己的 Agent 搭一套带知识库与图谱的后端时。</sub>
- **[suzike/llm_wiki](https://github.com/suzike/llm_wiki)** `自研` <sub>TypeScript · ★ 2</sub>
  把文档自动整理成互链知识库的跨平台桌面应用。
  <sub>想在本机把零散文档变成可检索的 wiki 时。</sub>

## MATLAB / Simulink 与基于模型的设计

<sub>8 个 · [返回目录](#目录)</sub>

- **[matlab/matlab-mcp-server](https://github.com/matlab/matlab-mcp-server)** <sub>Go · ★ 1.8k</sub>
  MathWorks 官方 MCP server，让 AI 应用直接运行 MATLAB。
  <sub>想让 Claude 等 AI 直接执行 MATLAB 代码时。</sub>
- **[matlab/simulink-agentic-toolkit](https://github.com/matlab/simulink-agentic-toolkit)** <sub>HTML · ★ 1.3k</sub>
  让 AI 智能体具备 Simulink 与基于模型设计工作能力的官方工具集。
  <sub>想让 Agent 参与 Simulink 建模与 MBD 流程时。</sub>
- **[matlab/matlab-agentic-toolkit](https://github.com/matlab/matlab-agentic-toolkit)** <sub>MATLAB · ★ 1.3k</sub>
  把 MATLAB 能力封装给 AI 智能体使用的官方工具集。
  <sub>需要让 Agent 稳定调用 MATLAB 工程能力时。</sub>
- **[matlab/agent-skills-playground](https://github.com/matlab/agent-skills-playground)** <sub>HTML · ★ 203</sub>
  面向 MATLAB/Simulink 的 Agent Skills 原型与演示沙箱。
  <sub>想为 MATLAB 工作流编写自定义 Agent 技能时的起点。</sub>
- **[suzike/DeepSeekMatlabCopilot](https://github.com/suzike/DeepSeekMatlabCopilot)** `自研` <sub>MATLAB · ★ 11</sub>
  面向 MATLAB 工程流程的 DeepSeek 辅助工具。
  <sub>想在 MATLAB 工作中接入 DeepSeek 时。</sub>
- **[suzike-dev/Matlab-Simulink-SuperAgent](https://github.com/suzike-dev/Matlab-Simulink-SuperAgent)** `私有` `自研` <sub>HTML · ★ 1</sub>
  内嵌进 MATLAB/Simulink 界面的 AI 智能体，支持多种模型后端。
  <sub>想在建模环境里直接调用 AI 辅助、不来回切换窗口时。</sub>
- **[suzike-dev/model-code-to-srs](https://github.com/suzike-dev/model-code-to-srs)** `私有` `自研` <sub>Python · ★ 1</sub>
  从 Simulink/Stateflow 模型与生成代码反推中文软件需求规格的 Agent Skill。
  <sub>需要为已完成的模型补齐可评审 SRS 文档时。</sub>
- **[suzike-dev/terminal-in-matlab](https://github.com/suzike-dev/terminal-in-matlab)** `私有` `自研` <sub>MATLAB · ★ 1</sub>
  在 MATLAB 环境中提供终端功能的工具仓库。
  <sub>需要在 MATLAB 界面内直接执行命令行操作时。</sub>

## 汽车电子、车载测试与控制

<sub>9 个 · [返回目录](#目录)</sub>

- **[shihabal3amri/DiPlay](https://github.com/shihabal3amri/DiPlay)** <sub>Kotlin · ★ 13.8k</sub>
  在兼容的安卓车机上接收有线与无线 CarPlay 的独立接收端应用。
  <sub>需要在安卓车机上使用 CarPlay 投屏功能，或研究车机端投屏协议实现时。</sub>
- **[pms67/PID](https://github.com/pms67/PID)** <sub>C · ★ 952</sub>
  C 语言实现的 PID 控制器。
  <sub>需要在嵌入式项目中集成 PID 控制时。</sub>
- **[ecubus/EcuBus-Pro](https://github.com/ecubus/EcuBus-Pro)** <sub>C++ · ★ 909</sub>
  覆盖 UDS、CAN-TP、DOIP、LIN 与类 CAPL 脚本的汽车 ECU 开发与 HIL 测试工具。
  <sub>做 ECU 诊断、总线通信或 HIL 测试、又不想依赖商业工具链时。</sub>
- **[auto-py-utils/py-canoe](https://github.com/auto-py-utils/py-canoe)** <sub>Python · ★ 123</sub>
  用于控制 Vector CANoe 的 Python 包。
  <sub>想用 Python 脚本驱动 CANoe 时。</sub>
- **[shiivashaakeri/Data-Driven-Model-Predictive-Control-MPC-with-Stability-and-Robustness-Guarantees](https://github.com/shiivashaakeri/Data-Driven-Model-Predictive-Control-MPC-with-Stability-and-Robustness-Guarantees)** <sub>Python · ★ 88</sub>
  复现数据驱动模型预测控制论文的 Python 实现，含稳定性与鲁棒性保证。
  <sub>需要在不确定系统上研究或验证数据驱动 MPC 控制算法时。</sub>
- **[suzike-dev/Agent2Canape](https://github.com/suzike-dev/Agent2Canape)** `私有` `自研` <sub>Python · ★ 1</sub>
  面向整车工程任务的 Vector CANape 自动化、分析与安全编排平台。
  <sub>需要把标定与测量流程脚本化时。</sub>
- **[suzike-dev/Agent2Canoe](https://github.com/suzike-dev/Agent2Canoe)** `私有` `自研` <sub>Python · ★ 1</sub>
  面向 Vector CANoe 的自然语言与 AI Agent 自动化平台。
  <sub>想让 AI 驱动 CANoe 测试流程时。</sub>
- **[suzike-dev/Intelligent-Calibration-platform](https://github.com/suzike-dev/Intelligent-Calibration-platform)** `私有` `自研` <sub>Python · ★ 1</sub>
  面向智能热管理与空调舒适性的实车标定平台。
  <sub>需要管理热管理标定数据与试验流程时。</sub>
- **[suzike-dev/Vehicle-Thermal-LLM-MultiAgent](https://github.com/suzike-dev/Vehicle-Thermal-LLM-MultiAgent)** `私有` `自研` <sub>Python · ★ 1</sub>
  面向汽车空调热舒适的大模型驱动多智能体系统。
  <sub>研究大模型在热舒适控制中的应用时。</sub>

## 内容创作与多媒体生成

<sub>16 个 · [返回目录](#目录)</sub>

- **[AUTOMATIC1111/stable-diffusion-webui](https://github.com/AUTOMATIC1111/stable-diffusion-webui)** <sub>Python · ★ 165.3k</sub>
  本地部署的 Stable Diffusion 图像生成 Web 界面。
  <sub>想在本机跑文生图、且需要完整参数控制与插件生态时。</sub>
- **[harry0703/MoneyPrinterTurbo](https://github.com/harry0703/MoneyPrinterTurbo)** <sub>Python · ★ 143.5k</sub>
  根据主题或关键词自动生成高清短视频的 AI 工作流工具。
  <sub>需要批量制作短视频素材、自动配音加字幕时。</sub>
- **[tt-a1i/archify](https://github.com/tt-a1i/archify)** <sub>JavaScript · ★ 96.4k</sub>
  生成架构图、流程图、时序图与数据流图的自包含 HTML Agent Skill。
  <sub>需要带动效、可导出、可验证的技术图表时。</sub>
- **[storytold/photocraft](https://github.com/storytold/photocraft)** <sub>Rust · ★ 79.4k</sub>
  用纯 Rust 从零编写的开源照片编辑软件。
  <sub>需要对图片进行编辑处理，并希望使用开源本地工具时。</sub>
- **[ATH-MaaS/Pixelle-Video](https://github.com/ATH-MaaS/Pixelle-Video)** <sub>Python · ★ 30.1k</sub>
  AI 全自动短视频生成引擎。
  <sub>需要批量产出短视频内容时。</sub>
- **[meta/astryx](https://github.com/meta/astryx)** <sub>TypeScript · ★ 27.9k</sub>
  可定制、面向智能体使用的开源设计系统，提供组件与设计规范。
  <sub>需要为产品搭建统一界面规范，或让智能体按设计系统生成界面时。</sub>
- **[easydiffusion/easydiffusion](https://github.com/easydiffusion/easydiffusion)** <sub>JavaScript · ★ 10.5k</sub>
  一键式本地 AI 绘图工具，面向无技术背景用户。
  <sub>想零配置体验本地图像生成时。</sub>
- **[Cocoon-AI/architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)** <sub>HTML · ★ 7.6k</sub>
  把系统架构描述生成独立 HTML/SVG 架构图的 Claude Skill。
  <sub>需要快速产出可分享的架构图、又不想手绘时。</sub>
- **[ZJU-REAL/Easel](https://github.com/ZJU-REAL/Easel)** <sub>Python · ★ 4.7k</sub>
  面向社交媒体的开源 AI 智能体，可发现热点、生成内容并一键发布到多平台。
  <sub>需要批量产出并分发小红书、抖音、知乎等平台内容时。</sub>
- **[LearnPrompt/awesome-seedance](https://github.com/LearnPrompt/awesome-seedance)** <sub>JavaScript · ★ 2.5k</sub>
  Seedance 视频生成提示词库，含案例、模板与可安装的 AI 视频 Skills。
  <sub>需要用 Seedance 生成视频并参考现成提示词模板时。</sub>
- **[JimLiu/baocut](https://github.com/JimLiu/baocut)** <sub>TypeScript · ★ 1.8k</sub>
  带可编辑时间线的 AI 视频处理工具，支持转写、字幕、翻译、配音、剪辑与动画。
  <sub>需要为视频批量生成字幕、翻译配音或做时间线剪辑时。</sub>
- **[threerocks/sweety-handdraw-video](https://github.com/threerocks/sweety-handdraw-video)** <sub>Python · ★ 1.2k</sub>
  从主题或文章生成手绘讲解视频，含描线、逐字书写与配音流程。
  <sub>需要把文章或主题快速转成手绘风格讲解视频时。</sub>
- **[Aryanutkarsh/SeeCode](https://github.com/Aryanutkarsh/SeeCode)** <sub>JavaScript · ★ 948</sub>
  根据简短 JSON 规格生成可交互动画架构图的工具，面向编码智能体。
  <sub>需要把系统设计或代码结构快速转成可探索的动画图表时。</sub>
- **[guanmo-ai/design-style](https://github.com/guanmo-ai/design-style)** <sub>TypeScript · ★ 253</sub>
  每日分享一种设计风格，提供动效短片、风格图与制作指南并开放源码。
  <sub>需要参考设计风格或制作动效短片、风格图素材时使用。</sub>
- **[NINKCH/dsh-infinite_canvas](https://github.com/NINKCH/dsh-infinite_canvas)** <sub>JavaScript · ★ 148</sub>
  基于节点的短剧创作插件，覆盖剧本、分镜、素材一致性与视频生成及剪辑。
  <sub>需要本地化、自带模型的短剧脚本到成片一体化创作流程时。</sub>
- **[suzike/nanju-write-paper](https://github.com/suzike/nanju-write-paper)** `自研` <sub>HTML · ★ 9</sub>
  从选题到成稿的写作流水线 Skill，含多 Agent 调研、五角色审查与多尺寸卡片版式输出。
  <sub>需要把技术选题批量产出为长文与公众号/PDF 版式时。</sub>

## 信息聚合与效率工具

<sub>19 个 · [返回目录](#目录)</sub>

- **[sansan0/TrendRadar](https://github.com/sansan0/TrendRadar)** <sub>Python · ★ 63.6k</sub>
  聚合多平台热点与 RSS 的 AI 舆情与趋势监控工具，支持多通道推送。
  <sub>想用关键词订阅热点并定时收到简报时。</sub>
- **[timqian/chinese-independent-blogs](https://github.com/timqian/chinese-independent-blogs)** <sub>JavaScript · ★ 24.5k</sub>
  收录中文独立博客的列表仓库，提供订阅源与站点索引。
  <sub>想找中文独立博客内容或为自己的阅读器补充 RSS 源时。</sub>
- **[genspark-ai/genoffice](https://github.com/genspark-ai/genoffice)** <sub>TypeScript · ★ 12.3k</sub>
  开源 AI 办公套件，含文档、表格、幻灯片与 PDF 编辑器及本地文件读写命令行工具。
  <sub>需要本地用自有密钥让编码智能体创建和编辑 Office 文件时。</sub>
- **[Tianyu199509/DeskBox](https://github.com/Tianyu199509/DeskBox)** <sub>C# · ★ 9.1k</sub>
  开源的 Windows 桌面整理工具，用 WinUI 3 小组件管理桌面文件与图标。
  <sub>Windows 桌面文件杂乱，需要分类整理并添加桌面小组件时。</sub>
- **[guaguastandup/zotero-pdf2zh](https://github.com/guaguastandup/zotero-pdf2zh)** <sub>Python · ★ 8.3k</sub>
  Zotero 的 PDF 中文翻译插件。
  <sub>需要读英文论文并要中文对照时。</sub>
- **[Kuddev/pebrel](https://github.com/Kuddev/pebrel)** <sub>Rust · ★ 3.8k</sub>
  面向 Windows 的 GPU 加速终端模拟器，支持 SSH、分屏与会话保持。
  <sub>需要在 Windows 上使用带分屏和 SSH 的终端跑 AI CLI 时。</sub>
- **[alejandrobujan/tendedero](https://github.com/alejandrobujan/tendedero)** <sub>Swift · ★ 3.2k</sub>
  把每张截图挂到屏幕顶部一条线上的 macOS 小工具。
  <sub>需要随手查看最近截图、避免窗口遮挡时使用。</sub>
- **[dw-dengwei/daily-arXiv-ai-enhanced](https://github.com/dw-dengwei/daily-arXiv-ai-enhanced)** <sub>JavaScript · ★ 3k</sub>
  每日自动抓取 arXiv 论文并用 AI 生成摘要、以 GitHub Pages 展示的聚合站点。
  <sub>需要每天快速浏览 AI 领域新论文摘要、跟踪研究动态时。</sub>
- **[s1dashu/quiet-md](https://github.com/s1dashu/quiet-md)** <sub>Rust · ★ 1.8k</sub>
  基于 Rust 与 GPUI 的本地优先笔记应用，兼容飞书文档格式，支持 macOS 与 Windows。
  <sub>需要本地存储笔记并与飞书文档格式互通时。</sub>
- **[ELY-Open-Source/ElyOffice](https://github.com/ELY-Open-Source/ElyOffice)** <sub>Rust · ★ 1.5k</sub>
  用 Rust 与 GPUI 构建的离线优先桌面办公套件。
  <sub>需要在本地离线处理文档、不依赖云服务的办公场景时。</sub>
- **[fuxiaoai/tidings-rss](https://github.com/fuxiaoai/tidings-rss)** <sub>Python · ★ 653</sub>
  经过筛选与实时校验的 OPML 订阅源合集，覆盖 AI、新闻、研究、播客等。
  <sub>需要批量导入 RSS 阅读器、快速搭建信息订阅源时使用。</sub>
- **[yetone/alma-relay](https://github.com/yetone/alma-relay)** <sub>JavaScript · ★ 528</sub>
  可自托管的中继服务，用手机远程访问桌面端 Alma 应用。
  <sub>需要在手机上随时远程操作桌面应用时。</sub>
- **[RoversX/ThinkTerm](https://github.com/RoversX/ThinkTerm)** <sub>Rust · ★ 249</sub>
  内置多路复用器的终端，关闭后会话继续运行，可跨机器管理 shell 与 AI 智能体。
  <sub>需要在桌面、浏览器和 TUI 间切换并保持长时间任务不中断时。</sub>
- **[jackwener/Kaze](https://github.com/jackwener/Kaze)** <sub>JavaScript · ★ 210</sub>
  macOS 上的轻量浏览器，内置可在标签页中执行任务的智能体。
  <sub>日常浏览网页并希望由智能体协助处理页面内容时。</sub>
- **[suzike/sunmemo-windows](https://github.com/suzike/sunmemo-windows)** `自研` <sub>JavaScript · ★ 6</sub>
  本地离线的 Electron 桌面应用，用于记录未完成的想法与待办。
  <sub>需要一款不联网、随手记录零散想法和待办事项的桌面工具时。</sub>
- **[suzike/RobinRead](https://github.com/suzike/RobinRead)** `自研` <sub>JavaScript · ★ 3</sub>
  本地优先、AI 增强的纸感三栏 RSS 阅读器（Windows / Electron）。
  <sub>想要不依赖云端的 RSS 阅读体验时。</sub>
- **[suzike/starred-toolbox](https://github.com/suzike/starred-toolbox)** `自研` <sub>Python · ★ 3</sub>
  用 Actions 定时同步并自动归类解读个人 GitHub 星标仓库的归档工具。
  <sub>想把自己的 GitHub Star 整理成可检索、带分类说明的个人知识库时。</sub>
- **[suzike/juzhen-dock](https://github.com/suzike/juzhen-dock)** `自研` <sub>HTML · ★ 2</sub>
  常驻 Windows 屏幕右侧的桌面入口工具，同一份 UI 源码可产出浏览器原型与 Electron 桌面版。
  <sub>需要在 Windows 桌面侧边常驻一个快速启动入口，并兼顾浏览器预览与桌面打包时。</sub>
- **[suzike/Office-Viewer](https://github.com/suzike/Office-Viewer)** `自研` <sub>TypeScript · ★ 2</sub>
  Windows 桌面文档查看与编辑器，支持 Office、Markdown、压缩包与 Git 历史。
  <sub>想不装 Office 也能快速查看和编辑文档时。</sub>

## 编程学习与计算机基础

<sub>21 个 · [返回目录](#目录)</sub>

- **[sindresorhus/awesome](https://github.com/sindresorhus/awesome)** <sub>★ 536.8k</sub>
  汇集各类主题优质资源清单的 Awesome 列表总目录仓库。
  <sub>想按主题查找学习资料、工具或开源项目索引时。</sub>
- **[ossu/computer-science](https://github.com/ossu/computer-science)** <sub>HTML · ★ 211.1k</sub>
  免费的计算机科学自学课程路线。
  <sub>想按完整课程体系自学 CS 时。</sub>
- **[521xueweihan/HelloGitHub](https://github.com/521xueweihan/HelloGitHub)** <sub>Python · ★ 188.8k</sub>
  面向入门者的开源项目推荐月刊。
  <sub>想发现适合上手的开源项目时。</sub>
- **[jackfrued/Python-100-Days](https://github.com/jackfrued/Python-100-Days)** <sub>Jupyter Notebook · ★ 187.8k</sub>
  从入门到进阶的 Python 系统教程，按天组织。
  <sub>想按天推进、系统学完 Python 时。</sub>
- **[justjavac/free-programming-books-zh_CN](https://github.com/justjavac/free-programming-books-zh_CN)** <sub>★ 119.6k</sub>
  免费计算机技术中文书籍索引。
  <sub>需要找中文技术书时。</sub>
- **[rohitg00/ai-engineering-from-scratch](https://github.com/rohitg00/ai-engineering-from-scratch)** <sub>Python · ★ 78.8k</sub>
  从零学习 AI 工程的教程项目，覆盖 LLM、Agent 与深度学习。
  <sub>想系统入门 AI 工程并动手实现各模块时作为学习路线。</sub>
- **[HKUDS/DeepTutor](https://github.com/HKUDS/DeepTutor)** <sub>Python · ★ 59.2k</sub>
  基于多智能体与 RAG 的个性化长期学习辅导系统。
  <sub>想搭建能持续跟踪学习进度并答疑的 AI 辅导工具时。</sub>
- **[storytold/craft-anything](https://github.com/storytold/craft-anything)** <sub>Rust · ★ 32.5k</sub>
  帮助理解任意软件工作原理并动手仿制实现的学习型项目。
  <sub>想通过拆解并复刻现有软件来学习系统设计与实现时。</sub>
- **[izackwu/TeachYourselfCS-CN](https://github.com/izackwu/TeachYourselfCS-CN)** <sub>★ 22.2k</sub>
  计算机科学自学路线指南的中文翻译。
  <sub>想按体系补齐计算机基础、又需要中文材料时。</sub>
- **[zergtant/pytorch-handbook](https://github.com/zergtant/pytorch-handbook)** <sub>Jupyter Notebook · ★ 21.7k</sub>
  PyTorch 入门开源书籍，教程均可运行。
  <sub>想系统学习 PyTorch 时。</sub>
- **[Yixiaohan/show-me-the-code](https://github.com/Yixiaohan/show-me-the-code)** <sub>★ 13.7k</sub>
  Python 练习册，每天一个小程序。
  <sub>想通过小练习巩固 Python 基础时。</sub>
- **[jikexueyuanwiki/tensorflow-zh](https://github.com/jikexueyuanwiki/tensorflow-zh)** <sub>TeX · ★ 12.3k</sub>
  TensorFlow 官方文档的中文翻译。
  <sub>需要查阅中文 TensorFlow 文档时。</sub>
- **[lawlite19/MachineLearning_Python](https://github.com/lawlite19/MachineLearning_Python)** <sub>Python · ★ 8.7k</sub>
  机器学习算法的 Python 实现合集。
  <sub>想对照代码理解经典算法时。</sub>
- **[jackzhenguo/python-small-examples](https://github.com/jackzhenguo/python-small-examples)** <sub>Python · ★ 8.1k</sub>
  Python 实用小例子合集。
  <sub>想快速查某个 Python 写法的实例时。</sub>
- **[billryan/algorithm-exercise](https://github.com/billryan/algorithm-exercise)** <sub>Python · ★ 3.5k</sub>
  数据结构与算法题解笔记，含 LeetCode 与 LintCode。
  <sub>刷题或复习算法时。</sub>
- **[datawhalechina/hugging-llm](https://github.com/datawhalechina/hugging-llm)** <sub>Jupyter Notebook · ★ 3.1k</sub>
  Datawhale 出品的大模型入门与实践教程。
  <sub>想跟着中文教程系统入门大模型时。</sub>
- **[datawhalechina/team-learning](https://github.com/datawhalechina/team-learning)** <sub>★ 2.4k</sub>
  Datawhale 组队学习计划的资料汇总。
  <sub>想跟着组队节奏推进学习时。</sub>
- **[yidao620c/core-algorithm](https://github.com/yidao620c/core-algorithm)** <sub>Python · ★ 783</sub>
  常见算法的 Python 实现集合。
  <sub>复习算法实现细节时。</sub>
- **[alchaincyf/3d-vibe-coding-handbook](https://github.com/alchaincyf/3d-vibe-coding-handbook)** <sub>HTML · ★ 311</sub>
  《3D Vibe Coding 手册》配套仓库，含 HTML 书稿、示例源码与资源索引。
  <sub>想按教程学习 3D 与 AI 生成建模、并动手跑示例时。</sub>
- **[ninetyhe-90/training-explore](https://github.com/ninetyhe-90/training-explore)** <sub>TypeScript · ★ 152</sub>
  交互式演示大语言模型训练过程的探索工具。
  <sub>想直观理解 LLM 训练各阶段原理时用于学习。</sub>
- **[suzike/EmbedSummary](https://github.com/suzike/EmbedSummary)** `自研` <sub>★ 1</sub>
  嵌入式开发资源汇总。
  <sub>需要嵌入式方向的资料索引时。</sub>

## 机器学习与深度学习框架

<sub>6 个 · [返回目录](#目录)</sub>

- **[tensorflow/models](https://github.com/tensorflow/models)** <sub>Python · ★ 77.6k</sub>
  TensorFlow 官方模型与示例库。
  <sub>想找官方模型实现作参考时。</sub>
- **[PaddlePaddle/Paddle](https://github.com/PaddlePaddle/Paddle)** <sub>C++ · ★ 24.1k</sub>
  百度开源的深度学习框架（飞桨）。
  <sub>需要在国产框架上训练与部署模型时。</sub>
- **[optuna/optuna](https://github.com/optuna/optuna)** <sub>Python · ★ 15k</sub>
  面向机器学习的超参数自动搜索与优化框架，支持分布式并行试验。
  <sub>需要为模型训练自动调参、并行跑多组试验并管理结果时。</sub>
- **[DLR-RM/stable-baselines3](https://github.com/DLR-RM/stable-baselines3)** <sub>Python · ★ 14k</sub>
  基于 PyTorch 的强化学习算法库，提供多种算法的可靠实现与统一接口。
  <sub>需要用 Python 训练或复现强化学习算法、搭建机器人控制实验时。</sub>
- **[astaxie/TokenHub](https://github.com/astaxie/TokenHub)** <sub>Go · ★ 1.4k</sub>
  面向企业的私有 AI 模型访问网关，统一接入并治理模型调用请求。
  <sub>企业需要统一管理多家大模型接入、配额与调用审计时。</sub>
- **[suzike-dev/AITrain_Platform](https://github.com/suzike-dev/AITrain_Platform)** `私有` `自研` <sub>Python · ★ 1</sub>
  覆盖 AI 算法开发、训练与部署的研发可视化管理平台。
  <sub>需要统一管理算法研发全流程时。</sub>

## 工程方法论与研发流程

<sub>2 个 · [返回目录](#目录)</sub>

- **[xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer](https://github.com/xdash/FDE-the-Guidance-Book-of-Forward-Deployed-Engineer)** <sub>★ 5.6k</sub>
  前沿部署工程师（FDE）的从零入门指南。
  <sub>想了解 FDE 岗位的能力模型与工作方法时。</sub>
- **[huangjia2019/sdd-in-action](https://github.com/huangjia2019/sdd-in-action)** <sub>Python · ★ 175</sub>
  规范驱动开发的实战手册，覆盖 Claude Code 与 OpenCode 两条路径。
  <sub>想系统学习 SDD 如何落地到日常开发时。</sub>

## 其他

<sub>8 个 · [返回目录](#目录)</sub>

- **[eternity4719/HowToLiveBetter](https://github.com/eternity4719/HowToLiveBetter)** <sub>HTML · ★ 75.7k</sub>
  按性价比排序的循证生活指南，涵盖健康、理财、法律、社保与育儿等主题。
  <sub>需要查阅有出处依据的生活决策建议时，可参考其成本收益与证据等级。</sub>
- **[pingdotgg/t3code](https://github.com/pingdotgg/t3code)** <sub>TypeScript · ★ 60.3k</sub>
  一个 TypeScript 编写的代码仓库，缺少官方描述与主题标签。
  <sub>信息有限，待补充。</sub>
- **[HeyPuter/everything](https://github.com/HeyPuter/everything)** <sub>JavaScript · ★ 8.4k</sub>
  以开源方式从零重建各类桌面软件的项目集合。
  <sub>信息有限，待补充。</sub>
- **[UniXNU/UniXNU](https://github.com/UniXNU/UniXNU)** <sub>Python · ★ 2.9k</sub>
  通过 UEFI 在非苹果 ARM64 硬件上运行 iOS 与 macOS 的引导项目。
  <sub>需要在非苹果 ARM64 设备上尝试运行苹果系统时参考。</sub>
- **[Cai-aa/CAE-Agent-Hub](https://github.com/Cai-aa/CAE-Agent-Hub)** <sub>Python · ★ 1.4k</sub>
  信息有限，待补充。
  <sub>信息有限，待补充。</sub>
- **[the-snowpear/omp-studio](https://github.com/the-snowpear/omp-studio)** <sub>TypeScript · ★ 145</sub>
  无描述信息的 TypeScript 项目，用途无法从元数据判断。
  <sub>信息有限，待补充。</sub>
- **[km-open-lab/SunMemo](https://github.com/km-open-lab/SunMemo)** <sub>Swift · ★ 4</sub>
  信息有限，无法判断其具体功能与用途。
  <sub>信息有限，待补充。</sub>
- **[suzike/suzike](https://github.com/suzike/suzike)** `自研` <sub>Python · ★ 1</sub>
  个人主页 README。
  <sub>信息有限，待补充。</sub>

## 我的自研项目

以下仓库同时出现在上方对应分类中，此处仅作快捷索引。

| 仓库 | 所属分类 | 仓库 | 所属分类 |
| :--- | :--- | :--- | :--- |
| [suzike-dev/Agent2Canape](https://github.com/suzike-dev/Agent2Canape) | 汽车电子、车载测试与控制 | [suzike-dev/Agent2Canoe](https://github.com/suzike-dev/Agent2Canoe) | 汽车电子、车载测试与控制 |
| [suzike-dev/AITrain_Platform](https://github.com/suzike-dev/AITrain_Platform) | 机器学习与深度学习框架 | [suzike-dev/Intelligent-Calibration-platform](https://github.com/suzike-dev/Intelligent-Calibration-platform) | 汽车电子、车载测试与控制 |
| [suzike-dev/IntentOS](https://github.com/suzike-dev/IntentOS) | AI Agent 与编码智能体 | [suzike-dev/Matlab-Simulink-SuperAgent](https://github.com/suzike-dev/Matlab-Simulink-SuperAgent) | MATLAB / Simulink 与基于模型的设计 |
| [suzike-dev/model-code-to-srs](https://github.com/suzike-dev/model-code-to-srs) | MATLAB / Simulink 与基于模型的设计 | [suzike-dev/polarion-mcp-server](https://github.com/suzike-dev/polarion-mcp-server) | Agent 扩展、Skills 与工具协议 |
| [suzike-dev/polarion-super-sidebar](https://github.com/suzike-dev/polarion-super-sidebar) | Agent 扩展、Skills 与工具协议 | [suzike-dev/terminal-in-matlab](https://github.com/suzike-dev/terminal-in-matlab) | MATLAB / Simulink 与基于模型的设计 |
| [suzike-dev/Vehicle-Thermal-LLM-MultiAgent](https://github.com/suzike-dev/Vehicle-Thermal-LLM-MultiAgent) | 汽车电子、车载测试与控制 | [suzike/agentic-island](https://github.com/suzike/agentic-island) | AI Agent 与编码智能体 |
| [suzike/DeepSeekMatlabCopilot](https://github.com/suzike/DeepSeekMatlabCopilot) | MATLAB / Simulink 与基于模型的设计 | [suzike/dsh-freestyle-theme](https://github.com/suzike/dsh-freestyle-theme) | Agent 扩展、Skills 与工具协议 |
| [suzike/EmbedSummary](https://github.com/suzike/EmbedSummary) | 编程学习与计算机基础 | [suzike/juzhen-dock](https://github.com/suzike/juzhen-dock) | 信息聚合与效率工具 |
| [suzike/llm_wiki](https://github.com/suzike/llm_wiki) | 知识库、RAG 与记忆 | [suzike/nanju-write-paper](https://github.com/suzike/nanju-write-paper) | 内容创作与多媒体生成 |
| [suzike/Office-Viewer](https://github.com/suzike/Office-Viewer) | 信息聚合与效率工具 | [suzike/RobinRead](https://github.com/suzike/RobinRead) | 信息聚合与效率工具 |
| [suzike/starred-toolbox](https://github.com/suzike/starred-toolbox) | 信息聚合与效率工具 | [suzike/sunmemo-windows](https://github.com/suzike/sunmemo-windows) | 信息聚合与效率工具 |
| [suzike/suzike](https://github.com/suzike/suzike) | 其他 |  |  |

---

[返回目录](#目录)

<details>
<summary>这个归档是怎么运转的</summary>

[![定时同步状态](https://github.com/suzike/starred-toolbox/actions/workflows/sync-stars.yml/badge.svg?branch=main)](https://github.com/suzike/starred-toolbox/actions/workflows/sync-stars.yml)

<sub>数据更新于 2026-11-14 16:36 UTC</sub>

- 唯一来源是本账号的 Star 列表，由 GitHub Actions 每小时定时拉取，不做任何主动发现。
- 新增条目会调用大模型归类并生成「这是什么 / 什么时候用」两句解读；没有配置模型密钥时降级为规则归类。
- 私有仓库只公开名称、描述与链接等元数据，同步脚本从不请求仓库文件、README 正文或代码内容。
- 取消 Star 后，条目会在下次同步时移出列表。

<sub>本文件与 `assets/` 下的分布图均由 `scripts/sync_stars.py` 自动生成，请勿手工编辑。</sub>

</details>
