---
name: imessage
description: 通过macOS上的imsg CLI发送和接收iMessage/SMS。
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [iMessage, SMS, 消息, macOS, Apple]
prerequisites:
  commands: [imsg]
---

# iMessage

使用`imsg`通过macOS Messages.app读取和发送iMessage/SMS。

## 先决条件

- 已登录Messages.app的**macOS**
- 安装：`brew install steipete/tap/imsg`
- 授予终端完全磁盘访问权限（系统设置 → 隐私 → 完全磁盘访问）
- 出现提示时授予Messages.app自动化权限

## 何时使用

- 用户要求发送iMessage或短信
- 读取iMessage对话历史
- 检查最近的Messages.app聊天
- 发送到电话号码或Apple ID

## 何时不使用

- Telegram/Discord/Slack/WhatsApp消息 → 使用适当的网关频道
- 群聊管理（添加/删除成员） → 不支持
- 批量/大量消息 → 始终先与用户确认

## 快速参考

### 列出聊天

```bash
imsg chats --limit 10 --json
```

### 查看历史记录

```bash
# 按聊天ID
imsg history --chat-id 1 --limit 20 --json

# 带附件信息
imsg history --chat-id 1 --limit 20 --attachments --json
```

### 发送消息

```bash
# 仅文本
imsg send --to "+14155551212" --text "你好！"

# 带附件
imsg send --to "+14155551212" --text "看看这个" --file /path/to/image.jpg

# 强制iMessage或SMS
imsg send --to "+14155551212" --text "嗨" --service imessage
imsg send --to "+14155551212" --text "嗨" --service sms
```

### 监听新消息

```bash
imsg watch --chat-id 1 --attachments
```

## 服务选项

- `--service imessage` — 强制iMessage（需要收件人有iMessage）
- `--service sms` — 强制SMS（绿色气泡）
- `--service auto` — 让Messages.app决定（默认）

## 规则

1. 发送前**始终确认收件人和消息内容**
2. 未经明确用户批准，**从不发送到未知号码**
3. 附加前**验证文件路径**存在
4. **不要发送垃圾邮件** — 自我限速

## 示例工作流程

用户："给妈妈发短信说我会迟到"

```bash
# 1. 找到妈妈的聊天
imsg chats --limit 20 --json | jq '.[] | select(.displayName | contains("妈妈"))'

# 2. 与用户确认："在+1555123456找到妈妈。通过iMessage发送'我会迟到'吗？"

# 3. 确认后发送
imsg send --to "+1555123456" --text "我会迟到"
```
