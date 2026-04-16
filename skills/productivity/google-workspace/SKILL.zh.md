---
name: google-workspace
description: Hermes的Gmail、Calendar、Drive、Contacts、Sheets和Docs集成。使用Hermes管理的OAuth2设置，当可用时优先使用Google Workspace CLI（`gws`）以获得更广泛的API覆盖，否则回退到Python客户端库。
version: 1.0.0
author: Nous Research
license: MIT
metadata:
  hermes:
    tags: [Google, Gmail, Calendar, Drive, Sheets, Docs, Contacts, 电子邮件, OAuth]
    homepage: https://github.com/NousResearch/hermes-agent
    related_skills: [himalaya]
---

# Google Workspace

Gmail、Calendar、Drive、Contacts、Sheets和Docs — 通过Hermes管理的OAuth和薄CLI包装器。当安装了`gws`时，此技能将其用作执行后端以获得更广泛的Google Workspace覆盖；否则回退到捆绑的Python客户端实现。

## 参考

- `references/gmail-search-syntax.md` — Gmail搜索运算符（is:unread、from:、newer_than:等）

## 脚本

- `scripts/setup.py` — OAuth2设置（运行一次以授权）
- `scripts/google_api.py` — 兼容性包装器CLI。当可用时优先使用`gws`进行操作，同时保留Hermes现有的JSON输出合同。

## 首次设置

设置是完全非交互式的 — 您逐步驱动它，以便它在CLI、Telegram、Discord或任何平台上都能工作。

首先定义一个简写：

```bash
GSETUP="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/setup.py"
```

### 步骤0：检查是否已设置

```bash
$GSETUP --check
```

如果它打印`AUTHENTICATED`，跳到使用 — 设置已完成。

### 步骤1：分类 — 询问用户他们需要什么

在开始OAuth设置之前，向用户询问两个问题：

**问题1："您需要什么Google服务？只需要电子邮件，还是也需要Calendar/Drive/Sheets/Docs？"**

- **仅电子邮件** → 他们根本不需要此技能。改用`himalaya`技能 — 它与Gmail应用密码（设置 → 安全 → 应用密码）一起使用，需要2分钟设置。不需要Google Cloud项目。加载himalaya技能并按照其设置说明操作。

- **电子邮件 + Calendar** → 继续使用此技能，但在身份验证期间使用`--services email,calendar`，以便同意屏幕仅询问他们实际需要的范围。

- **仅Calendar/Drive/Sheets/Docs** → 继续使用此技能，并使用更窄的`--services`集合，如`calendar,drive,sheets,docs`。

- **完整Workspace访问** → 继续使用此技能并使用默认的`all`服务集合。

**问题2："您的Google账户是否使用高级保护（需要硬件安全密钥才能登录）？如果您不确定，您可能没有 — 这是您会明确注册的东西。"**

- **否 / 不确定** → 正常设置。继续下面。
- **是** → 他们的Workspace管理员必须在步骤4工作之前将OAuth客户端ID添加到组织的允许应用列表中。提前让他们知道。

### 步骤2：创建OAuth凭据（一次性，~5分钟）

告诉用户：

> 您需要一个Google Cloud OAuth客户端。这是一次性设置：
>
> 1. 创建或选择一个项目：
>    https://console.cloud.google.com/projectselector2/home/dashboard
> 2. 从API库启用所需的API：
>    https://console.cloud.google.com/apis/library
>    启用：Gmail API、Google Calendar API、Google Drive API、
>    Google Sheets API、Google Docs API、People API
> 3. 在这里创建OAuth客户端：
>    https://console.cloud.google.com/apis/credentials
>    凭据 → 创建凭据 → OAuth 2.0客户端ID
> 4. 应用类型："桌面应用" → 创建
> 5. 如果应用仍在测试中，请在此处将用户的Google账户添加为测试用户：
>    https://console.cloud.google.com/auth/audience
>    受众 → 测试用户 → 添加用户
> 6. 下载JSON文件并告诉我文件路径
>
> 重要的Hermes CLI说明：如果文件路径以`/`开头，不要在CLI中仅将裸路径作为自己的消息发送，因为它可能被误认为是斜杠命令。而是在句子中发送它，例如：
> `JSON文件路径是：/home/user/Downloads/client_secret_....json`

一旦他们提供了路径：

```bash
$GSETUP --client-secret /path/to/client_secret.json
```

如果他们粘贴原始客户端ID / 客户端密钥值而不是文件路径，自己为他们编写一个有效的桌面OAuth JSON文件，将其保存在某个明确的地方（例如`~/Downloads/hermes-google-client-secret.json`），然后对该文件运行`--client-secret`。

### 步骤3：获取授权URL

使用在步骤1中选择的服务集合。示例：

```bash
$GSETUP --auth-url --services email,calendar --format json
$GSETUP --auth-url --services calendar,drive,sheets,docs --format json
$GSETUP --auth-url --services all --format json
```

这返回带有`auth_url`字段的JSON，并且还将确切的URL保存到`~/.hermes/google_oauth_last_url.txt`。

此步骤的代理规则：
- 提取`auth_url`字段，并将该确切的URL作为单行发送给用户。
- 告诉用户，批准后浏览器可能会在`http://localhost:1`上失败，这是预期的。
- 告诉他们从浏览器地址栏复制整个重定向URL。
- 如果用户得到`Error 403: access_denied`，直接将他们发送到`https://console.cloud.google.com/auth/audience`以将自己添加为测试用户。

### 步骤4：交换代码

用户将粘贴回类似`http://localhost:1/?code=4/0A...&scope=...`的URL，或者只是代码字符串。两者都有效。`--auth-url`步骤在本地存储临时待处理的OAuth会话，以便`--auth-code`可以在以后完成PKCE交换，即使在无头系统上也是如此：

```bash
$GSETUP --auth-code "THE_URL_OR_CODE_THE_USER_PASTED" --format json
```

如果`--auth-code`因为代码过期、已使用或来自较旧的浏览器选项卡而失败，它现在返回一个新鲜的`fresh_auth_url`。在这种情况下，立即将新URL发送给用户，并让他们仅使用最新的浏览器重定向重试。

### 步骤5：验证

```bash
$GSETUP --check
```

应该打印`AUTHENTICATED`。设置完成 — 从现在开始令牌自动刷新。

### 备注

- 令牌存储在`~/.hermes/google_token.json`并自动刷新。
- 待处理的OAuth会话状态/验证器临时存储在`~/.hermes/google_oauth_pending.json`，直到交换完成。
- 如果安装了`gws`，`google_api.py`将其指向相同的`~/.hermes/google_token.json`凭据文件。用户不需要运行单独的`gws auth login`流程。
- 要撤销：`$GSETUP --revoke`

## 使用

所有命令都通过API脚本。将`GAPI`设置为简写：

```bash
GAPI="python ${HERMES_HOME:-$HOME/.hermes}/skills/productivity/google-workspace/scripts/google_api.py"
```

### Gmail

```bash
# 搜索（返回带有id、from、subject、date、snippet的JSON数组）
$GAPI gmail search "is:unread" --max 10
$GAPI gmail search "from:boss@company.com newer_than:1d"
$GAPI gmail search "has:attachment filename:pdf newer_than:7d"

# 读取完整消息（返回带有正文文本的JSON）
$GAPI gmail get MESSAGE_ID

# 发送
$GAPI gmail send --to user@example.com --subject "Hello" --body "Message text"
$GAPI gmail send --to user@example.com --subject "Report" --body "<h1>Q4</h1><p>Details...</p>" --html
$GAPI gmail send --to user@example.com --subject "Hello" --from '"Research Agent" <user@example.com>' --body "Message text"

# 回复（自动线程化并设置In-Reply-To）
$GAPI gmail reply MESSAGE_ID --body "Thanks, that works for me."
$GAPI gmail reply MESSAGE_ID --from '"Support Bot" <user@example.com>' --body "Thanks"

# 标签
$GAPI gmail labels
$GAPI gmail modify MESSAGE_ID --add-labels LABEL_ID
$GAPI gmail modify MESSAGE_ID --remove-labels UNREAD
```

### Calendar

```bash
# 列出事件（默认为接下来7天）
$GAPI calendar list
$GAPI calendar list --start 2026-03-01T00:00:00Z --end 2026-03-07T23:59:59Z

# 创建事件（需要带有时区的ISO 8601）
$GAPI calendar create --summary "Team Standup" --start 2026-03-01T10:00:00-06:00 --end 2026-03-01T10:30:00-06:00
$GAPI calendar create --summary "Lunch" --start 2026-03-01T12:00:00Z --end 2026-03-01T13:00:00Z --location "Cafe"
$GAPI calendar create --summary "Review" --start 2026-03-01T14:00:00Z --end 2026-03-01T15:00:00Z --attendees "alice@co.com,bob@co.com"

# 删除事件
$GAPI calendar delete EVENT_ID
```

### Drive

```bash
$GAPI drive search "quarterly report" --max 10
$GAPI drive search "mimeType='application/pdf'" --raw-query --max 5
```

### Contacts

```bash
$GAPI contacts list --max 20
```

### Sheets

```bash
# 读取
$GAPI sheets get SHEET_ID "Sheet1!A1:D10"

# 写入
$GAPI sheets update SHEET_ID "Sheet1!A1:B2" --values '[["Name","Score"],["Alice","95"]]'

# 追加行
$GAPI sheets append SHEET_ID "Sheet1!A:C" --values '[["new","row","data"]]'
```

### Docs

```bash
$GAPI docs get DOC_ID
```

## 输出格式

所有命令返回JSON。用`jq`解析或直接读取。关键字段：

- **Gmail搜索**：`[{id, threadId, from, to, subject, date, snippet, labels}]`
- **Gmail获取**：`{id, threadId, from, to, subject, date, labels, body}`
- **Gmail发送/回复**：`{status: "sent", id, threadId}`
- **Calendar列出**：`[{id, summary, start, end, location, description, htmlLink}]`
- **Calendar创建**：`{status: "created", id, summary, htmlLink}`
- **Drive搜索**：`[{id, name, mimeType, modifiedTime, webViewLink}]`
- **Contacts列出**：`[{name, emails: [...], phones: [...]}]`
- **Sheets获取**：`[[cell, cell, ...], ...]`

## 规则

1. **在发送电子邮件或创建/删除事件之前，始终先与用户确认。** 显示草稿内容并请求批准。
2. **首次使用前检查身份验证** — 运行`setup.py --check`。如果失败，引导用户完成设置。
3. **对于复杂查询，使用Gmail搜索语法参考** — 用`skill_view("google-workspace", file_path="references/gmail-search-syntax.md")`加载它。
4. **Calendar时间必须包含时区** — 始终使用带偏移的ISO 8601（例如`2026-03-01T10:00:00-06:00`）或UTC（`Z`）。
5. **尊重速率限制** — 避免快速连续的API调用。尽可能批量读取。

## 故障排除

| 问题 | 修复 |
|---------|-----|
| `NOT_AUTHENTICATED` | 运行上面的设置步骤2-5 |
| `REFRESH_FAILED` | 令牌被撤销或过期 — 重做步骤3-5 |
| `HttpError 403: Insufficient Permission` | 缺少API范围 — `$GSETUP --revoke`然后重做步骤3-5 |
| `HttpError 403: Access Not Configured` | API未启用 — 用户需要在Google Cloud Console中启用它 |
| `ModuleNotFoundError` | 运行`$GSETUP --install-deps` |
| 高级保护阻止身份验证 | Workspace管理员必须允许OAuth客户端ID |

## 撤销访问

```bash
$GSETUP --revoke
```
