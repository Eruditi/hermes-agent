---
name: xitter
description: 使用x-cli终端客户端通过官方X API凭据与X/Twitter交互。用于发布、阅读时间线、搜索推文、点赞、转发、书签、提及和用户查找。
version: 1.0.0
author: Siddharth Balyan + Hermes Agent
license: MIT
platforms: [linux, macos]
prerequisites:
  commands: [uv]
  env_vars: [X_API_KEY, X_API_SECRET, X_BEARER_TOKEN, X_ACCESS_TOKEN, X_ACCESS_TOKEN_SECRET]
metadata:
  hermes:
    tags: [twitter, x, 社交媒体, x-cli]
    homepage: https://github.com/Infatoshi/x-cli
---

# Xitter — 通过x-cli访问X/Twitter

使用`x-cli`从终端进行官方X/Twitter API交互。

此技能用于：
- 发布推文、回复和引用推文
- 搜索推文和阅读时间线
- 查找用户、关注者和正在关注
- 点赞和转发
- 检查提及和书签

此技能有意不向Hermes中单独vendor一个CLI实现。而是安装和使用上游`x-cli`。

## 重要成本/访问说明

对于大多数实际使用，X API访问并不是真正免费的。期望需要付费或预付费的X开发者访问。如果命令因权限或配额错误失败，请首先检查您的X开发者计划。

## 安装

使用`uv`安装上游`x-cli`：

```bash
uv tool install git+https://github.com/Infatoshi/x-cli.git
```

稍后升级：

```bash
uv tool upgrade x-cli
```

验证：

```bash
x-cli --help
```

## 凭据

您需要来自X开发者门户的这五个值：
- `X_API_KEY`
- `X_API_SECRET`
- `X_BEARER_TOKEN`
- `X_ACCESS_TOKEN`
- `X_ACCESS_TOKEN_SECRET`

从以下位置获取它们：
- https://developer.x.com/en/portal/dashboard

### 为什么X需要5个密钥？

不幸的是，官方X API将身份验证拆分为应用程序级和用户级凭据：

- `X_API_KEY` + `X_API_SECRET` 标识您的应用
- `X_BEARER_TOKEN` 用于应用程序级读取访问
- `X_ACCESS_TOKEN` + `X_ACCESS_TOKEN_SECRET` 让CLI充当您的用户账户进行写入和身份验证操作

所以是的 — 一个集成需要很多密钥，但这是稳定的官方API路径，仍然比cookie/会话抓取更可取。

在门户中设置要求：
1. 创建或打开您的应用
2. 在用户身份验证设置中，将权限设置为`读取和写入`
3. 启用写入权限后生成或重新生成访问令牌 + 访问令牌密钥
4. 仔细保存所有五个值 — 缺少其中任何一个通常会产生令人困惑的身份验证或权限错误

注意：上游`x-cli`期望完整的凭据集存在，所以即使您主要关心只读命令，配置全部五个也是最简单的。

## 成本/摩擦现实检查

如果此设置感觉比应该的更重，那是因为它确实如此。X的官方开发者流程是高摩擦的，并且通常是付费的。此技能选择官方API路径，因为它比浏览器cookie/会话方法更稳定和可维护。

如果用户想要最不脆弱的长期设置，请使用此技能。如果他们想要零设置或非官方路径，那是不同的权衡，不是此技能的目的。


## 存储凭据的位置

`x-cli`在`~/.config/x-cli/.env`中查找凭据。

如果您已经将X凭据保存在`~/.hermes/.env`中，最干净的设置是：

```bash
mkdir -p ~/.config/x-cli
ln -sf ~/.hermes/.env ~/.config/x-cli/.env
```

或者创建一个专用文件：

```bash
mkdir -p ~/.config/x-cli
cat > ~/.config/x-cli/.env <<'EOF'
X_API_KEY=your_consumer_key
X_API_SECRET=your_secret_key
X_BEARER_TOKEN=your_bearer_token
X_ACCESS_TOKEN=your_access_token
X_ACCESS_TOKEN_SECRET=your_access_token_secret
EOF
chmod 600 ~/.config/x-cli/.env
```

## 快速验证

```bash
x-cli user get openai
x-cli tweet search "from:NousResearch" --max 3
x-cli me mentions --max 5
```

如果读取有效但写入失败，请在确认`读取和写入`权限后重新生成访问令牌。

## 常用命令

### 推文

```bash
x-cli tweet post "hello world"
x-cli tweet get https://x.com/user/status/1234567890
x-cli tweet delete 1234567890
x-cli tweet reply 1234567890 "nice post"
x-cli tweet quote 1234567890 "worth reading"
x-cli tweet search "AI agents" --max 20
x-cli tweet metrics 1234567890
```

### 用户

```bash
x-cli user get openai
x-cli user timeline openai --max 10
x-cli user followers openai --max 50
x-cli user following openai --max 50
```

### 自我/已验证用户

```bash
x-cli me mentions --max 20
x-cli me bookmarks --max 20
x-cli me bookmark 1234567890
x-cli me unbookmark 1234567890
```

### 快速操作

```bash
x-cli like 1234567890
x-cli retweet 1234567890
```

## 输出模式

当代理需要以编程方式检查字段时，使用结构化输出：

```bash
x-cli -j tweet search "AI agents" --max 5
x-cli -p user get openai
x-cli -md tweet get 1234567890
x-cli -v -j tweet get 1234567890
```

推荐的默认值：
- `-j` 用于机器可读输出
- `-v` 当您需要时间戳、指标或元数据时
- 普通/默认模式用于快速人工检查

## 代理工作流程

1. 确认`x-cli`已安装
2. 确认凭据存在
3. 从读取命令开始（`user get`、`tweet search`、`me mentions`）
4. 在提取字段以供后续步骤时使用`-j`
5. 仅在确认目标推文/用户和用户意图后执行写入操作

## 陷阱

- **付费API访问**：许多失败是计划/权限问题，而不是代码问题。
- **403 oauth1-permissions**：启用`读取和写入`后重新生成访问令牌。
- **回复限制**：X限制许多程序化回复。`tweet quote`通常比`tweet reply`更可靠。
- **速率限制**：期望每个端点限制和冷却窗口。
- **凭据漂移**：如果您在`~/.hermes/.env`中轮换令牌，请确保`~/.config/x-cli/.env`仍然指向当前文件。

## 备注

- 优先使用官方API工作流程而不是cookie/会话抓取。
- 可互换使用推文URL或ID — `x-cli`接受两者。
- 如果书签行为在上游更改，请首先检查上游README：
  https://github.com/Infatoshi/x-cli
