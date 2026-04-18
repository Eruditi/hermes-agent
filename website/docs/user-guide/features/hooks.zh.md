---
sidebar_position: 6
title---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/h---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 |---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)**---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` |---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord、Slack、WhatsApp），不会阻塞主代理管道。

### 创建钩子

每个---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord、Slack、WhatsApp），不会阻塞主代理管道。

### 创建钩子

每个钩子都是 `~/.hermes/hooks/` 下的一个目录，包含两个文件---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord、Slack、WhatsApp），不会阻塞主代理管道。

### 创建钩子

每个钩子都是 `~/.hermes/hooks/` 下的一个目录，包含两个文件：

```text
~/.hermes/hooks/
└── my-hook/
---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord、Slack、WhatsApp），不会阻塞主代理管道。

### 创建钩子

每个钩子都是 `~/.hermes/hooks/` 下的一个目录，包含两个文件：

```text
~/.hermes/hooks/
└── my-hook/
    ├── HOOK.yaml      # 声明要监听哪些事件
    └── handler.py---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord、Slack、WhatsApp），不会阻塞主代理管道。

### 创建钩子

每个钩子都是 `~/.hermes/hooks/` 下的一个目录，包含两个文件：

```text
~/.hermes/hooks/
└── my-hook/
    ├── HOOK.yaml      # 声明要监听哪些事件
    └── handler.py     # Python 处理函数
```

#### HOOK.yaml

```yaml
name: my-h---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord、Slack、WhatsApp），不会阻塞主代理管道。

### 创建钩子

每个钩子都是 `~/.hermes/hooks/` 下的一个目录，包含两个文件：

```text
~/.hermes/hooks/
└── my-hook/
    ├── HOOK.yaml      # 声明要监听哪些事件
    └── handler.py     # Python 处理函数
```

#### HOOK.yaml

```yaml
name: my-hook
description: 将所有代理活动记录到文件
events:
  - agent:start---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord、Slack、WhatsApp），不会阻塞主代理管道。

### 创建钩子

每个钩子都是 `~/.hermes/hooks/` 下的一个目录，包含两个文件：

```text
~/.hermes/hooks/
└── my-hook/
    ├── HOOK.yaml      # 声明要监听哪些事件
    └── handler.py     # Python 处理函数
```

#### HOOK.yaml

```yaml
name: my-hook
description: 将所有代理活动记录到文件
events:
  - agent:start
  - agent:end
  - agent:step
```

`events` 列表---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord、Slack、WhatsApp），不会阻塞主代理管道。

### 创建钩子

每个钩子都是 `~/.hermes/hooks/` 下的一个目录，包含两个文件：

```text
~/.hermes/hooks/
└── my-hook/
    ├── HOOK.yaml      # 声明要监听哪些事件
    └── handler.py     # Python 处理函数
```

#### HOOK.yaml

```yaml
name: my-hook
description: 将所有代理活动记录到文件
events:
  - agent:start
  - agent:end
  - agent:step
```

`events` 列表确定哪些事件触发您的处理函数。您可以订阅任何事件组合，包括像 `command---
sidebar_position: 6
title: "事件钩子"
description: "在关键生命周期点运行自定义代码 — 记录活动、发送警报、发布到 webhooks"
---

# 事件钩子

Hermes 有两个钩子系统，在关键生命周期点运行自定义代码：

| 系统 | 注册方式 | 运行位置 | 用例 |
|--------|---------------|---------|----------|
| **[网关钩子](#gateway-event-hooks)** | `~/.hermes/hooks/` 中的 `HOOK.yaml` + `handler.py` | 仅网关 | 日志记录、警报、webhooks |
| **[插件钩子](#plugin-hooks)** | [插件](/docs/user-guide/features/plugins) 中的 `ctx.register_hook()` | CLI + 网关 | 工具拦截、指标、防护栏 |

两个系统都是非阻塞的 — 任何钩子中的错误都会被捕获并记录，永远不会使代理崩溃。

## 网关事件钩子

网关钩子在网关操作期间自动触发（Telegram、Discord、Slack、WhatsApp），不会阻塞主代理管道。

### 创建钩子

每个钩子都是 `~/.hermes/hooks/` 下的一个目录，包含两个文件：

```text
~/.hermes/hooks/
└── my-hook/
    ├── HOOK.yaml      # 声明要监听哪些事件
    └── handler.py     # Python 处理函数
```

#### HOOK.yaml

```yaml
name: my-hook
description: 将所有代理活动记录到文件
events:
  - agent:start
  - agent:end
  - agent:step
```

`events` 列表确定哪些事件触发您的处理函数。您可以订阅任何事件组合，包括像 `command:*` 这样的通配符。

#### handler.py

```python
import json
