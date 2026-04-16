---
name: webhook-subscriptions
description: 创建和管理用于事件驱动的代理激活的webhook订阅。当用户希望外部服务通过自动触发代理运行时使用。
version: 1.0.0
metadata:
  hermes:
    tags: [webhook, events, automation, integrations, 事件, 自动化, 集成]
---

# Webhook订阅

创建动态webhook订阅，以便外部服务（GitHub、GitLab、Stripe、CI/CD、IoT传感器、监控工具）可以通过向URL POST事件来触发Hermes代理运行。

## 设置（首先需要）

必须先启用webhook平台，然后才能创建订阅。检查：
```bash
hermes webhook list
```

如果显示"Webhook platform is not enabled"，设置它：

### 选项1：设置向导
```bash
hermes gateway setup
```
按照提示启用webhooks、设置端口和设置全局HMAC密钥。

### 选项2：手动配置
添加到`~/.hermes/config.yaml`：
```yaml
platforms:
  webhook:
    enabled: true
    extra:
      host: "0.0.0.0"
      port: 8644
      secret: "generate-a-strong-secret-here"
```

### 选项3：环境变量
添加到`~/.hermes/.env`：
```bash
WEBHOOK_ENABLED=true
WEBHOOK_PORT=8644
WEBHOOK_SECRET=generate-a-strong-secret-here
```

配置后，启动（或重启）网关：
```bash
hermes gateway run
# 或如果使用systemd：
systemctl --user restart hermes-gateway
```

验证它正在运行：
```bash
curl http://localhost:8644/health
```

## 命令

所有管理都通过`hermes webhook` CLI命令：

### 创建订阅
```bash
hermes webhook subscribe <name> \
  --prompt "Prompt template with {payload.fields}" \
  --events "event1,event2" \
  --description "What this does" \
  --skills "skill1,skill2" \
  --deliver telegram \
  --deliver-chat-id "12345" \
  --secret "optional-custom-secret"
```

返回webhook URL和HMAC密钥。用户配置他们的服务向该URL POST。

### 列出订阅
```bash
hermes webhook list
```

### 移除订阅
```bash
hermes webhook remove <name>
```

### 测试订阅
```bash
hermes webhook test <name>
hermes webhook test <name> --payload '{"key": "value"}'
```

## 提示模板

提示支持`{dot.notation}`用于访问嵌套的有效负载字段：

- `{issue.title}` — GitHub issue标题
- `{pull_request.user.login}` — PR作者
- `{data.object.amount}` — Stripe支付金额
- `{sensor.temperature}` — IoT传感器读数

如果未指定提示，完整的JSON有效负载将被转储到代理提示中。

## 常见模式

### GitHub：新issues
```bash
hermes webhook subscribe github-issues \
  --events "issues" \
  --prompt "New GitHub issue #{issue.number}: {issue.title}\n\nAction: {action}\nAuthor: {issue.user.login}\nBody:\n{issue.body}\n\nPlease triage this issue." \
  --deliver telegram \
  --deliver-chat-id "-100123456789"
```

然后在GitHub仓库设置 → Webhooks → 添加webhook：
- Payload URL：返回的webhook_url
- Content type：application/json
- Secret：返回的secret
- Events："Issues"

### GitHub：PR评审
```bash
hermes webhook subscribe github-prs \
  --events "pull_request" \
  --prompt "PR #{pull_request.number} {action}: {pull_request.title}\nBy: {pull_request.user.login}\nBranch: {pull_request.head.ref}\n\n{pull_request.body}" \
  --skills "github-code-review" \
  --deliver github_comment
```

### Stripe：支付事件
```bash
hermes webhook subscribe stripe-payments \
  --events "payment_intent.succeeded,payment_intent.payment_failed" \
  --prompt "Payment {data.object.status}: {data.object.amount} cents from {data.object.receipt_email}" \
  --deliver telegram \
  --deliver-chat-id "-100123456789"
```

### CI/CD：构建通知
```bash
hermes webhook subscribe ci-builds \
  --events "pipeline" \
  --prompt "Build {object_attributes.status} on {project.name} branch {object_attributes.ref}\nCommit: {commit.message}" \
  --deliver discord \
  --deliver-chat-id "1234567890"
```

### 通用监控警报
```bash
hermes webhook subscribe alerts \
  --prompt "Alert: {alert.name}\nSeverity: {alert.severity}\nMessage: {alert.message}\n\nPlease investigate and suggest remediation." \
  --deliver origin
```

## 安全性

- 每个订阅获取自动生成的HMAC-SHA256密钥（或通过`--secret`提供您自己的）
- Webhook适配器验证每个传入POST的签名
- 配置.yaml中的静态路由无法被动态订阅覆盖
- 订阅持久化到`~/.hermes/webhook_subscriptions.json`

## 工作原理

1. `hermes webhook subscribe`写入到`~/.hermes/webhook_subscriptions.json`
2. Webhook适配器在每个传入请求时热重新加载此文件（mtime门控，可忽略的开销）
3. 当匹配路由的POST到达时，适配器格式化提示并触发代理运行
4. 代理的响应被交付到配置的目标（Telegram、Discord、GitHub评论等）

## 故障排除

如果webhooks不工作：

1. **网关正在运行吗？** 用`systemctl --user status hermes-gateway`或`ps aux | grep gateway`检查
2. **Webhook服务器正在监听吗？** `curl http://localhost:8644/health`应返回`{"status": "ok"}`
3. **检查网关日志：** `grep webhook ~/.hermes/logs/gateway.log | tail -20`
4. **签名不匹配？** 验证您服务中的密钥与`hermes webhook list`中的匹配。GitHub发送`X-Hub-Signature-256`，GitLab发送`X-Gitlab-Token`。
5. **防火墙/NAT？** Webhook URL必须从服务可访问。对于本地开发，使用隧道（ngrok、cloudflared）。
6. **错误的事件类型？** 检查`--events`过滤器匹配服务发送的内容。使用`hermes webhook test <name>`验证路由工作。