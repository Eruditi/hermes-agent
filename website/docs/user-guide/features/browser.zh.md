---
title: "浏览器自动化"
description: "使用多个提供程序、通过 CDP 的本地 Chrome 或云浏览器控制浏览器，用于 Web 交互、表单填写、抓取等。"
sidebar_label: "浏览器"
sidebar_position: 5
---

# 浏览器自动化

Hermes Agent 包含具有多个后端选项的完整浏览器自动化工具集：

- **Browserbase 云模式** 通过 [Browserbase](https://browserbase.com) 用于托管云浏览器和反机器人工具
- **Browser Use 云模式** 通过 [Browser Use](https://browser-use.com) 作为替代云浏览器提供程序
- **Firecrawl 云模式** 通过 [Firecrawl](https://firecrawl.dev) 用于带有内置抓取的云浏览器
- **Camofox 本地模式** 通过 [Camofox](https://github.com/jo-inc/camofox-browser) 用于本地反检测浏览（基于 Firefox 的指纹欺骗）
- **通过 CDP 的本地 Chrome** — 使用 `/browser connect` 将浏览器工具连接到您自己的 Chrome 实例
- **本地浏览器模式** 通过 `agent-browser` CLI 和本地 Chromium 安装

在所有模式中，代理可以导航网站、与页面元素交互、填写表单和提取信息。

## 概述

页面被表示为**可访问性树**（基于文本的快照），使其非常适合 LLM 代理。交互式元素获得代理用于点击和键入的 ref ID（如 `@e1`、`@e2`）。

主要功能：

- **多提供程序云执行** — Browserbase、Browser Use 或 Firecrawl — 无需本地浏览器
- **本地 Chrome 集成** — 通过 CDP 附加到您运行的 Chrome 以进行实际浏览
- **内置隐身** — 随机指纹、CAPTCHA 解决、住宅代理（Browserbase）
- **会话隔离** — 每个任务都有自己的浏览器会话
- **自动清理** — 非活动会话在超时后关闭
- **视觉分析** — 截图 + AI 分析用于视觉理解

## 设置

:::tip Nous 订阅者
如果您有付费的 [Nous Portal](https://portal.nousresearch.com) 订阅，您可以通过**[工具网关](tool-gateway.md)**使用浏览器自动化，无需任何单独的 API 密钥。运行 `hermes model` 或 `hermes tools` 启用它。
:::

### Browserbase 云模式

要使用 Browserbase 托管的云浏览器，请添加：

```bash
# 添加到 ~/.hermes/.env
BROWSERBASE_API_KEY=***
BROWSERBASE_PROJECT_ID=your-project-id-here
```

在 [browserbase.com](https://browserbase.com) 获取您的凭据。

### Browser Use 云模式

要使用 Browser Use 作为您的云浏览器提供程序，请添加：

```bash
# 添加到 ~/.hermes/.env
BROWSER_USE_API_KEY=***
```

在 [browser-use.com](https://browser-use.com) 获取您的 API 密钥。Browser Use 通过其 REST API 提供云浏览器。如果同时设置了 Browserbase 和 Browser Use 凭据，则 Browserbase 优先。

### Firecrawl 云模式

要使用 Firecrawl 作为您的云浏览器提供程序，请添加：

```bash
# 添加到 ~/.hermes/.env
FIRECRAWL_API_KEY=fc-***
```

在 [firecrawl.dev](https://firecrawl.dev) 获取您的 API 密钥。然后选择 Firecrawl 作为您的浏览器提供程序：

```bash
hermes setup tools
# → Browser Automation → Firecrawl
```

可选设置：

```bash
# 自托管 Firecrawl 实例（默认：https://api.firecrawl.dev）
FIRECRAWL_API_URL=http://localhost:3002

# 会话 TTL（秒）（默认：300）
FIRECRAWL_BROWSER_TTL=600
```

### Camofox 本地模式

[Camofox](https://github.com/jo-inc/camofox-browser) 是一个自托管的 Node.js 服务器，包装了 Camoufox（一个带有 C++ 指纹欺骗的 Firefox 分支）。它提供没有云依赖项的本地反检测浏览。

```bash
# 安装并运行
git clone https://github.com/jo-inc/camofox-browser && cd camofox-browser
npm install && npm start   # 第一次运行时下载 Camoufox（~300MB）

# 或通过 Docker
docker run -d --network host -e CAMOFOX_PORT=9377 jo-inc/camofox-browser
```

然后在 `~/.hermes/.env` 中设置：

```bash
CAMOFOX_URL=http://localhost:9377
```

或通过 `hermes tools` → Browser Automation → Camofox 配置。

当设置了 `CAMOFOX_URL` 时，所有浏览器工具会自动通过 Camofox 而不是 Browserbase 或 agent-browser 路由。

#### 持久浏览器会话

默认情况下，每个 Camofox 会话都会获得一个随机身份 — cookie 和登录不会在代理重启后保留。要启用持久浏览器会话，请将以下内容添加到 `~/.hermes/config.yaml`：

```yaml
browser:
  camofox:
    managed_persistence: true
```

然后完全重启 Hermes，以便新配置被拾取。

:::warning 嵌套路径很重要
Hermes 读取 `browser.camofox.managed_persistence`，**而不是**顶级的 `managed_persistence`。一个常见的错误是写：

```yaml
# ❌ 错误 — Hermes 忽略这个
managed_persistence: true
```

如果标志放置在错误的路径，Hermes 会静默回退到随机的临时 `userId`，并且您的登录状态将在每个会话中丢失。
:::

##### Hermes 做什么
- 向 Camofox 发送确定性的配置文件作用域 `userId`，以便服务器可以在会话之间重用相同的 Firefox 配置文件。
- 在清理时跳过服务器端上下文销毁，以便 cookie 和登录在代理任务之间保留。
- 将 `userId` 作用域到活动的 Hermes 配置文件，以便不同的 Hermes 配置文件获得不同的浏览器配置文件（配置文件隔离）。

##### Hermes 不做什么
- 它不会在 Camofox 服务器上强制持久化。Hermes 只发送一个稳定的 `userId`；服务器必须通过将该 `userId` 映射到持久的 Firefox 配置文件目录来遵守它。
- 如果您的 Camofox 服务器构建将每个请求视为临时的（例如，总是调用 `browser.newContext()` 而不加载存储的配置文件），Hermes 无法使这些会话持久化。确保您运行的 Camofox 构建实现了基于 userId 的配置文件持久化。

##### 验证它是否工作

1. 启动 Hermes 和您的 Camofox 服务器。
2. 在浏览器任务中打开 Google（或任何登录站点）并手动登录。
3. 正常结束浏览器任务。
4. 开始新的浏览器任务。
5. 再次打开同一站点 — 您应该仍然登录。

如果步骤 5 将您登出，则 Camofox 服务器没有遵守稳定的 `userId`。仔细检查您的配置路径，确认您在编辑 `config.yaml` 后完全重启了 Hermes，并验证您的 Camofox 服务器版本支持每个用户的持久配置文件。

##### 状态存储位置

Hermes 从配置文件作用域目录 `~/.hermes/browser_auth/camofox/`（或非默认配置文件在 `$HERMES_HOME` 下的等效目录）派生稳定的 `userId`。实际的浏览器配置文件数据存储在 Camofox 服务器端，由该 `userId` 键入。要完全重置持久配置文件，请在 Camofox 服务器上清除它，并删除相应的 Hermes 配置文件的状态目录。

#### VNC 实时视图

当 Camofox 以有头模式运行（带有可见的浏览器窗口）时，它会在其健康检查响应中暴露一个 VNC 端口。Hermes 自动发现这一点，并在导航响应中包含 VNC URL，因此代理可以共享一个链接供您实时观看浏览器。

### 通过 CDP 的本地 Chrome（`/browser connect`）

您可以通过 Chrome DevTools 协议（CDP）将 Hermes 浏览器工具附加到您自己运行的 Chrome 实例，而不是云提供程序。当您想要实时查看代理正在做什么、与需要您自己的 cookie/会话的页面交互或避免云浏览器成本时，这很有用。

在 CLI 中，使用：

```
/browser connect              # 连接到 ws://localhost:9222 处的 Chrome
/browser connect ws://host:port  # 连接到特定 CDP 端点
/browser status               # 检查当前连接
/browser disconnect            # 分离并返回云/本地模式
```

如果 Chrome 尚未启用远程调试运行，Hermes 将尝试使用 `--remote-debugging-port=9222` 自动启动它。

:::tip
要手动启动启用 CDP 的 Chrome：
```bash
# Linux
google-chrome --remote-debugging-port=9222

# macOS
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --remote-debugging-port=9222
```
:::

通过 CDP 连接时，所有浏览器工具（`browser_navigate`、`browser_click` 等）都在您的实时 Chrome 实例上运行，而不是启动云会话。

### 本地浏览器模式

如果您**没有**设置任何云凭据也不使用 `/browser connect`，Hermes 仍然可以通过由 `agent-browser` 驱动的本地 Chromium 安装使用浏览器工具。

### 可选环境变量

```bash
# 用于更好的 CAPTCHA 解决的住宅代理（默认："true"）
BROWSERBASE_PROXIES=true

# 使用自定义 Chromium 的高级隐身 — 需要 Scale Plan（默认："false"）
BROWSERBASE_ADVANCED_STEALTH=false

# 断开连接后的会话重新连接 — 需要付费计划（默认："true"）
BROWSERBASE_KEEP_ALIVE=true

# 自定义会话超时（毫秒）（默认：项目默认）
# 示例：600000（10 分钟）、1800000（30 分钟）
BROWSERBASE_SESSION_TIMEOUT=600000

# 自动清理前的非活动超时（秒）（默认：120）
BROWSER_INACTIVITY_TIMEOUT=120
```

### 安装 agent-browser CLI

```bash
npm install -g agent-browser
# 或在仓库中本地安装：
npm install
```

:::info
`browser` 工具集必须包含在您配置的 `toolsets` 列表中，或通过 `hermes config set toolsets '["hermes-cli", "browser"]'` 启用。
:::

## 可用工具

### `browser_navigate`

导航到 URL。必须在任何其他浏览器工具之前调用。初始化 Browserbase 会话。

```
Navigate to https://github.com/NousResearch
```

:::tip
对于简单的信息检索，首选 `web_search` 或 `web_extract` — 它们更快更便宜。当您需要**交互**页面时（点击按钮、填写表单、处理动态内容）使用浏览器工具。
:::

### `browser_snapshot`

获取当前页面可访问性树的基于文本的快照。返回带有 ref ID（如 `@e1`、`@e2`）的交互式元素，以供 `browser_click` 和 `browser_type` 使用。

- **`full=false`**（默认）：仅显示交互式元素的紧凑视图
- **`full=true`**：完整页面内容

超过 8000 字符的快照会由 LLM 自动摘要。

### `browser_click`

点击由快照中的 ref ID 标识的元素。

```
Click @e5 to press the "Sign In" button
```

### `browser_type`

将文本键入输入字段。首先清除字段，然后键入新文本。

```
Type "hermes agent" into the search field @e3
```

### `browser_scroll`

向上或向下滚动页面以显示更多内容。

```
Scroll down to see more results
```

### `browser_press`

按下键盘键。对于提交表单或导航很有用。

```
Press Enter to submit the form
```

支持的键：`Enter`、`Tab`、`Escape`、`ArrowDown`、`ArrowUp` 等。

### `browser_back`

导航回浏览器历史记录中的上一页。

### `browser_get_images`

列出当前页面上的所有图像及其 URL 和 alt 文本。对于查找要分析的图像很有用。

### `browser_vision`

截取屏幕截图并使用视觉 AI 分析它。当文本快照没有捕获重要的视觉信息时使用此选项 — 对于 CAPTCHA、复杂布局或视觉验证挑战特别有用。

屏幕截图被持久保存，文件路径与 AI 分析一起返回。在消息平台（Telegram、Discord、Slack、WhatsApp）上，您可以要求代理共享屏幕截图 — 它将通过 `MEDIA:` 机制作为原生照片附件发送。

```
What does the chart on this page show?
```

屏幕截图存储在 `~/.hermes/cache/screenshots/` 中，并在 24 小时后自动清理。

### `browser_console`

从当前页面获取浏览器控制台输出（日志/警告/错误消息）和未捕获的 JavaScript 异常。对于检测不出现在可访问性树中的静默 JS 错误至关重要。

```
Check the browser console for any JavaScript errors
```

使用 `clear=True` 在读取后清除控制台，以便后续调用仅显示新消息。

## 实际示例

### 填写 Web 表单

```
User: Sign up for an account on example.com with my email john@example.com

Agent workflow:
1. browser_navigate("https://example.com/signup")
2. browser_snapshot()  → 看到带有 refs 的表单字段
3. browser_type(ref="@e3", text="john@example.com")
4. browser_type(ref="@e5", text="SecurePass123")
5. browser_click(ref="@e8")  → 点击"Create Account"
6. browser_snapshot()  → 确认成功
```

### 研究动态内容

```
User: What are the top trending repos on GitHub right now?

Agent workflow:
1. browser_navigate("https://github.com/trending")
2. browser_snapshot(full=true)  → 读取趋势仓库列表
3. 返回格式化结果
```

## 会话录制

自动将浏览器会话录制为 WebM 视频文件：

```yaml
browser:
  record_sessions: true  # default: false
```

启用后，录制在第一个 `browser_navigate` 时自动开始，并在会话关闭时保存到 `~/.hermes/browser_recordings/`。在本地和云（Browserbase）模式下都有效。超过 72 小时的录制会自动清理。

## 隐身功能

Browserbase 提供自动隐身功能：

| 功能 | 默认 | 备注 |
|---------|---------|-------|
| 基本隐身 | 始终开启 | 随机指纹、视口随机化、CAPTCHA 解决 |
| 住宅代理 | 开启 | 通过住宅 IP 路由以获得更好的访问权限 |
| 高级隐身 | 关闭 | 自定义 Chromium 构建，需要 Scale Plan |
| 保持活动 | 开启 | 网络中断后的会话重新连接 |

:::note
如果付费功能在您的计划中不可用，Hermes 会自动回退 — 首先禁用 `keepAlive`，然后是代理 — 因此浏览在免费计划上仍然有效。
:::

## 会话管理

- 每个任务都通过 Browserbase 获得隔离的浏览器会话
- 会话在非活动后自动清理（默认：2 分钟）
- 后台线程每 30 秒检查一次陈旧会话
- 紧急清理在进程退出时运行以防止孤立会话
- 会话通过 Browserbase API（`REQUEST_RELEASE` 状态）释放

## 限制

- **基于文本的交互** — 依赖可访问性树，而不是像素坐标
- **快照大小** — 大页面可能在 8000 字符处被截断或由 LLM 摘要
- **会话超时** — 云会话根据您提供程序的计划设置过期
- **成本** — 云会话消耗提供程序积分；会话在对话结束或非活动后自动清理。使用 `/browser connect` 进行免费的本地浏览。
- **无文件下载** — 无法从浏览器下载文件
