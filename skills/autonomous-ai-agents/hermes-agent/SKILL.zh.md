---
name: hermes-agent
description: 使用和扩展 Hermes Agent 的完整指南 — CLI 使用、设置、配置、生成额外代理、网关平台、技能、语音、工具、配置文件和简明的贡献者参考。在帮助用户配置 Hermes、排除故障、生成代理实例或进行代码贡献时加载此技能。
version: 2.0.0
author: Hermes Agent + Teknium
license: MIT
metadata:
  hermes:
    tags: [hermes, setup, configuration, multi-agent, spawning, cli, gateway, development]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [claude-code, codex, opencode]
---

# Hermes Agent

Hermes Agent 是 Nous Research 开发的开源 AI 代理框架，运行在您的终端、消息传递平台和 IDE 中。它与 Claude Code（Anthropic）、Codex（OpenAI）和 OpenClaw 属于同一类别 — 自主编码和任务执行代理，使用工具调用来与您的系统交互。Hermes 适用于任何 LLM 提供商（OpenRouter、Anthropic、OpenAI、DeepSeek、本地模型以及其他 15+ 个提供商），并在 Linux、macOS 和 WSL 上运行。

使 Hermes 与众不同的是：

- **通过技能自我改进** — Hermes 通过将可重用程序保存为技能来从经验中学习。当它解决复杂问题、发现工作流或被纠正时，它可以将该知识持久化为技能文档，加载到未来的会话中。技能随着时间的推移而积累，使代理在您的特定任务和环境中表现更好。
- **跨会话的持久内存** — 记住您是谁、您的偏好、环境细节和学到的教训。可插拔的内存后端（内置、Honcho、Mem0 等）让您选择内存的工作方式。
- **多平台网关** — 同一个代理在 Telegram、Discord、Slack、WhatsApp、Signal、Matrix、Email 和其他 10+ 个平台上运行，具有完整的工具访问权限，而不仅仅是聊天。
- **提供商无关** — 在工作流中间交换模型和提供商，而无需更改任何其他内容。凭据池自动跨多个 API 密钥轮换。
- **配置文件** — 运行多个独立的 Hermes 实例，具有隔离的配置、会话、技能和内存。
- **可扩展** — 插件、MCP 服务器、自定义工具、Webhook 触发器、cron 调度和完整的 Python 生态系统。

人们使用 Hermes 进行软件开发、研究、系统管理、数据分析、内容创建、家庭自动化以及任何其他受益于具有持久上下文和完整系统访问权限的 AI 代理的事情。

**此技能帮助您有效地使用 Hermes Agent** — 设置它、配置功能、生成额外的代理实例、排除故障、找到正确的命令和设置，以及在您需要扩展或贡献时理解系统的工作方式。

**文档：** https://hermes-agent.nousresearch.com/docs/

## 快速开始

```bash
# 安装
curl -fsSL https://raw.githubusercontent.com/NousResearch/hermes-agent/main/scripts/install.sh | bash

# 交互式聊天（默认）
hermes

# 单次查询
hermes chat -q \"What is the capital of France?\"

# 设置向导
hermes setup

# 更改模型/提供商
hermes model

# 检查健康状况
hermes doctor
```

---

## CLI 参考

### 全局标志

```
hermes [flags] [command]

  --version, -V             显示版本
  --resume, -r SESSION      通过 ID 或标题恢复会话
  --continue, -c [NAME]     按名称恢复，或最近的会话
  --worktree, -w            隔离 git 工作树模式（并行代理）
  --skills, -s SKILL        预加载技能（逗号分隔或重复）
  --profile, -p NAME        使用命名配置文件
  --yolo                    跳过危险命令批准
  --pass-session-id         在系统提示中包含会话 ID
```

没有子命令默认为 `chat`。

### 聊天

```
hermes chat [flags]
  -q, --query TEXT          单次查询，非交互式
  -m, --model MODEL         模型（例如 anthropic/claude-sonnet-4）
  -t, --toolsets LIST       逗号分隔的工具集
  --provider PROVIDER       强制提供商（openrouter、anthropic、nous 等）
  -v, --verbose             详细输出
  -Q, --quiet               抑制横幅、旋转器、工具预览
  --checkpoints             启用文件系统检查点（/rollback）
  --source TAG              会话源标签（默认：cli）
```

### 配置

```
hermes setup [section]      交互式向导（model|terminal|gateway|tools|agent）
hermes model                交互式模型/提供商选择器
hermes config               查看当前配置
hermes config edit          在 $EDITOR 中打开 config.yaml
hermes config set KEY VAL   设置配置值
hermes config path          打印 config.yaml 路径
hermes config env-path      打印 .env 路径
hermes config check         检查缺失/过时的配置
hermes config migrate       使用新选项更新配置
hermes login [--provider P] OAuth 登录（nous、openai-codex）
hermes logout               清除存储的身份验证
hermes doctor [--fix]       检查依赖项和配置
hermes status [--all]       显示组件状态
```

### 工具与技能

```
hermes tools                交互式工具启用/禁用（curses UI）
hermes tools list           显示所有工具和状态
hermes tools enable NAME    启用工具集
hermes tools disable NAME   禁用工具集

hermes skills list          列出已安装的技能
hermes skills search QUERY  搜索技能中心
hermes skills install ID    安装技能
hermes skills inspect ID    预览而不安装
hermes skills config        按平台启用/禁用技能
hermes skills check         检查更新
hermes skills update        更新过时的技能
hermes skills uninstall N   移除中心技能
hermes skills publish PATH  发布到注册表
hermes skills browse        浏览所有可用技能
hermes skills tap add REPO  添加 GitHub 仓库作为技能源
```

### MCP 服务器

```
hermes mcp serve            将 Hermes 作为 MCP 服务器运行
hermes mcp add NAME         添加 MCP 服务器（--url 或 --command）
hermes mcp remove NAME      移除 MCP 服务器
hermes mcp list             列出配置的服务器
hermes mcp test NAME        测试连接
hermes mcp configure NAME   切换工具选择
```

### 网关（消息传递平台）

```
hermes gateway run          前台启动网关
hermes gateway install      安装为后台服务
hermes gateway start/stop   控制服务
hermes gateway restart      重启服务
hermes gateway status       检查状态
hermes gateway setup        配置平台
```

支持的平台：Telegram、Discord、Slack、WhatsApp、Signal、Email、SMS、Matrix、Mattermost、Home Assistant、DingTalk、Feishu、WeCom、BlueBubbles（iMessage）、Weixin（微信）、API Server、Webhooks。Open WebUI 通过 API Server 适配器连接。

平台文档：https://hermes-agent.nousresearch.com/docs/user-guide/messaging/

### 会话

```
hermes sessions list        列出最近的会话
hermes sessions browse      交互式选择器
hermes sessions export OUT  导出到 JSONL
hermes sessions rename ID T 重命名会话
hermes sessions delete ID   删除会话
hermes sessions prune       清理旧会话（--older-than N 天）
hermes sessions stats       会话存储统计信息
```

### Cron 作业

```
hermes cron list            列出作业（--all 用于禁用的）
hermes cron create SCHED    创建：'30m'、'every 2h'、'0 9 * * *'
hermes cron edit ID         编辑日程、提示、交付
hermes cron pause/resume ID 控制作业状态
hermes cron run ID          在下一个刻度触发
hermes cron remove ID       删除作业
hermes cron status          调度器状态
```

### Webhook

```
hermes webhook subscribe N  在 /webhooks/<name> 创建路由
hermes webhook list         列出订阅
hermes webhook remove NAME  移除订阅
hermes webhook test NAME    发送测试 POST
```

### 配置文件

```
hermes profile list         列出所有配置文件
hermes profile create NAME  创建（--clone、--clone-all、--clone-from）
hermes profile use NAME     设置粘性默认值
hermes profile delete NAME  删除配置文件
hermes profile show NAME    显示详细信息
hermes profile alias NAME   管理包装脚本
hermes profile rename A B   重命名配置文件
hermes profile export NAME  导出到 tar.gz
hermes profile import FILE  从存档导入
```

### 凭据池

```
hermes auth add             交互式凭据向导
hermes auth list [PROVIDER] 列出池化凭据
hermes auth remove P INDEX  按提供商 + 索引移除
hermes auth reset PROVIDER  清除耗尽状态
```

### 其他

```
hermes insights [--days N]  使用分析
hermes update               更新到最新版本
hermes pairing list/approve/revoke  DM 授权
hermes plugins list/install/remove  插件管理
hermes honcho setup/status  Honcho 内存集成（需要 honcho 插件）
hermes memory setup/status/off  内存提供商配置
hermes completion bash|zsh  Shell 补全
hermes acp                  ACP 服务器（IDE 集成）
hermes claw migrate         从 OpenClaw 迁移
hermes uninstall            卸载 Hermes
```

---

## 斜杠命令（会话内）

在交互式聊天会话期间输入这些。

### 会话控制
```
/new (/reset)        新会话
/clear               清屏 + 新会话（CLI）
/retry               重发最后一条消息
/undo                移除最后一次交换
/title [name]        命名会话
/compress            手动压缩上下文
/stop                杀死后台进程
/rollback [N]        恢复文件系统检查点
/background <prompt> 在后台运行提示
/queue <prompt>      排队等待下一轮
/resume [name]       恢复命名会话
```

### 配置
```
/config              显示配置（CLI）
/model [name]        显示或更改模型
/provider            显示提供商信息
/personality [name]  设置个性
/reasoning [level]   设置推理（none|minimal|low|medium|high|xhigh|show|hide）
/verbose             循环：关 → 新 → 全部 → 详细
/voice [on|off|tts]  语音模式
/yolo                切换批准绕过
/skin [name]         更改主题（CLI）
/statusbar           切换状态栏（CLI）
```

### 工具与技能
```
/tools               管理工具（CLI）
/toolsets            列出工具集（CLI）
/skills              搜索/安装技能（CLI）
/skill <name>        将技能加载到会话中
/cron                管理 cron 作业（CLI）
/reload-mcp          重新加载 MCP 服务器
/plugins             列出插件（CLI）
```

### 网关
```
/approve             批准待处理的命令（网关）
/deny                拒绝待处理的命令（网关）
/restart             重启网关（网关）
/sethome             将当前聊天设置为主频道（网关）
/update              将 Hermes 更新到最新（网关）
/platforms (/gateway) 显示平台连接状态（网关）
```

### 实用工具
```
/branch (/fork)      分支当前会话
/btw                 短暂的附带问题（不中断主任务）
/fast                切换优先级/快速处理
/browser             打开 CDP 浏览器连接
/history             显示对话历史（CLI）
/save                将对话保存到文件（CLI）
/paste               附加剪贴板图像（CLI）
/image               附加本地图像文件（CLI）
```

### 信息
```
/help                显示命令
/commands [page]     浏览所有命令（网关）
/usage               令牌使用情况
/insights [days]     使用分析
/status              会话信息（网关）
/profile             活动配置文件信息
```

### 退出
```
/quit (/exit, /q)    退出 CLI
```

---

## 关键路径与配置

```
~/.hermes/config.yaml       主配置
~/.hermes/.env              API 密钥和机密
$HERMES_HOME/skills/        已安装的技能
~/.hermes/sessions/         会话转录
~/.hermes/logs/             网关和错误日志
~/.hermes/auth.json         OAuth 令牌和凭据池
~/.hermes/hermes-agent/     源代码（如果是 git 安装）
```

配置文件使用 `~/.hermes/profiles/<name>/`，布局相同。

### 配置部分

使用 `hermes config edit` 或 `hermes config set section.key value` 编辑。

| 部分 | 关键选项 |
|---------|-------------|
| `model` | `default`、`provider`、`base_url`、`api_key`、`context_length` |
| `agent` | `max_turns`（90）、`tool_use_enforcement` |
| `terminal` | `backend`（local/docker/ssh/modal）、`cwd`、`timeout`（180） |
| `compression` | `enabled`、`threshold`（0.50）、`target_ratio`（0.20） |
| `display` | `skin`、`tool_progress`、`show_reasoning`、`show_cost` |
| `stt` | `enabled`、`provider`（local/groq/openai/mistral） |
| `tts` | `provider`（edge/elevenlabs/openai/minimax/mistral/neutts） |
| `memory` | `memory_enabled`、`user_profile_enabled`、`provider` |
| `security` | `tirith_enabled`、`website_blocklist` |
| `delegation` | `model`、`provider`、`base_url`、`api_key`、`max_iterations`（50）、`reasoning_effort` |
| `smart_model_routing` | `enabled`、`cheap_model` |
| `checkpoints` | `enabled`、`max_snapshots`（50） |

完整配置参考：https://hermes-agent.nousresearch.com/docs/user-guide/configuration

### 提供商

支持 20+ 个提供商。通过 `hermes model` 或 `hermes setup` 设置。

| 提供商 | 身份验证 | 密钥环境变量 |
|----------|------|-------------|
| OpenRouter | API 密钥 | `OPENROUTER_API_KEY` |
| Anthropic | API 密钥 | `ANTHROPIC_API_KEY` |
| Nous Portal | OAuth | `hermes auth` |
| OpenAI Codex | OAuth | `hermes auth` |
| GitHub Copilot | 令牌 | `COPILOT_GITHUB_TOKEN` |
| Google Gemini | API 密钥 | `GOOGLE_API_KEY` 或 `GEMINI_API_KEY` |
| DeepSeek | API 密钥 | `DEEPSEEK_API_KEY` |
| xAI / Grok | API 密钥 | `XAI_API_KEY` |
| Hugging Face | 令牌 | `HF_TOKEN` |
| Z.AI / GLM | API 密钥 | `GLM_API_KEY` |
| MiniMax | API 密钥 | `MINIMAX_API_KEY` |
| MiniMax CN | API 密钥 | `MINIMAX_CN_API_KEY` |
| Kimi / Moonshot | API 密钥 | `KIMI_API_KEY` |
| Alibaba / DashScope | API 密钥 | `DASHSCOPE_API_KEY` |
| Xiaomi MiMo | API 密钥 | `XIAOMI_API_KEY` |
| Kilo Code | API 密钥 | `KILOCODE_API_KEY` |
| AI Gateway (Vercel) | API 密钥 | `AI_GATEWAY_API_KEY` |
| OpenCode Zen | API 密钥 | `OPENCODE_ZEN_API_KEY` |
| OpenCode Go | API 密钥 | `OPENCODE_GO_API_KEY` |
| Qwen OAuth | OAuth | `hermes login --provider qwen-oauth` |
| 自定义端点 | 配置 | config.yaml 中的 `model.base_url` + `model.api_key` |
| GitHub Copilot ACP | 外部 | `COPILOT_CLI_PATH` 或 Copilot CLI |

完整提供商文档：https://hermes-agent.nousresearch.com/docs/integrations/providers

### 工具集

通过 `hermes tools`（交互式）或 `hermes tools enable/disable NAME` 启用/禁用。

| 工具集 | 提供的内容 |
|---------|-----------------|
| `web` | Web 搜索和内容提取 |
| `browser` | 浏览器自动化（Browserbase、Camofox 或本地 Chromium） |
| `terminal` | Shell 命令和进程管理 |
| `file` | 文件读/写/搜索/补丁 |
| `code_execution` | 沙盒化 Python 执行 |
| `vision` | 图像分析 |
| `image_gen` | AI 图像生成 |
| `tts` | 文本到语音 |
| `skills` | 技能浏览和管理 |
| `memory` | 持久的跨会话内存 |
| `session_search` | 搜索过去的对话 |
| `delegation` | 子代理任务委托 |
| `cronjob` | 定时任务管理 |
| `clarify` | 向用户提出澄清问题 |
| `messaging` | 跨平台消息发送 |
| `search` | 仅 Web 搜索（`web` 的子集） |
| `todo` | 会话内任务规划和跟踪 |
| `rl` | 强化学习工具（默认关闭） |
| `moa` | 代理混合（默认关闭） |
| `homeassistant` | 智能家居控制（默认关闭） |

工具更改在 `/reset`（新会话）上生效。它们不会在对话中间应用以保留提示缓存。

---

## 语音与转录

### STT（语音 → 文本）

来自消息传递平台的语音消息会自动转录。

提供商优先级（自动检测）：
1. **本地 faster-whisper** — 免费，无需 API 密钥：`pip install faster-whisper`
2. **Groq Whisper** — 免费层：设置 `GROQ_API_KEY`
3. **OpenAI Whisper** — 付费：设置 `VOICE_TOOLS_OPENAI_KEY`
4. **Mistral Voxtral** — 设置 `MISTRAL_API_KEY`

配置：
```yaml
stt:
  enabled: true
  provider: local        # local、groq、openai、mistral
  local:
    model: base          # tiny、base、small、medium、large-v3
```

### TTS（文本 → 语音）

| 提供商 | 环境变量 | 免费？ |
|----------|---------|-------|
| Edge TTS | 无 | 是（默认） |
| ElevenLabs | `ELEVENLABS_API_KEY` | 免费层 |
| OpenAI | `VOICE_TOOLS_OPENAI_KEY` | 付费 |
| MiniMax | `MINIMAX_API_KEY` | 付费 |
| Mistral (Voxtral) | `MISTRAL_API_KEY` | 付费 |
| NeuTTS（本地） | 无（`pip install neutts[all]` + `espeak-ng`） | 免费 |

语音命令：`/voice on`（语音到语音）、`/voice tts`（始终语音）、`/voice off`。

---

## 生成额外的 Hermes 实例

将额外的 Hermes 进程作为完全独立的子进程运行 — 单独的会话、工具和环境。

### 何时使用此与 delegate_task

| | `delegate_task` | 生成 `hermes` 进程 |
|-|-----------------|--------------------------|
| 隔离 | 单独的对话，共享进程 | 完全独立的进程 |
| 持续时间 | 分钟（受父循环限制） | 小时/天 |
| 工具访问 | 父工具的子集 | 完整工具访问 |
| 交互式 | 否 | 是（PTY 模式） |
| 用例 | 快速并行子任务 | 长期自主任务 |

### 单次模式

```
terminal(command="hermes chat -q 'Research GRPO papers and write summary to ~/research/grpo.md'", timeout=300)

# 后台处理长任务：
terminal(command="hermes chat -q 'Set up CI/CD for ~/myapp'", background=true)
```

### 交互式 PTY 模式（通过 tmux）

Hermes 使用 prompt_toolkit，它需要真实的终端。使用 tmux 进行交互式生成：

```
# 启动
terminal(command="tmux new-session -d -s agent1 -x 120 -y 40 'hermes'", timeout=10)

# 等待启动，然后发送消息
terminal(command="sleep 8 && tmux send-keys -t agent1 'Build a FastAPI auth service' Enter", timeout=15)

# 读取输出
terminal(command="sleep 20 && tmux capture-pane -t agent1 -p", timeout=5)

# 发送后续
terminal(command="tmux send-keys -t agent1 'Add rate limiting middleware' Enter", timeout=5)

# 退出
terminal(command="tmux send-keys -t agent1 '/exit' Enter && sleep 2 && tmux kill-session -t agent1", timeout=10)
```

### 多代理协调

```
# 代理 A：后端
terminal(command="tmux new-session -d -s backend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t backend 'Build REST API for user management' Enter", timeout=15)

# 代理 B：前端
terminal(command="tmux new-session -d -s frontend -x 120 -y 40 'hermes -w'", timeout=10)
terminal(command="sleep 8 && tmux send-keys -t frontend 'Build React dashboard for user management' Enter", timeout=15)

# 检查进度，在它们之间中继上下文
terminal(command="tmux capture-pane -t backend -p | tail -30", timeout=5)
terminal(command="tmux send-keys -t frontend 'Here is the API schema from the backend agent: ...' Enter", timeout=5)
```

### 会话恢复

```
# 恢复最近的会话
terminal(command="tmux new-session -d -s resumed 'hermes --continue'", timeout=10)

# 恢复特定会话
terminal(command="tmux new-session -d -s resumed 'hermes --resume 20260225_143052_a1b2c3'", timeout=10)
```

### 提示

- **对于快速子任务优先使用 `delegate_task`** — 比生成完整进程开销更少
- **在生成编辑代码的代理时使用 `-w`（工作树模式）** — 防止 git 冲突
- **为单次模式设置超时** — 复杂任务可能需要 5-10 分钟
- **对即发即弃使用 `hermes chat -q`** — 不需要 PTY
- **对交互式会话使用 tmux** — 原始 PTY 模式与 prompt_toolkit 有 `\