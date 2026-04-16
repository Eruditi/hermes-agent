---
name: native-mcp
description: 内置MCP（模型上下文协议）客户端，连接到外部MCP服务器，发现它们的工具，并将它们注册为原生Hermes Agent工具。支持stdio和HTTP传输，具有自动重新连接、安全过滤和零配置工具注入。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [MCP, 工具, 集成]
    related_skills: [mcporter]
---

# 原生MCP客户端

Hermes Agent有一个内置的MCP客户端，在启动时连接到MCP服务器，发现它们的工具，并使它们作为代理可以直接调用的一流工具可用。无需桥接CLI — 来自MCP服务器的工具与`terminal`、`read_file`等内置工具一起出现。

## 何时使用

当你想要以下任何情况时使用此技能：
- 连接到MCP服务器并在Hermes Agent中使用它们的工具
- 通过MCP添加外部功能（文件系统访问、GitHub、数据库、API）
- 运行本地基于stdio的MCP服务器（npx、uvx或任何命令）
- 连接到远程HTTP/StreamableHTTP MCP服务器
- 让MCP工具自动发现并在每个对话中可用

对于无需配置任何内容的临时、一次性MCP工具调用，请参阅`mcporter`技能。

## 先决条件

- **mcp Python包** — 可选依赖；用`pip install mcp`安装。如果未安装，MCP支持会被静默禁用。
- **Node.js** — 基于`npx`的MCP服务器（大多数社区服务器）需要
- **uv** — 基于`uvx`的MCP服务器（基于Python的服务器）需要

安装MCP SDK：

```bash
pip install mcp
# 或者，如果使用uv：
uv pip install mcp
```

## 快速开始

在`~/.hermes/config.yaml`中的`mcp_servers`键下添加MCP服务器：

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

重启Hermes Agent。在启动时它将：
1. 连接到服务器
2. 发现可用工具
3. 用前缀`mcp_time_*`注册它们
4. 将它们注入到所有平台工具集中

然后你可以自然地使用工具 — 只需让代理获取当前时间。

## 配置参考

`mcp_servers`下的每个条目都是一个服务器名称映射到其配置。有两种传输类型：**stdio**（基于命令）和**HTTP**（基于URL）。

### Stdio传输（命令 + 参数）

```yaml
mcp_servers:
  server_name:
    command: "npx"             # （必需）要运行的可执行文件
    args: ["-y", "pkg-name"]   # （可选）命令参数，默认：[]
    env:                       # （可选）子进程的环境变量
      SOME_API_KEY: "value"
    timeout: 120               # （可选）每个工具调用的超时（秒），默认：120
    connect_timeout: 60        # （可选）初始连接超时（秒），默认：60
```

### HTTP传输（URL）

```yaml
mcp_servers:
  server_name:
    url: "https://my-server.example.com/mcp"   # （必需）服务器URL
    headers:                                     # （可选）HTTP头
      Authorization: "Bearer sk-..."
    timeout: 180               # （可选）每个工具调用的超时（秒），默认：120
    connect_timeout: 60        # （可选）初始连接超时（秒），默认：60
```

### 所有配置选项

| 选项              | 类型   | 默认值 | 描述                                       |
|-------------------|--------|---------|---------------------------------------------------|
| `command`         | string | --      | 要运行的可执行文件（stdio传输，必需）     |
| `args`            | list   | `[]`    | 传递给命令的参数                   |
| `env`             | dict   | `{}`    | 子进程的额外环境变量    |
| `url`             | string | --      | 服务器URL（HTTP传输，必需）             |
| `headers`         | dict   | `{}`    | 随每个请求发送的HTTP头              |
| `timeout`         | int    | `120`   | 每个工具调用的超时（秒）                  |
| `connect_timeout` | int    | `60`    | 初始连接和发现的超时      |

注意：服务器配置必须具有`command`（stdio）或`url`（HTTP），而不是两者都有。

## 工作原理

### 启动发现

当Hermes Agent启动时，`discover_mcp_tools()`在工具初始化期间被调用：

1. 从`~/.hermes/config.yaml`读取`mcp_servers`
2. 对于每个服务器，在专用后台事件循环中生成连接
3. 初始化MCP会话并调用`list_tools()`以发现可用工具
4. 在Hermes工具注册表中注册每个工具

### 工具命名约定

MCP工具用命名模式注册：

```
mcp_{server_name}_{tool_name}
```

名称中的连字符和点被下划线替换，以与LLM API兼容。

示例：
- 服务器`filesystem`，工具`read_file` → `mcp_filesystem_read_file`
- 服务器`github`，工具`list-issues` → `mcp_github_list_issues`
- 服务器`my-api`，工具`fetch.data` → `mcp_my_api_fetch_data`

### 自动注入

发现后，MCP工具会自动注入到所有`hermes-*`平台工具集（CLI、Discord、Telegram等）。这意味着MCP工具无需任何额外配置即可在每个对话中可用。

### 连接生命周期

- 每个服务器在后台守护进程线程中作为长期存在的asyncio任务运行
- 连接在代理进程的生命周期内持续存在
- 如果连接断开，带有指数退避的自动重新连接会启动（最多5次重试，最大60秒退避）
- 在代理关闭时，所有连接都被优雅地关闭

### 幂等性

`discover_mcp_tools()`是幂等的 — 多次调用它只会连接到尚未连接的服务器。失败的服务器在后续调用中重试。

## 传输类型

### Stdio传输

最常见的传输。Hermes将MCP服务器作为子进程启动，并通过stdin/stdout进行通信。

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/projects"]
```

子进程继承一个**过滤的**环境（请参阅下面的安全部分）加上你在`env`中指定的任何变量。

### HTTP / StreamableHTTP传输

对于远程或共享的MCP服务器。需要`mcp`包包含HTTP客户端支持（`mcp.client.streamable_http`）。

```yaml
mcp_servers:
  remote_api:
    url: "https://mcp.example.com/mcp"
    headers:
      Authorization: "Bearer sk-..."
```

如果你安装的`mcp`版本中没有HTTP支持，服务器将失败并出现ImportError，其他服务器将正常继续。

## 安全

### 环境变量过滤

对于stdio服务器，Hermes**不会**将你的完整shell环境传递给MCP子进程。仅继承安全的基线变量：

- `PATH`、`HOME`、`USER`、`LANG`、`LC_ALL`、`TERM`、`SHELL`、`TMPDIR`
- 任何`XDG_*`变量

所有其他环境变量（API密钥、令牌、机密）都被排除，除非你通过`env`配置键显式添加它们。这可以防止意外的凭据泄露到不受信任的MCP服务器。

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      # 只有这个令牌传递给子进程
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."
```

### 错误消息中的凭据剥离

如果MCP工具调用失败，错误消息中任何类似凭据的模式在显示给LLM之前会被自动编辑。这涵盖：

- GitHub PATs（`ghp_...`）
- OpenAI风格的密钥（`sk-...`）
- Bearer令牌
- 通用`token=`、`key=`、`API_KEY=`、`password=`、`secret=`模式

## 故障排除

### "MCP SDK不可用 — 跳过MCP工具发现"

`mcp` Python包未安装。安装它：

```bash
pip install mcp
```

### "未配置MCP服务器"

`~/.hermes/config.yaml`中没有`mcp_servers`键，或者它是空的。至少添加一个服务器。

### "无法连接到MCP服务器'X'"

常见原因：
- **命令未找到**：`command`二进制文件不在PATH上。确保`npx`、`uvx`或相关命令已安装。
- **包未找到**：对于npx服务器，npm包可能不存在，或者可能需要在args中使用`-y`来自动安装。
- **超时**：服务器启动时间过长。增加`connect_timeout`。
- **端口冲突**：对于HTTP服务器，URL可能无法访问。

### "MCP服务器'X'需要HTTP传输，但mcp.client.streamable_http不可用"

你的`mcp`包版本不包含HTTP客户端支持。升级：

```bash
pip install --upgrade mcp
```

### 工具没有出现

- 检查服务器是否在`mcp_servers`下列出（不是`mcp`或`servers`）
- 确保YAML缩进正确
- 查看Hermes Agent启动日志以获取连接消息
- 工具名称带有`mcp_{server}_{tool}`前缀 — 寻找该模式

### 连接持续断开

客户端使用指数退避（1s、2s、4s、8s、16s，上限为60s）重试最多5次。如果服务器根本无法访问，它会在5次尝试后放弃。检查服务器进程和网络连接。

## 示例

### 时间服务器（uvx）

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]
```

注册像`mcp_time_get_current_time`这样的工具。

### 文件系统服务器（npx）

```yaml
mcp_servers:
  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/home/user/documents"]
    timeout: 30
```

注册像`mcp_filesystem_read_file`、`mcp_filesystem_write_file`、`mcp_filesystem_list_directory`这样的工具。

### 带身份验证的GitHub服务器

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxx"
    timeout: 60
```

注册像`mcp_github_list_issues`、`mcp_github_create_pull_request`等工具。

### 远程HTTP服务器

```yaml
mcp_servers:
  company_api:
    url: "https://mcp.mycompany.com/v1/mcp"
    headers:
      Authorization: "Bearer sk-xxxxxxxxxxxxxxxxxxxx"
      X-Team-Id: "engineering"
    timeout: 180
    connect_timeout: 30
```

### 多个服务器

```yaml
mcp_servers:
  time:
    command: "uvx"
    args: ["mcp-server-time"]

  filesystem:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-filesystem", "/tmp"]

  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_xxxxxxxxxxxxxxxxxxxx"

  company_api:
    url: "https://mcp.internal.company.com/mcp"
    headers:
      Authorization: "Bearer sk-xxxxxxxxxxxxxxxxxxxx"
    timeout: 300
```

所有服务器的所有工具都被注册并同时可用。每个服务器的工具都带有其名称前缀，以避免冲突。

## 采样（服务器发起的LLM请求）

Hermes支持MCP的`sampling/createMessage`功能 — MCP服务器可以在工具执行期间通过代理请求LLM完成。这启用了代理在循环中的工作流（数据分析、内容生成、决策制定）。

采样**默认启用**。为每个服务器配置：

```yaml
mcp_servers:
  my_server:
    command: "npx"
    args: ["-y", "my-mcp-server"]
    sampling:
      enabled: true           # 默认：true
      model: "gemini-3-flash" # 模型覆盖（可选）
      max_tokens_cap: 4096    # 每个请求的最大令牌
      timeout: 30             # LLM调用超时（秒）
      max_rpm: 10             # 每分钟最大请求数
      allowed_models: []      # 模型白名单（空 = 所有）
      max_tool_rounds: 5      # 工具循环限制（0 = 禁用）
      log_level: "info"       # 审计详细程度
```

服务器还可以在采样请求中包含`tools`以进行多轮工具增强工作流。`max_tool_rounds`配置防止无限工具循环。每个服务器的审计指标（请求、错误、令牌、工具使用计数）通过`get_mcp_status()`进行跟踪。

对于不受信任的服务器，使用`sampling: { enabled: false }`禁用采样。

## 注意

- MCP工具从代理的角度同步调用，但在专用后台事件循环上异步运行
- 工具结果作为JSON返回，带有`{"result": "..."}`或`{"error": "..."}`
- 原生MCP客户端独立于`mcporter` — 你可以同时使用两者
- 服务器连接是持久的，并在同一代理进程中的所有对话中共享
- 添加或删除服务器需要重启代理（当前没有热重载）
