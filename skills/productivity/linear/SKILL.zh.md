---
name: linear
description: 通过GraphQL API管理Linear问题、项目和团队。创建、更新、搜索和组织问题。使用API密钥身份验证（无需OAuth）。所有操作通过curl — 没有依赖项。
version: 1.0.0
author: Hermes Agent
license: MIT
prerequisites:
  env_vars: [LINEAR_API_KEY]
  commands: [curl]
metadata:
  hermes:
    tags: [Linear, 项目管理, 问题, GraphQL, API, 生产力]
---

# Linear — 问题和项目管理

使用`curl`直接通过GraphQL API管理Linear问题、项目和团队。没有MCP服务器，没有OAuth流程，没有额外依赖项。

## 设置

1. 从**Linear设置 > API > 个人API密钥**获取个人API密钥
2. 在您的环境中设置`LINEAR_API_KEY`（通过`hermes setup`或您的环境配置）

## API基础

- **端点：** `https://api.linear.app/graphql`（POST）
- **身份验证头：** `Authorization: $LINEAR_API_KEY`（API密钥没有"Bearer"前缀）
- **所有请求都是POST**，带有`Content-Type: application/json`
- **UUID和短标识符**（例如`ENG-123`）都适用于`issue(id:)`

基本curl模式：
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { id name } }"}' | python3 -m json.tool
```

## 工作流状态

Linear使用带有`type`字段的`WorkflowState`对象。**6种状态类型：**

| 类型 | 描述 |
|------|-------------|
| `triage` | 需要审查的传入问题 |
| `backlog` | 已确认但尚未计划 |
| `unstarted` | 已计划/准备但尚未开始 |
| `started` | 正在积极处理 |
| `completed` | 已完成 |
| `canceled` | 不会做 |

每个团队都有自己的命名状态（例如，"进行中"是类型`started`）。要更改问题的状态，您需要目标状态的`stateId`（UUID）— 首先查询工作流状态。

**优先级值：** 0 = 无，1 = 紧急，2 = 高，3 = 中，4 = 低

## 常用查询

### 获取当前用户
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { id name email } }"}' | python3 -m json.tool
```

### 列出团队
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ teams { nodes { id name key } } }"}' | python3 -m json.tool
```

### 列出团队的工作流状态
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ workflowStates(filter: { team: { key: { eq: \"ENG\" } } }) { nodes { id name type } } }"}' | python3 -m json.tool
```

### 列出问题（前20个）
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(first: 20) { nodes { identifier title priority state { name type } assignee { name } team { key } url } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool
```

### 列出我分配的问题
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ viewer { assignedIssues(first: 25) { nodes { identifier title state { name type } priority url } } } }"}' | python3 -m json.tool
```

### 获取单个问题（通过标识符如ENG-123）
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issue(id: \"ENG-123\") { id identifier title description priority state { id name type } assignee { id name } team { key } project { name } labels { nodes { name } } comments { nodes { body user { name } createdAt } } url } }"}' | python3 -m json.tool
```

### 按文本搜索问题
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issueSearch(query: \"bug login\", first: 10) { nodes { identifier title state { name } assignee { name } url } } }"}' | python3 -m json.tool
```

### 按状态类型过滤问题
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(filter: { state: { type: { in: [\"started\"] } } }, first: 20) { nodes { identifier title state { name } assignee { name } } } }"}' | python3 -m json.tool
```

### 按团队和被分配者过滤
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(filter: { team: { key: { eq: \"ENG\" } }, assignee: { email: { eq: \"user@example.com\" } } }, first: 20) { nodes { identifier title state { name } priority } } }"}' | python3 -m json.tool
```

### 列出项目
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ projects(first: 20) { nodes { id name description progress lead { name } teams { nodes { key } } url } } }"}' | python3 -m json.tool
```

### 列出团队成员
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ users { nodes { id name email active } } }"}' | python3 -m json.tool
```

### 列出标签
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issueLabels { nodes { id name color } } }"}' | python3 -m json.tool
```

## 常用变更

### 创建问题
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation($input: IssueCreateInput!) { issueCreate(input: $input) { success issue { id identifier title url } } }",
    "variables": {
      "input": {
        "teamId": "TEAM_UUID",
        "title": "Fix login bug",
        "description": "Users cannot login with SSO",
        "priority": 2
      }
    }
  }' | python3 -m json.tool
```

### 更新问题状态
首先从上面的工作流状态查询中获取目标状态UUID，然后：
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { stateId: \"STATE_UUID\" }) { success issue { identifier state { name type } } } }"}' | python3 -m json.tool
```

### 分配问题
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { assigneeId: \"USER_UUID\" }) { success issue { identifier assignee { name } } } }"}' | python3 -m json.tool
```

### 设置优先级
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { priority: 1 }) { success issue { identifier priority } } }"}' | python3 -m json.tool
```

### 添加评论
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { commentCreate(input: { issueId: \"ISSUE_UUID\", body: \"Investigated. Root cause is X.\" }) { success comment { id body } } }"}' | python3 -m json.tool
```

### 设置截止日期
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { dueDate: \"2026-04-01\" }) { success issue { identifier dueDate } } }"}' | python3 -m json.tool
```

### 向问题添加标签
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { labelIds: [\"LABEL_UUID_1\", \"LABEL_UUID_2\"] }) { success issue { identifier labels { nodes { name } } } }"}' | python3 -m json.tool
```

### 将问题添加到项目
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "mutation { issueUpdate(id: \"ENG-123\", input: { projectId: \"PROJECT_UUID\" }) { success issue { identifier project { name } } } }"}' | python3 -m json.tool
```

### 创建项目
```bash
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "query": "mutation($input: ProjectCreateInput!) { projectCreate(input: $input) { success project { id name url } } }",
    "variables": {
      "input": {
        "name": "Q2 Auth Overhaul",
        "description": "Replace legacy auth with OAuth2 and PKCE",
        "teamIds": ["TEAM_UUID"]
      }
    }
  }' | python3 -m json.tool
```

## 分页

Linear使用Relay风格的游标分页：

```bash
# 第一页
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(first: 20) { nodes { identifier title } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool

# 下一页 — 使用上一个响应的endCursor
curl -s -X POST https://api.linear.app/graphql \
  -H "Authorization: $LINEAR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"query": "{ issues(first: 20, after: \"CURSOR_FROM_PREVIOUS\") { nodes { identifier title } pageInfo { hasNextPage endCursor } } }"}' | python3 -m json.tool
```

默认页面大小：50。最大：250。始终使用`first: N`来限制结果。

## 过滤参考

比较器：`eq`、`neq`、`in`、`nin`、`lt`、`lte`、`gt`、`gte`、`contains`、`startsWith`、`containsIgnoreCase`

使用`or: [...]`组合过滤器以实现OR逻辑（默认在过滤器对象内是AND）。

## 典型工作流程

1. **查询团队**以获取团队ID和密钥
2. **查询目标团队的工作流状态**以获取状态UUID
3. **列出或搜索问题**以找到需要处理的内容
4. **创建问题**，带有团队ID、标题、描述、优先级
5. **通过将`stateId`设置为目标工作流状态来更新状态**
6. **添加评论**以跟踪进度
7. **通过将`stateId`设置为团队的"已完成"类型状态来标记完成**

## 速率限制

- 每个API密钥5,000个请求/小时
- 3,000,000个复杂度点/小时
- 使用`first: N`来限制结果并降低复杂度成本
- 监视`X-RateLimit-Requests-Remaining`响应头

## 重要备注

- 始终对API调用使用带有`curl`的`terminal`工具 — 不要使用`web_extract`或`browser`
- 始终检查GraphQL响应中的`errors`数组 — HTTP 200仍然可能包含错误
- 如果在创建问题时省略了`stateId`，Linear默认为第一个待办事项状态
- `description`字段支持Markdown
- 使用`python3 -m json.tool`或`jq`来格式化JSON响应以提高可读性
