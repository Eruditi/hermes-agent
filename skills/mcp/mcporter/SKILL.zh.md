---
name: mcporter
description: 使用mcporter CLI直接列出、配置、验证和调用MCP服务器/工具（HTTP或stdio），包括临时服务器、配置编辑和CLI/类型生成。
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [MCP, 工具, API, 集成, 互操作]
    homepage: https://mcporter.dev
prerequisites:
  commands: [npx]
---

# mcporter

使用`mcporter`直接从终端发现、调用和管理[MCP（模型上下文协议）](https://modelcontextprotocol.io/)服务器和工具。

## 先决条件

需要Node.js：
```bash
# 无需安装（通过npx运行）
npx mcporter list

# 或全局安装
npm install -g mcporter
```

## 快速开始

```bash
# 列出此机器上已配置的MCP服务器
mcporter list

# 列出特定服务器的工具，带模式详情
mcporter list <server> --schema

# 调用工具
mcporter call <server.tool> key=value
```

## 发现MCP服务器

mcporter自动发现机器上由其他MCP客户端（Claude Desktop、Cursor等）配置的服务器。要查找要使用的新服务器，请浏览[mcpfinder.dev](https://mcpfinder.dev)或[mcp.so](https://mcp.so)等注册表，然后临时连接：

```bash
# 通过URL连接到任何MCP服务器（无需配置）
mcporter list --http-url https://some-mcp-server.com --name my_server

# 或即时运行stdio服务器
mcporter list --stdio "npx -y @modelcontextprotocol/server-filesystem" --name fs
```

## 调用工具

```bash
# 键=值语法
mcporter call linear.list_issues team=ENG limit:5

# 函数语法
mcporter call "linear.create_issue(title: \"Bug fix needed\")"

# 临时HTTP服务器（无需配置）
mcporter call https://api.example.com/mcp.fetch url=https://example.com

# 临时stdio服务器
mcporter call --stdio "bun run ./server.ts" scrape url=https://example.com

# JSON负载
mcporter call <server.tool> --args '{"limit": 5}'

# 机器可读输出（推荐用于Hermes）
mcporter call <server.tool> key=value --output json
```

## 验证和配置

```bash
# 服务器的OAuth登录
mcporter auth <server | url> [--reset]

# 管理配置
mcporter config list
mcporter config get <key>
mcporter config add <server>
mcporter config remove <server>
mcporter config import <path>
```

配置文件位置：`./config/mcporter.json`（用`--config`覆盖）。

## 守护进程

对于持久服务器连接：
```bash
mcporter daemon start
mcporter daemon status
mcporter daemon stop
mcporter daemon restart
```

## 代码生成

```bash
# 为MCP服务器生成CLI包装器
mcporter generate-cli --server <name>
mcporter generate-cli --command <url>

# 检查生成的CLI
mcporter inspect-cli <path> [--json]

# 生成TypeScript类型/客户端
mcporter emit-ts <server> --mode client
mcporter emit-ts <server> --mode types
```

## 注意

- 使用`--output json`获取更易于解析的结构化输出
- 临时服务器（HTTP URL或`--stdio`命令）无需任何配置即可工作 — 对一次性调用有用
- OAuth验证可能需要交互式浏览器流程 — 如需使用`terminal(command="mcporter auth <server>", pty=true)`
