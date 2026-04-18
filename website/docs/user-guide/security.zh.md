---
sidebar_position: 8
title: "安全"
description: "安全模型、危险命令审批、用户授权、容器隔离和生产部署最佳实践"
---

# 安全

Hermes Agent 采用纵深防御安全模型设计。本页面涵盖每个安全边界 —— 从命令审批到容器隔离再到消息平台上的用户授权。

## 概述

安全模型有七层：

1. **用户授权** —— 谁可以与代理交谈（允许列表、DM 配对）
2. **危险命令审批** —— 破坏性操作的人工参与
3. **容器隔离** —— 带有强化设置的 Docker/Singularity/Modal 沙箱
4. **MCP 凭据过滤** —— MCP 子进程的环境变量隔离
5. **上下文文件扫描** —— 项目文件中的提示注入检测
6. **跨会话隔离** —— 会话无法访问彼此的数据或状态；定时任务存储路径针对路径遍历攻击进行了强化
7. **输入清理** —— 终端工具后端中的工作目录参数根据允许列表进行验证以防止 shell 注入

## 危险命令审批

在执行任何命令之前，Hermes 会根据精心策划的危险模式列表检查它。如果找到匹配项，用户必须明确批准。

### 审批模式

审批系统支持三种模式，通过 `~/.hermes/config.yaml` 中的 `approvals.mode` 配置：

```yaml
approvals:
  mode: manual    # manual | smart | off
  timeout: 60     # 等待用户响应的秒数（默认：60）
```

| 模式 | 行为 |
|------|----------|
| **manual**（默认） | 始终提示用户批准危险命令 |
| **smart** | 使用辅助 LLM 评估风险。低风险命令（例如 `python -c "print('hello')"`）会自动批准。真正危险的命令会自动拒绝。不确定的情况会升级到手动提示。 |
| **off** | 禁用所有审批检查 —— 等同于使用 `--yolo` 运行。所有命令在没有提示的情况下执行。 |

:::warning
设置 `approvals.mode: off` 会禁用所有安全提示。仅在受信任的环境（CI/CD、容器等）中使用。
:::

### YOLO 模式

YOLO 模式会绕过当前会话的 **所有** 危险命令审批提示。它可以通过三种方式激活：

1. **CLI 标志**：使用 `hermes --yolo` 或 `hermes chat --yolo` 启动会话
2. **斜杠命令**：在会话期间键入 `/yolo` 以切换它开/关
3. **环境变量**：设置 `HERMES_YOLO_MODE=1`

`/yolo` 命令是一个 **切换** —— 每次使用都会翻转模式开或关：

```
> /yolo
  ⚡ YOLO mode ON — all commands auto-approved. Use with caution.

> /yolo
  ⚠ YOLO mode OFF — dangerous commands will require approval.
```

YOLO 模式在 CLI 和网话会话中都可用。在内部，它设置 `HERMES_YOLO_MODE` 环境变量，该变量在每次命令执行之前都会被检查。

:::danger
YOLO 模式会禁用会话的 **所有** 危险命令安全检查。仅当你完全信任正在生成的命令时才使用（例如，在一次性环境中经过充分测试的自动化脚本）。
:::

### 审批超时

当出现危险命令提示时，用户有可配置的时间来响应。如果在超时时间内没有给出响应，默认情况下命令会被**拒绝**（故障关闭）。

在 `~/.hermes/config.yaml` 中配置超时：

```yaml
approvals:
  timeout: 60  # 秒（默认：60）
```

### 什么触发审批

以下模式触发审批提示（在 `tools/approval.py` 中定义）：

| 模式 | 描述 |
|---------|-------------|
| `rm -r` / `rm --recursive` | 递归删除 |
| `rm ... /` | 在根路径中删除 |
| `chmod 777/666` / `o+w` / `a+w` | 全球/其他可写权限 |
| 带有不安全权限的 `chmod --recursive` | 递归全球/其他可写（长标志） |
| `chown -R root` / `chown --recursive root` | 递归 chown 到 root |
| `mkfs` | 格式化文件系统 |
| `dd if=` | 磁盘复制 |
| `> /dev/sd` | 写入块设备 |
| `DROP TABLE/DATABASE` | SQL DROP |
| 没有 WHERE 的 `DELETE FROM` | 没有 WHERE 的 SQL DELETE |
| `TRUNCATE TABLE` | SQL TRUNCATE |
| `> /etc/` | 覆盖系统配置 |
| `systemctl stop/disable/mask` | 停止/禁用系统服务 |
| `kill -9 -1` | 杀死所有进程 |
| `pkill -9` | 强制杀死进程 |
| Fork bomb 模式 | Fork bombs |
| `bash -c` / `sh -c` / `zsh -c` / `ksh -c` | 通过 `-c` 标志执行 shell 命令（包括组合标志如 `-lc`） |
| `python -e` / `perl -e` / `ruby -e` / `node -c` | 通过 `-e`/`-c` 标志执行脚本 |
| `curl ... \| sh` / `wget ... \| sh` | 将远程内容管道传输到 shell |
| `bash <(curl ...)` / `sh <(wget ...)` | 通过进程替换执行远程脚本 |
| `tee` 到 `/etc/`、`~/.ssh/`、`~/.hermes/.env` | 通过 tee 覆盖敏感文件 |
| `>` / `>>` 到 `/etc/`、`~/.ssh/`、`~/.hermes/.env` | 通过重定向覆盖敏感文件 |
| `xargs rm` | 带有 rm 的 xargs |
| `find -exec rm` / `find -delete` | 带有破坏性操作的 find |
| `cp`/`mv`/`install` 到 `/etc/` | 将文件复制/移动到系统配置 |
| `/etc/` 上的 `sed -i` / `sed --in-place` | 就地编辑系统配置 |
| `pkill`/`killall` hermes/gateway | 自终止预防 |
| 带有 `&`/`disown`/`nohup`/`setsid` 的 `gateway run` | 防止在服务管理器之外启动网关 |

:::info
**容器绕过**：当在 `docker`、`singularity`、`modal` 或 `daytona` 后端中运行时，危险命令检查会被**跳过**，因为容器本身就是安全边界。容器内的破坏性命令不会损害主机。
:::

### 审批流程（CLI）

在交互式 CLI 中，危险命令显示内联审批提示：

```
  ⚠️  DANGEROUS COMMAND: recursive delete
      rm -rf /tmp/old-project

      [o]nce  |  [s]ession  |  [a]lways  |  [d]eny

      Choice [o/s/a/D]:
```

四个选项：

- **once** —— 允许这一次执行
- **session** —— 允许会话其余部分的此模式
- **always** —— 添加到永久允许列表（保存到 `config.yaml`）
- **deny**（默认）—— 阻止命令

### 审批流程（网关/消息）

在消息平台上，代理将危险命令详细信息发送到聊天并等待用户回复：

- 回复 **yes**、**y**、**approve**、**ok** 或 **go** 以批准
- 回复 **no**、**n**、**deny** 或 **cancel** 以拒绝

运行网关时会自动设置 `HERMES_EXEC_ASK=1` 环境变量。

### 永久允许列表

使用 "always" 批准的命令保存到 `~/.hermes/config.yaml`：

```yaml
# 永久允许的危险命令模式
command_allowlist:
  - rm
  - systemctl
```

这些模式在启动时加载，并在所有未来会话中静默批准。

:::tip
使用 `hermes config edit` 查看或从你的永久允许列表中删除模式。
:::

## 用户授权（网关）

运行消息网关时，Hermes 通过分层授权系统控制谁可以与机器人交互。

### 授权检查顺序

`_is_user_authorized()` 方法按此顺序检查：

1. **每个平台的允许所有标志**（例如 `DISCORD_ALLOW_ALL_USERS=true`）
2. **DM 配对批准列表**（通过配对代码批准的用户）
3. **特定平台的允许列表**（例如 `TELEGRAM_ALLOWED_USERS=12345,67890`）
4. **全局允许列表**（`GATEWAY_ALLOWED_USERS=12345,67890`）
5. **全局允许所有**（`GATEWAY_ALLOW_ALL_USERS=true`）
6. **默认：拒绝**

### 平台允许列表

在 `~/.hermes/.env` 中将允许的用户 ID 设置为逗号分隔值：

```bash
# 特定平台的允许列表
TELEGRAM_ALLOWED_USERS=123456789,987654321
DISCORD_ALLOWED_USERS=111222333444555666
WHATSAPP_ALLOWED_USERS=15551234567
SLACK_ALLOWED_USERS=U01ABC123

# 跨平台允许列表（对所有平台检查）
GATEWAY_ALLOWED_USERS=123456789

# 每个平台的允许所有（谨慎使用）
DISCORD_ALLOW_ALL_USERS=true

# 全局允许所有（极其谨慎使用）
GATEWAY_ALLOW_ALL_USERS=true
```

:::warning
如果**没有配置允许列表**并且未设置 `GATEWAY_ALLOW_ALL_USERS`，则**所有用户都被拒绝**。网关在启动时记录警告：

```
No user allowlists configured. All unauthorized users will be denied.
Set GATEWAY_ALLOW_ALL_USERS=true in ~/.hermes/.env to allow open access,
or configure platform allowlists (e.g., TELEGRAM_ALLOWED_USERS=your_id).
```
:::

### DM 配对系统

为了更灵活的授权，Hermes 包含一个基于代码的配对系统。不需要预先提供用户 ID，未知用户会收到一个机器人所有者通过 CLI 批准的一次性配对代码。

**它的工作原理：**

1. 未知用户向机器人发送 DM
2. 机器人回复一个 8 字符的配对代码
3. 机器人所有者在 CLI 上运行 `hermes pairing approve <platform> <code>`
4. 用户被永久批准用于该平台

在 `~/.hermes/config.yaml` 中控制如何处理未经授权的直接消息：

```yaml
unauthorized_dm_behavior: pair

whatsapp:
  unauthorized_dm_behavior: ignore
```

- `pair` 是默认值。未经授权的 DM 会收到配对代码回复。
- `ignore` 静默丢弃未经授权的 DM。
- 平台部分覆盖全局默认值，因此你可以在 Telegram 上保持配对，同时保持 WhatsApp 静默。

**安全功能**（基于 OWASP + NIST SP 800-63-4 指南）：

| 功能 | 详情 |
|---------|---------|
| 代码格式 | 来自 32 字符无歧义字母表的 8 字符（无 0/O/1/I） |
| 随机性 | 加密（`secrets.choice()`） |
| 代码 TTL | 1 小时过期 |
| 速率限制 | 每 10 分钟每个用户 1 个请求 |
| 待处理限制 | 每个平台最多 3 个待处理代码 |
| 锁定 | 5 次失败的审批尝试 → 1 小时锁定 |
| 文件安全性 | 所有配对数据文件上的 `chmod 0600` |
| 日志记录 | 代码永远不会记录到 stdout |

**配对 CLI 命令：**

```bash
# 列出待处理和已批准的用户
hermes pairing list

# 批准配对代码
hermes pairing approve telegram ABC12DEF

# 撤销用户的访问权限
hermes pairing revoke telegram 123456789

# 清除所有待处理代码
hermes pairing clear-pending
```

**存储：** 配对数据存储在 `~/.hermes/pairing/` 中，带有按平台的 JSON 文件：
- `{platform}-pending.json` —— 待处理的配对请求
- `{platform}-approved.json` —— 已批准的用户
- `_rate_limits.json` —— 速率限制和锁定跟踪

## 容器隔离

当使用 `docker` 终端后端时，Hermes 对每个容器应用严格的安全强化。

### Docker 安全标志

每个容器都使用这些标志运行（在 `tools/environments/docker.py` 中定义）：

```python
_SECURITY_ARGS = [
    "--cap-drop", "ALL",                          # 放弃所有 Linux 功能
    "--cap-add", "DAC_OVERRIDE",                  # Root 可以写入绑定挂载的目录
    "--cap-add", "CHOWN",                         # 包管理器需要文件所有权
    "--cap-add", "FOWNER",                        # 包管理器需要文件所有权
    "--security-opt", "no-new-privileges",         # 阻止权限提升
    "--pids-limit", "256",                         # 限制进程数
    "--tmpfs", "/tmp:rw,nosuid,size=512m",         # 大小受限的 /tmp
    "--tmpfs", "/var/tmp:rw,noexec,nosuid,size=256m",  # 无执行 /var/tmp
    "--tmpfs", "/run:rw,noexec,nosuid,size=64m",   # 无执行 /run
]
```

### 资源限制

容器资源在 `~/.hermes/config.yaml` 中可配置：

```yaml
terminal:
  backend: docker
  docker_image: "nikolaik/python-nodejs:python3.11-nodejs20"
  docker_forward_env: []  # 仅显式允许列表；为空会将密钥排除在容器之外
  container_cpu: 1        # CPU 核数
  container_memory: 5120  # MB（默认 5GB）
  container_disk: 51200   # MB（默认 50GB，需要 XFS 上的 overlay2）
  container_persistent: true  # 在会话之间持久化文件系统
```

### 文件系统持久性

- **持久模式**（`container_persistent: true`）：从 `~/.hermes/sandboxes/docker/<task_id>/` 绑定挂载 `/workspace` 和 `/root`
- **临时模式**（`container_persistent: false`）：对工作区使用 tmpfs —— 清理时所有内容都会丢失

:::tip
对于生产网关部署，使用 `docker`、`modal` 或 `daytona` 后端将代理命令与你的主机系统隔离。这完全消除了对危险命令审批的需要。
:::

:::warning
如果你将名称添加到 `terminal.docker_forward_env`，这些变量会被有意注入到容器中用于终端命令。这对于任务特定的凭据（如 `GITHUB_TOKEN`）很有用，但这也意味着在容器中运行的代码可以读取和泄露它们。
:::

## 终端后端安全比较

| 后端 | 隔离 | 危险命令检查 | 最适合 |
|---------|-----------|-------------------|----------|
| **local** | 无 —— 在主机上运行 | ✅ 是 | 开发、受信任的用户 |
| **ssh** | 远程机器 | ✅ 是 | 在单独的服务器上运行 |
| **docker** | 容器 | ❌ 跳过（容器是边界） | 生产网关 |
| **singularity** | 容器 | ❌ 跳过 | HPC 环境 |
| **modal** | 云沙箱 | ❌ 跳过 | 可扩展的云隔离 |
| **daytona** | 云沙箱 | ❌ 跳过 | 持久云工作区 |

## 环境变量传递 {#environment-variable-passthrough}

`execute_code` 和 `terminal` 都会从子进程中剥离敏感的环境变量，以防止 LLM 生成的代码泄露凭据。但是，声明 `required_environment_variables` 的技能合法地需要访问这些变量。

### 它的工作原理

两种机制允许特定变量通过沙箱过滤器：

**1. 技能范围传递（自动）**

当加载技能（通过 `skill_view` 或 `/skill` 命令）并声明 `required_environment_variables` 时，环境中实际设置的任何这些变量都会自动注册为传递。缺失的变量（仍处于需要设置状态）**不会**被注册。

```yaml
# 在技能的 SKILL.md 前置元数据中
required_environment_variables:
  - name: TENOR_API_KEY
    prompt: Tenor API key
    help: Get a key from https://developers.google.com/tenor
```

加载此技能后，`TENOR_API_KEY` 会传递到 `execute_code`、`terminal`（本地）、**和远程后端（Docker、Modal）** —— 无需手动配置。

:::info Docker & Modal
在 v0.5.1 之前，Docker 的 `forward_env` 是一个与技能传递分离的系统。它们现在已合并 —— 技能声明的 env 变量会自动转发到 Docker 容器和 Modal 沙箱，无需手动将它们添加到 `docker_forward_env`。
:::

**2. 基于配置的传递（手动）**

对于任何技能未声明的 env 变量，将它们添加到 `config.yaml` 中的 `terminal.env_passthrough`：

```yaml
terminal:
  env_passthrough:
    - MY_CUSTOM_KEY
    - ANOTHER_TOKEN
```

### 凭据文件传递（OAuth 令牌等）{#credential-file-passthrough}

一些技能需要**文件**（不仅仅是 env 变量）在沙箱中 —— 例如，Google Workspace 将 OAuth 令牌存储为活动配置文件的 `HERMES_HOME` 下的 `google_token.json`。技能在前置元数据中声明这些：

```yaml
required_credential_files:
  - path: google_token.json
    description: Google OAuth2 token (created by setup script)
  - path: google_client_secret.json
    description: Google OAuth2 client credentials
```

加载后，Hermes 检查这些文件是否存在于活动配置文件的 `HERMES_HOME` 中并注册它们以进行挂载：

- **Docker**：只读绑定挂载（`-v host:container:ro`）
- **Modal**：在沙箱创建时挂载 + 在每个命令之前同步（处理会话中期 OAuth 设置）
- **Local**：无需操作（文件已可访问）

你也可以在 `config.yaml` 中手动列出凭据文件：

```yaml
terminal:
  credential_files:
    - google_token.json
    - my_custom_oauth_token.json
```

路径相对于 `~/.hermes/`。文件挂载到容器内的 `/root/.hermes/`。

### 每个沙箱过滤什么

| 沙箱 | 默认过滤器 | 传递覆盖 |
|---------|---------------|---------------------|
| **execute_code** | 阻止名称中包含 `KEY`、`TOKEN`、`SECRET`、`PASSWORD`、`CREDENTIAL`、`PASSWD`、`AUTH` 的变量；仅允许安全前缀变量通过 | ✅ 传递变量绕过两个检查 |
| **terminal**（本地） | 阻止显式 Hermes 基础设施变量（提供程序密钥、网关令牌、工具 API 密钥） | ✅ 传递变量绕过阻止列表 |
| **terminal**（Docker） | 默认情况下没有主机 env 变量 | ✅ 传递变量 + `docker_forward_env` 通过 `-e` 转发 |
| **terminal**（Modal） | 默认情况下没有主机 env/文件 | ✅ 凭据文件已挂载；通过同步传递 env |
| **MCP** | 除安全系统变量 + 显式配置的 `env` 外，阻止所有内容 | ❌ 不受传递影响（改为使用 MCP `env` 配置） |

### 安全注意事项

- 传递仅影响你或你的技能明确声明的变量 —— 对于任意 LLM 生成的代码，默认安全态势保持不变
- 凭据文件以**只读**方式挂载到 Docker 容器中
- 技能卫士在安装前扫描技能内容以查找可疑的 env 访问模式
- 缺失/未设置的变量永远不会被注册（你不能泄露不存在的东西）
- Hermes 基础设施密钥（提供程序 API 密钥、网关令牌）永远不应添加到 `env_passthrough` —— 它们有专用机制

## MCP 凭据处理

MCP（模型上下文协议）服务器子进程接收**过滤的环境**以防止意外的凭据泄露。

### 安全环境变量

只有这些变量从主机传递到 MCP stdio 子进程：

```
PATH, HOME, USER, LANG, LC_ALL, TERM, SHELL, TMPDIR
```

加上任何 `XDG_*` 变量。所有其他环境变量（API 密钥、令牌、密钥）都被**剥离**。

显式在 MCP 服务器的 `env` 配置中定义的变量会被传递：

```yaml
mcp_servers:
  github:
    command: "npx"
    args: ["-y", "@modelcontextprotocol/server-github"]
    env:
      GITHUB_PERSONAL_ACCESS_TOKEN: "ghp_..."  # 仅传递这个
```

### 凭据编辑

来自 MCP 工具的错误消息在返回给 LLM 之前会被清理。以下模式被替换为 `[REDACTED]`：

- GitHub PAT（`ghp_...`）
- OpenAI 风格的密钥（`sk-...`）
- Bearer 令牌
- `token=`、`key=`、`API_KEY=`、`password=`、`secret=` 参数

### 网站访问策略

你可以限制代理可以通过其 Web 和浏览器工具访问哪些网站。这对于防止代理访问内部服务、管理面板或其他敏感 URL 很有用。

```yaml
# 在 ~/.hermes/config.yaml 中
security:
  website_blocklist:
    enabled: true
    domains:
      - "*.internal.company.com"
      - "admin.example.com"
    shared_files:
      - "/etc/hermes/blocked-sites.txt"
```

当请求被阻止的 URL 时，工具会返回一个错误，解释该域被策略阻止。阻止列表在 `web_search`、`web_extract`、`browser_navigate` 和所有具有 URL 功能的工具上强制执行。

有关完整详细信息，请参阅配置指南中的 [网站阻止列表](/docs/user-guide/configuration#website-blocklist)。

### SSRF 保护

所有具有 URL 功能的工具（Web 搜索、Web 提取、视觉、浏览器）在获取 URL 之前都会验证 URL 以防止服务器端请求伪造（SSRF）攻击。被阻止的地址包括：

- **专用网络**（RFC 1918）：`10.0.0.0/8`、`172.16.0.0/12`、`192.168.0.0/16`
- **环回**：`127.0.0.0/8`、`::1`
- **链接本地**：`169.254.0.0/16`（包括位于 `169.254.169.254` 的云元数据）
- **CGNAT / 共享地址空间**（RFC 6598）：`100.64.0.0/10`（Tailscale、WireGuard VPN）
- **云元数据主机名**：`metadata.google.internal`、`metadata.goog`
- **保留、多播和未指定地址**

SSRF 保护始终处于活动状态且无法禁用。DNS 故障被视为被阻止（故障关闭）。重定向链在每一跳都被重新验证以防止基于重定向的绕过。

### Tirith 执行前安全扫描

Hermes 集成了 [tirith](https://github.com/sheeki03/tirith) 用于在执行前进行内容级命令扫描。Tirith 检测仅靠模式匹配无法发现的威胁：

- 同形 URL 欺骗（国际化域名攻击）
- 管道到解释器模式（`curl | bash`、`wget | sh`）
- 终端注入攻击

Tirith 在首次使用时从 GitHub 发布版本自动安装，并进行 SHA-256 校验和验证（如果 cosign 可用，还会进行 cosign 来源验证）。

```yaml
# 在 ~/.hermes/config.yaml 中
security:
  tirith_enabled: true       # 启用/禁用 tirith 扫描（默认：true）
  tirith_path: "tirith"      # 到 tirith 二进制文件的路径（默认：PATH 查找）
  tirith_timeout: 5          # 子进程超时（秒）
  tirith_fail_open: true     # 当 tirith 不可用时允许执行（默认：true）
```

当 `tirith_fail_open` 为 `true`（默认）时，如果 tirith 未安装或超时，命令会继续。在高安全性环境中设置为 `false` 以在 tirith 不可用时阻止命令。

Tirith 的裁决与审批流程集成：安全命令通过，而可疑和被阻止的命令都会触发用户审批，并附带完整的 tirith 发现（严重性、标题、描述、更安全的替代方案）。用户可以批准或拒绝 —— 默认选择是否认以保持无人值守场景的安全。

### 上下文文件注入保护

上下文文件（AGENTS.md、.cursorrules、SOUL.md）在包含在系统提示中之前会被扫描以查找提示注入。扫描器检查：

- 忽略/无视先前指令的指令
- 带有可疑关键字的隐藏 HTML 注释
- 读取密钥的尝试（`.env`、`credentials`、`.netrc`）
- 通过 `curl` 进行的凭据泄露
- 不可见的 Unicode 字符（零宽度空格、双向覆盖）

被阻止的文件显示警告：

```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

## 生产部署最佳实践

### 网关部署清单

1. **设置显式允许列表** —— 永远不要在生产中使用 `GATEWAY_ALLOW_ALL_USERS=true`
2. **使用容器后端** —— 在 config.yaml 中设置 `terminal.backend: docker`
3. **限制资源限制** —— 设置适当的 CPU、内存和磁盘限制
4. **安全存储密钥** —— 保持 API 密钥在 `~/.hermes/.env` 中并具有适当的文件权限
5. **启用 DM 配对** —— 尽可能使用配对代码而不是硬编码用户 ID
6. **审查命令允许列表** —— 定期审核 config.yaml 中的 `command_allowlist`
7. **设置 `MESSAGING_CWD`** —— 不要让代理从敏感目录操作
8. **以非 root 身份运行** —— 永远不要以 root 身份运行网关
9. **监控日志** —— 检查 `~/.hermes/logs/` 以查找未经授权的访问尝试
10. **保持更新** —— 定期运行 `hermes update` 以获取安全补丁

### 保护 API 密钥

```bash
# 在 .env 文件上设置适当的权限
chmod 600 ~/.hermes/.env

# 为不同的服务保持单独的密钥
# 永远不要将 .env 文件提交到版本控制
```

### 网络隔离

为了获得最大安全性，请在单独的机器或 VM 上运行网关：

```yaml
terminal:
  backend: ssh
  ssh_host: "agent-worker.local"
  ssh_user: "hermes"
  ssh_key: "~/.ssh/hermes_agent_key"
```

这使网关的消息连接与代理的命令执行保持分离。
