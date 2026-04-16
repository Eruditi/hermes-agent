---
name: himalaya
description: 通过IMAP/SMTP管理电子邮件的CLI。使用himalaya从终端列出、阅读、编写、回复、转发、搜索和整理电子邮件。支持多个账户和使用MML（MIME元语言）的消息撰写。
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Email, IMAP, SMTP, CLI, Communication, 电子邮件, 通信]
    homepage: https://github.com/pimalaya/himalaya
prerequisites:
  commands: [himalaya]
---

# Himalaya 电子邮件 CLI

Himalaya是一个CLI电子邮件客户端，让你可以使用IMAP、SMTP、Notmuch或Sendmail后端从终端管理电子邮件。

## 参考文献

- `references/configuration.md`（配置文件设置 + IMAP/SMTP认证）
- `references/message-composition.md`（用于撰写电子邮件的MML语法）

## 先决条件

1. 已安装Himalaya CLI（用`himalaya --version`验证）
2. 配置文件位于`~/.config/himalaya/config.toml`
3. 配置了IMAP/SMTP凭据（安全存储密码）

### 安装

```bash
# 预构建二进制文件（Linux/macOS — 推荐）
curl -sSL https://raw.githubusercontent.com/pimalaya/himalaya/master/install.sh | PREFIX=~/.local sh

# macOS通过Homebrew
brew install himalaya

# 或通过cargo（任何带Rust的平台）
cargo install himalaya --locked
```

## 配置设置

运行交互式向导设置账户：

```bash
himalaya account configure
```

或手动创建`~/.config/himalaya/config.toml`：

```toml
[accounts.personal]
email = "you@example.com"
display-name = "Your Name"
default = true

backend.type = "imap"
backend.host = "imap.example.com"
backend.port = 993
backend.encryption.type = "tls"
backend.login = "you@example.com"
backend.auth.type = "password"
backend.auth.cmd = "pass show email/imap"  # 或使用钥匙环

message.send.backend.type = "smtp"
message.send.backend.host = "smtp.example.com"
message.send.backend.port = 587
message.send.backend.encryption.type = "start-tls"
message.send.backend.login = "you@example.com"
message.send.backend.auth.type = "password"
message.send.backend.auth.cmd = "pass show email/smtp"
```

## Hermes集成注意事项

- **阅读、列出、搜索、移动、删除**都直接通过终端工具工作
- **撰写/回复/转发** — 管道输入（`cat << EOF | himalaya template send`）推荐用于可靠性。交互式`$EDITOR`模式与`pty=true` + background + process tool一起工作，但需要知道编辑器及其命令
- 使用`--output json`获取更容易以编程方式解析的结构化输出
- `himalaya account configure`向导需要交互式输入 — 使用PTY模式：`terminal(command="himalaya account configure", pty=true)`

## 常见操作

### 列出文件夹

```bash
himalaya folder list
```

### 列出电子邮件

在INBOX中列出电子邮件（默认）：

```bash
himalaya envelope list
```

在特定文件夹中列出电子邮件：

```bash
himalaya envelope list --folder "Sent"
```

带分页列出：

```bash
himalaya envelope list --page 1 --page-size 20
```

### 搜索电子邮件

```bash
himalaya envelope list from john@example.com subject meeting
```

### 阅读电子邮件

通过ID阅读电子邮件（显示纯文本）：

```bash
himalaya message read 42
```

导出原始MIME：

```bash
himalaya message export 42 --full
```

### 回复电子邮件

要从Hermes非交互式回复，阅读原始消息，撰写回复，然后用管道传输：

```bash
# 获取回复模板，编辑它，然后发送
himalaya template reply 42 | sed 's/^$/\nYour reply text here\n/' | himalaya template send
```

或手动构建回复：

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: sender@example.com
Subject: Re: Original Subject
In-Reply-To: <original-message-id>

Your reply here.
EOF
```

回复所有人（交互式 — 需要$EDITOR，改为使用上面的模板方法）：

```bash
himalaya message reply 42 --all
```

### 转发电子邮件

```bash
# 获取转发模板并用修改进行管道传输
himalaya template forward 42 | sed 's/^To:.*/To: newrecipient@example.com/' | himalaya template send
```

### 撰写新电子邮件

**非交互式（从Hermes使用这个）** — 通过stdin用管道传输消息：

```bash
cat << 'EOF' | himalaya template send
From: you@example.com
To: recipient@example.com
Subject: Test Message

Hello from Himalaya!
EOF
```

或带有标题标志：

```bash
himalaya message write -H "To:recipient@example.com" -H "Subject:Test" "Message body here"
```

注意：没有管道输入的`himalaya message write`会打开`$EDITOR`。这与`pty=true` + background模式一起工作，但用管道传输更简单和更可靠。

### 移动/复制电子邮件

移动到文件夹：

```bash
himalaya message move 42 "Archive"
```

复制到文件夹：

```bash
himalaya message copy 42 "Important"
```

### 删除电子邮件

```bash
himalaya message delete 42
```

### 管理标志

添加标志：

```bash
himalaya flag add 42 --flag seen
```

移除标志：

```bash
himalaya flag remove 42 --flag seen
```

## 多个账户

列出账户：

```bash
himalaya account list
```

使用特定账户：

```bash
himalaya --account work envelope list
```

## 附件

从消息保存附件：

```bash
himalaya attachment download 42
```

保存到特定目录：

```bash
himalaya attachment download 42 --dir ~/Downloads
```

## 输出格式

大多数命令支持`--output`用于结构化输出：

```bash
himalaya envelope list --output json
himalaya envelope list --output plain
```

## 调试

启用调试日志：

```bash
RUST_LOG=debug himalaya envelope list
```

带有回溯的完整跟踪：

```bash
RUST_LOG=trace RUST_BACKTRACE=1 himalaya envelope list
```

## 提示

- 使用`himalaya --help`或`himalaya <command> --help`获取详细使用说明。
- 消息ID相对于当前文件夹；文件夹更改后重新列出。
- 对于撰写带附件的丰富电子邮件，使用MML语法（见`references/message-composition.md`）。
- 使用`pass`、系统钥匙环或输出密码的命令安全存储密码。