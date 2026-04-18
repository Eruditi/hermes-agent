---
sidebar_position: 4
title: "教程：团队 Telegram 助手"
description: "逐步指南，设置一个整个团队都可以用于代码帮助、研究、系统管理等的 Telegram 机器人"
---

# 设置团队 Telegram 助手

本教程将引导您设置一个由 Hermes Agent 驱动的 Telegram 机器人，多个团队成员可以使用。完成后，您的团队将拥有一个共享的 AI 助手，他们可以通过消息寻求代码、研究、系统管理等方面的帮助 — 并通过每用户授权确保安全。

## 我们正在构建什么

一个 Telegram 机器人，它：

- **任何授权的团队成员**都可以通过 DM 寻求帮助 — 代码审查、研究、shell 命令、调试
- **在您的服务器上运行**，具有完整的工具访问权限 — 终端、文件编辑、网络搜索、代码执行
- **每用户会话** — 每个人都有自己的对话上下文
- **默认安全** — 只有经过批准的用户可以交互，有两种授权方法
- **计划任务** — 每日站会、健康检查和提醒发送到团队频道

---

## 先决条件

开始之前，请确保您有：

- **Hermes Agent 安装**在服务器或 VPS 上（不是您的笔记本电脑 — 机器人需要保持运行）。如果尚未安装，请按照[安装指南](/docs/getting-started/installation)进行操作。
- **Telegram 账户**（机器人所有者）
- **配置的 LLM 提供商** — 至少在 `~/.hermes/.env` 中为 OpenAI、Anthropic 或其他支持的提供商设置 API 密钥

:::tip
每月 5 美元的 VPS 足以运行网关。Hermes 本身很轻量级 — 花费金钱的是 LLM API 调用，这些调用在远程发生。
:::

---

## 步骤 1：创建 Telegram 机器人

每个 Telegram 机器人都从 **@BotFather** 开始 — Telegram 官方的机器人创建机器人。

1. **打开 Telegram** 并搜索 `@BotFather`，或访问 [t.me/BotFather](https://t.me/BotFather)

2. **发送 `/newbot`** — BotFather 会询问您两件事：
   - **显示名称** — 用户看到的名称（例如，`Team Hermes Assistant`）
   - **用户名** — 必须以 `bot` 结尾（例如，`myteam_hermes_bot`）

3. **复制机器人令牌** — BotFather 回复类似：
   ```
   使用此令牌访问 HTTP API：
   7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...
   ```
   保存此令牌 — 您将在下一步中需要它。

4. **设置描述**（可选但推荐）：
   ```
   /setdescription
   ```
   选择您的机器人，然后输入类似：
   ```
   由 Hermes Agent 驱动的团队 AI 助手。向我发送消息以获取代码、研究、调试等方面的帮助。
   ```

5. **设置机器人命令**（可选 — 为用户提供命令菜单）：
   ```
   /setcommands
   ```
   选择您的机器人，然后粘贴：
   ```
   new - 开始新对话
   model - 显示或更改 AI 模型
   status - 显示会话信息
   help - 显示可用命令
   stop - 停止当前任务
   ```

:::warning
保持您的机器人令牌保密。任何拥有令牌的人都可以控制机器人。如果泄露，请在 BotFather 中使用 `/revoke` 生成新令牌。
:::

---

## 步骤 2：配置网关

您有两个选项：交互式设置向导（推荐）或手动配置。

### 选项 A：交互式设置（推荐）

```bash
hermes gateway setup
```

这将通过箭头键选择引导您完成所有操作。选择 **Telegram**，粘贴您的机器人令牌，并在提示时输入您的用户 ID。

### 选项 B：手动配置

将这些行添加到 `~/.hermes/.env`：

```bash
# 来自 BotFather 的 Telegram 机器人令牌
TELEGRAM_BOT_TOKEN=7123456789:AAH1bGciOiJSUzI1NiIsInR5cCI6Ikp...

# 您的 Telegram 用户 ID（数字）
TELEGRAM_ALLOWED_USERS=123456789
```

### 查找您的用户 ID

您的 Telegram 用户 ID 是一个数字值（不是您的用户名）。要找到它：

1. 在 Telegram 上向 [@userinfobot](https://t.me/userinfobot) 发送消息
2. 它会立即回复您的数字用户 ID
3. 将该数字复制到 `TELEGRAM_ALLOWED_USERS`

:::info
Telegram 用户 ID 是像 `123456789` 这样的永久数字。它们与您的 `@username` 不同，后者可以更改。始终使用数字 ID 进行允许列表。
:::

---

## 步骤 3：启动网关

### 快速测试

首先在前台运行网关以确保一切正常：

```bash
hermes gateway
```

您应该看到类似的输出：

```
[Gateway] Starting Hermes Gateway...
[Gateway] Telegram adapter connected
[Gateway] Cron scheduler started (tick every 60s)
```

打开 Telegram，找到您的机器人，向它发送消息。如果它回复，您就成功了。按 `Ctrl+C` 停止。

### 生产环境：安装为服务

对于在重启后仍然运行的持久部署：

```bash
hermes gateway install
sudo hermes gateway install --system   # 仅 Linux：启动时系统服务
```

这会创建一个后台服务：默认情况下，Linux 上的用户级 **systemd** 服务，macOS 上的 **launchd** 服务，或者如果您传递 `--system`，则为启动时的 Linux 系统服务。

```bash
# Linux — 管理默认用户服务
hermes gateway start
hermes gateway stop
hermes gateway status

# 查看实时日志
journalctl --user -u hermes-gateway -f

# SSH 注销后保持运行
sudo loginctl enable-linger $USER

# Linux 服务器 — 显式系统服务命令
sudo hermes gateway start --system
sudo hermes gateway status --system
journalctl -u hermes-gateway -f
```

```bash
# macOS — 管理服务
hermes gateway start
hermes gateway stop
tail -f ~/.hermes/logs/gateway.log
```

:::tip macOS PATH
launchd plist 在安装时捕获您的 shell PATH，以便网关子进程可以找到 Node.js 和 ffmpeg 等工具。如果您稍后安装新工具，请重新运行 `hermes gateway install` 来更新 plist。
:::

### 验证它正在运行

```bash
hermes gateway status
```

然后在 Telegram 上向您的机器人发送测试消息。您应该在几秒钟内收到响应。

---

## 步骤 4：设置团队访问

现在让我们为您的团队成员提供访问权限。有两种方法。

### 方法 A：静态允许列表

收集每个团队成员的 Telegram 用户 ID（让他们向 [@userinfobot](https://t.me/userinfobot) 发送消息）并将它们添加为逗号分隔的列表：

```bash
# 在 ~/.hermes/.env 中
TELEGRAM_ALLOWED_USERS=123456789,987654321,555555555
```

更改后重启网关：

```bash
hermes gateway stop && hermes gateway start
```

### 方法 B：DM 配对（团队推荐）

DM 配对更灵活 — 您不需要预先收集用户 ID。工作原理如下：

1. **团队成员向机器人发送 DM** — 由于他们不在允许列表中，机器人会回复一个一次性配对代码：
   ```
   🔐 配对代码：XKGH5N7P
   将此代码发送给机器人所有者以获得批准。
   ```

2. **团队成员向您发送代码**（通过任何渠道 — Slack、电子邮件、面对面）

3. **您在服务器上批准它**：
   ```bash
   hermes pairing approve telegram XKGH5N7P
   ```

4. **他们加入** — 机器人立即开始响应他们的消息

**管理配对用户：**

```bash
# 查看所有待处理和已批准的用户
hermes pairing list

# 撤销某人的访问权限
hermes pairing revoke telegram 987654321

# 清除过期的待处理代码
hermes pairing clear-pending
```

:::tip
DM 配对非常适合团队，因为添加新用户时不需要重启网关。批准立即生效。
:::

### 安全考虑

- **永远不要设置 `GATEWAY_ALLOW_ALL_USERS=true`** 在具有终端访问权限的机器人上 — 任何找到您机器人的人都可以在您的服务器上运行命令
- 配对代码在 **1 小时**后过期并使用加密随机性
- 速率限制防止暴力攻击：每 10 分钟每个用户 1 个请求，每个平台最多 3 个待处理代码
- 5 次失败的批准尝试后，平台进入 1 小时锁定
- 所有配对数据以 `chmod 0600` 权限存储

---

## 步骤 5：配置机器人

### 设置家庭频道

**家庭频道**是机器人发送 cron 任务结果和主动消息的地方。没有它，计划任务就没有地方发送输出。

**选项 1：** 在机器人所在的任何 Telegram 群组或聊天中使用 `/sethome` 命令。

**选项 2：** 在 `~/.hermes/.env` 中手动设置：

```bash
TELEGRAM_HOME_CHANNEL=-1001234567890
TELEGRAM_HOME_CHANNEL_NAME="Team Updates"
```

要找到频道 ID，请将 [@userinfobot](https://t.me/userinfobot) 添加到群组 — 它会报告群组的聊天 ID。

### 配置工具进度显示

控制机器人使用工具时显示的详细程度。在 `~/.hermes/config.yaml` 中：

```yaml
display:
  tool_progress: new    # off | new | all | verbose
```

| 模式 | 您看到的内容 |
|------|-------------|
| `off` | 仅干净的响应 — 无工具活动 |
| `new` | 每个新工具调用的简要状态（消息传递推荐） |
| `all` | 每个工具调用的详细信息 |
| `verbose` | 完整的工具输出，包括命令结果 |

用户也可以在聊天中使用 `/verbose` 命令按会话更改此设置。

### 使用 SOUL.md 设置个性

通过编辑 `~/.hermes/SOUL.md` 自定义机器人的沟通方式：

完整指南，请参阅 [将 SOUL.md 与 Hermes 一起使用](/docs/guides/use-soul-with-hermes)。

```markdown
# Soul
You are a helpful team assistant. Be concise and technical.
Use code blocks for any code. Skip pleasantries — the team
values directness. When debugging, always ask for error logs
before guessing at solutions.
```

### 添加项目上下文

如果您的团队从事特定项目，创建上下文文件以便机器人了解您的技术栈：

```markdown
<!-- ~/.hermes/AGENTS.md -->
# Team Context
- We use Python 3.12 with FastAPI and SQLAlchemy
- Frontend is React with TypeScript
- CI/CD runs on GitHub Actions
- Production deploys to AWS ECS
- Always suggest writing tests for new code
```

:::info
上下文文件被注入到每个会话的系统提示中。保持简洁 — 每个字符都会占用您的令牌预算。
:::

---

## 步骤 6：设置计划任务

随着网关的运行，您可以安排定期任务，将结果传递到您的团队频道。

### 每日站会摘要

在 Telegram 上向机器人发送消息：

```
每个工作日上午 9 点，检查 GitHub 仓库
github.com/myorg/myproject 的：
1. 过去 24 小时内打开/合并的拉取请求
2. 创建或关闭的问题
3. 主分支上的任何 CI/CD 失败
格式为简短的站会风格摘要。
```

代理会自动创建一个 cron 任务，并将结果传递到您提出请求的聊天（或家庭频道）。

### 服务器健康检查

```
每 6 小时，使用 'df -h' 检查磁盘使用情况，使用 'free -h' 检查内存，
并使用 'docker ps' 检查 Docker 容器状态。报告任何异常 —
超过 80% 的分区，已重启的容器，或高内存使用。
```

### 管理计划任务

```bash
# 从 CLI
hermes cron list          # 查看所有计划任务
hermes cron status        # 检查调度程序是否运行

# 从 Telegram 聊天
/cron list                # 查看任务
/cron remove <job_id>     # 删除任务
```

:::warning
Cron 任务提示在完全新鲜的会话中运行，没有对先前对话的记忆。确保每个提示包含**所有**代理需要的上下文 — 文件路径、URL、服务器地址和明确的说明。
:::

---

## 生产提示

### 使用 Docker 确保安全

在共享团队机器人上，使用 Docker 作为终端后端，以便代理命令在容器中而不是在您的主机上运行：

```bash
# 在 ~/.hermes/.env 中
TERMINAL_BACKEND=docker
TERMINAL_DOCKER_IMAGE=nikolaik/python-nodejs:python3.11-nodejs20
```

或在 `~/.hermes/config.yaml` 中：

```yaml
terminal:
  backend: docker
  container_cpu: 1
  container_memory: 5120
  container_persistent: true
```

这样，即使有人要求机器人运行具有破坏性的东西，您的主机系统也会受到保护。

### 监控网关

```bash
# 检查网关是否运行
hermes gateway status

# 观看实时日志（Linux）
journalctl --user -u hermes-gateway -f

# 观看实时日志（macOS）
tail -f ~/.hermes/logs/gateway.log
```

### 保持 Hermes 更新

在 Telegram 上，向机器人发送 `/update` — 它将拉取最新版本并重启。或从服务器：

```bash
hermes update
hermes gateway stop && hermes gateway start
```

### 日志位置

| 内容 | 位置 |
|------|----------|
| 网关日志 | `journalctl --user -u hermes-gateway`（Linux）或 `~/.hermes/logs/gateway.log`（macOS） |
| Cron 任务输出 | `~/.hermes/cron/output/{job_id}/{timestamp}.md` |
| Cron 任务定义 | `~/.hermes/cron/jobs.json` |
| 配对数据 | `~/.hermes/pairing/` |
| 会话历史 | `~/.hermes/sessions/` |

---

## 进一步发展

您已经有了一个工作的团队 Telegram 助手。以下是一些后续步骤：

- **[安全指南](/docs/user-guide/security)** — 深入了解授权、容器隔离和命令批准
- **[消息网关](/docs/user-guide/messaging)** — 网关架构、会话管理和聊天命令的完整参考
- **[Telegram 设置](/docs/user-guide/messaging/telegram)** — 平台特定的详细信息，包括语音消息和 TTS
- **[计划任务](/docs/user-guide/features/cron)** — 具有交付选项和 cron 表达式的高级 cron 调度
- **[上下文文件](/docs/user-guide/features/context-files)** — AGENTS.md、SOUL.md 和 .cursorrules 用于项目知识
- **[个性](/docs/user-guide/features/personality)** — 内置个性预设和自定义角色定义
- **添加更多平台** — 同一个网关可以同时运行 [Discord](/docs/user-guide/messaging/discord)、[Slack](/docs/user-guide/messaging/slack) 和 [WhatsApp](/docs/user-guide/messaging/whatsapp)

---

*有问题或问题？在 GitHub 上打开 issue — 欢迎贡献。*