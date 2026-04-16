---
name: github-code-review
description: 通过分析 git diff、在 PR 上留下内联评论以及执行彻底的推送前审查来审查代码变更。使用 gh CLI 或回退到 git + GitHub REST API via curl。
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, 代码审查, Pull-Requests, Git, 质量]
    related_skills: [github-auth, github-pr-workflow]
---

# GitHub 代码审查

在推送前审查本地变更，或审查 GitHub 上开放的 PR。此技能的大部分使用纯 `git` — `gh`/`curl` 拆分仅对 PR 级别的交互重要。

## 前置条件

- 已通过 GitHub 认证（参见 `github-auth` 技能）
- 在 git 仓库中

### 设置（用于 PR 交互）

```bash
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  AUTH="gh"
else
  AUTH="git"
  if [ -z "$GITHUB_TOKEN" ]; then
    if [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
      GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
    elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
      GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
    fi
  fi
fi

REMOTE_URL=$(git remote get-url origin)
OWNER_REPO=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]||; s|\.git$||')
OWNER=$(echo "$OWNER_REPO" | cut -d/ -f1)
REPO=$(echo "$OWNER_REPO" | cut -d/ -f2)
```

---

## 1. 审查本地变更（推送前）

这是纯 `git` — 适用于任何地方，不需要 API。

### 获取差异

```bash
# 暂存的变更（将要提交的内容）
git diff --staged

# 与 main 相比的所有变更（PR 会包含的内容）
git diff main...HEAD

# 仅文件名
git diff main...HEAD --name-only

# 统计摘要（每个文件的插入/删除）
git diff main...HEAD --stat
```

### 审查策略

1. **先获取大局观:**

```bash
git diff main...HEAD --stat
git log main..HEAD --oneline
```

2. **逐文件审查** — 对变更的文件使用 `read_file` 获取完整上下文，使用 diff 查看变更内容：

```bash
git diff main...HEAD -- src/auth/login.py
```

3. **检查常见问题:**

```bash
# 遗留的调试语句、TODO、console.log
git diff main...HEAD | grep -n "print(\|console\.log\|TODO\|FIXME\|HACK\|XXX\|debugger"

# 意外暂存的大文件
git diff main...HEAD --stat | sort -t'|' -k2 -rn | head -10

# 密钥或凭据模式
git diff main...HEAD | grep -in "password\|secret\|api_key\|token.*=\|private_key"

# 合并冲突标记
git diff main...HEAD | grep -n "<<<<<<\|>>>>>>\|======="
```

4. **向用户展示结构化反馈**。

### 审查输出格式

审查本地变更时，按此结构展示发现：

```
## 代码审查摘要

### 严重
- **src/auth.py:45** — SQL 注入：用户输入直接传递给查询。
  建议：使用参数化查询。

### 警告
- **src/models/user.py:23** — 密码以明文存储。使用 bcrypt 或 argon2。
- **src/api/routes.py:112** — 登录端点没有速率限制。

### 建议
- **src/utils/helpers.py:8** — 与 `src/core/utils.py:34` 中的逻辑重复。合并。
- **tests/test_auth.py** — 缺少边缘情况：过期令牌测试。

### 看起来不错
- 中间件层的关注点清晰分离
- 主流程的测试覆盖率良好
```

---

## 2. 在 GitHub 上审查 Pull Request

### 查看 PR 详情

**使用 gh:**

```bash
gh pr view 123
gh pr diff 123
gh pr diff 123 --name-only
```

**使用 git + curl:**

```bash
PR_NUMBER=123

# 获取 PR 详情
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "
import sys, json
pr = json.load(sys.stdin)
print(f\"Title: {pr['title']}\")
print(f\"Author: {pr['user']['login']}\")
print(f\"Branch: {pr['head']['ref']} -> {pr['base']['ref']}\")
print(f\"State: {pr['state']}\")
print(f\"Body:\n{pr['body']}\")"

# 列出变更的文件
curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/files \
  | python3 -c "
import sys, json
for f in json.load(sys.stdin):
    print(f\"{f['status']:10} +{f['additions']:-4} -{f['deletions']:-4}  {f['filename']}\")"
```

### 本地检出 PR 以进行完整审查

这使用纯 `git` — 不需要 `gh`：

```bash
# 获取 PR 分支并检出
git fetch origin pull/123/head:pr-123
git checkout pr-123

# 现在您可以使用 read_file、search_files、运行测试等。

# 查看与基础分支的差异
git diff main...pr-123
```

**使用 gh（快捷方式）:**

```bash
gh pr checkout 123
```

### 在 PR 上留下评论

**常规 PR 评论 — 使用 gh:**

```bash
gh pr comment 123 --body "总体看起来不错，下面有一些建议。"
```

**常规 PR 评论 — 使用 curl:**

```bash
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/issues/$PR_NUMBER/comments \
  -d '{"body": "总体看起来不错，下面有一些建议。"}'
```

### 留下内联审查评论

**单个内联评论 — 使用 gh（通过 API）:**

```bash
HEAD_SHA=$(gh pr view 123 --json headRefOid --jq '.headRefOid')

gh api repos/$OWNER/$REPO/pulls/123/comments \
  --method POST \
  -f body="这可以用列表推导简化。" \
  -f path="src/auth/login.py" \
  -f commit_id="$HEAD_SHA" \
  -f line=45 \
  -f side="RIGHT"
```

**单个内联评论 — 使用 curl:**

```bash
# 获取头部提交 SHA
HEAD_SHA=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/comments \
  -d "{
    \"body\": \"这可以用列表推导简化。\",
    \"path\": \"src/auth/login.py\",
    \"commit_id\": \"$HEAD_SHA\",
    \"line\": 45,
    \"side\": \"RIGHT\"
  }"
```

### 提交正式审查（批准 / 请求变更）

**使用 gh:**

```bash
gh pr review 123 --approve --body "LGTM!"
gh pr review 123 --request-changes --body "请参阅内联评论。"
gh pr review 123 --comment --body "一些建议，没有阻塞性内容。"
```

**使用 curl — 多评论审查原子提交:**

```bash
HEAD_SHA=$(curl -s \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$OWNER/$REPO/pulls/$PR_NUMBER/reviews \
  -d "{
    \"commit_id\": \"$HEAD_SHA\",
    \"event\": \"COMMENT\",
    \"body\": \"Hermes Agent 代码审查\",
    \"comments\": [
      {\"path\": \"src/auth.py\", \"line\": 45, \"body\": \"使用参数化查询防止 SQL 注入。\"},
      {\"path\": \"src/models/user.py\", \"line\": 23, \"body\": \"存储前用 bcrypt 哈希密码。\"},
      {\"path\": \"tests/test_auth.py\", \"line\": 1, \"body\": \"添加过期令牌边缘情况的测试。\"}
    ]
  }"
```

事件值: `"APPROVE"`, `"REQUEST_CHANGES"`, `"COMMENT"`

`line` 字段指的是文件*新*版本中的行号。对于已删除的行，使用 `"side": "LEFT"`。

---

## 3. 审查清单

执行代码审查（本地或 PR）时，系统地检查：

### 正确性
- 代码是否按声称的那样工作？
- 边缘情况是否已处理（空输入、null、大数据、并发访问）？
- 错误路径是否已优雅处理？

### 安全性
- 没有硬编码的密钥、凭据或 API 密钥
- 对面向用户的输入进行输入验证
- 没有 SQL 注入、XSS 或路径遍历
- 在需要的地方进行身份验证/授权检查

### 代码质量
- 清晰的命名（变量、函数、类）
- 没有不必要的复杂性或过早的抽象
- DRY — 没有应该提取的重复逻辑
- 函数专注（单一职责）

### 测试
- 新代码路径是否已测试？
- 主流程和错误情况是否已覆盖？
- 测试是否可读且可维护？

### 性能
- 没有 N+1 查询或不必要的循环
- 在有益的地方适当缓存
- 异步代码路径中没有阻塞操作

### 文档
- 公共 API 已文档化
- 非显而易见的逻辑有解释"为什么"的注释
- 如果行为变更，README 已更新

---

## 4. 推送前审查工作流程

当用户要求您"审查代码"或"推送前检查"时：

1. `git diff main...HEAD --stat` — 查看变更范围
2. `git diff main...HEAD` — 阅读完整差异
3. 对于每个变更的文件，如果需要更多上下文，使用 `read_file`
4. 应用上面的清单
5. 以结构化格式展示发现（严重 / 警告 / 建议 / 看起来不错）
6. 如果发现严重问题，在用户推送前主动修复

---

## 5. PR 审查工作流程（端到端）

当用户要求您"审查 PR #N"、"查看这个 PR"或给您一个 PR URL 时，遵循此流程：

### 步骤 1: 设置环境

```bash
source "${HERMES_HOME:-$HOME/.hermes}/skills/github/github-auth/scripts/gh-env.sh"
# 或运行此技能顶部的内联设置块
```

### 步骤 2: 收集 PR 上下文

获取 PR 元数据、描述和变更文件列表，以便在深入代码之前了解范围。

**使用 gh:**
```bash
gh pr view 123
gh pr diff 123 --name-only
gh pr checks 123
```

**使用 curl:**
```bash
PR_NUMBER=123

# PR 详情（标题、作者、描述、分支）
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER

# 带行数的变更文件
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER/files
```

### 步骤 3: 本地检出 PR

这让您可以完全访问 `read_file`、`search_files` 以及运行测试的能力。

```bash
git fetch origin pull/$PR_NUMBER/head:pr-$PR_NUMBER
git checkout pr-$PR_NUMBER
```

### 步骤 4: 阅读差异并理解变更

```bash
# 与基础分支的完整差异
git diff main...HEAD

# 或者对于大型 PR 逐文件
git diff main...HEAD --name-only
# 然后对于每个文件：
git diff main...HEAD -- path/to/file.py
```

对于每个变更的文件，使用 `read_file` 查看变更周围的完整上下文 — 仅差异可能会遗漏仅通过周围代码可见的问题。

### 步骤 5: 本地运行自动化检查（如果适用）

```bash
# 如果有测试套件，运行测试
python -m pytest 2>&1 | tail -20
# 或：npm test, cargo test, go test ./..., 等等。

# 如果配置了 linter，运行它
ruff check . 2>&1 | head -30
# 或：eslint, clippy, 等等。
```

### 步骤 6: 应用审查清单（第 3 部分）

逐个检查每个类别：正确性、安全性、代码质量、测试、性能、文档。

### 步骤 7: 将审查发布到 GitHub

收集您的发现并作为带有内联评论的正式审查提交。

**使用 gh:**
```bash
# 如果没有问题 — 批准
gh pr review $PR_NUMBER --approve --body "由 Hermes Agent 审查。代码看起来干净 — 良好的测试覆盖率，没有安全问题。"

# 如果发现问题 — 用内联评论请求变更
gh pr review $PR_NUMBER --request-changes --body "发现了一些问题 — 请参阅内联评论。"
```

**使用 curl — 带有多个内联评论的原子审查:**
```bash
HEAD_SHA=$(curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER \
  | python3 -c "import sys,json; print(json.load(sys.stdin)['head']['sha'])")

# 构建审查 JSON — 事件是 APPROVE、REQUEST_CHANGES 或 COMMENT
curl -s -X POST \
  -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/repos/$GH_OWNER/$GH_REPO/pulls/$PR_NUMBER/reviews \
  -d "{
    \"commit_id\": \"$HEAD_SHA\",
    \"event\": \"REQUEST_CHANGES\",
    \"body\": \"## Hermes Agent 审查\n\n发现 2 个问题，1 个建议。请参阅内联评论。\",
    \"comments\": [
      {\"path\": \"src/auth.py\", \"line\": 45, \"body\": \"🔴 **严重:** 用户输入直接传递给 SQL 查询 — 使用参数化查询。\"},
      {\"path\": \"src/models.py\", \"line\": 23, \"body\": \"⚠️ **警告:** 密码未哈希存储。\"},
      {\"path\": \"src/utils.py\", \"line\": 8, \"body\": \"💡 **建议:** 这与 core/utils.py:34 中的逻辑重复。\"}
    ]
  }"
```

### 步骤 8: 也发布摘要评论

除了内联评论外，留下顶级摘要，以便 PR 作者一眼就能看到全貌。使用 `references/review-output-template.md` 中的审查输出格式。

**使用 gh:**
```bash
gh pr comment $PR_NUMBER --body "$(cat <<'EOF'
## 代码审查摘要

**结论: 请求变更** (2 个问题，1 个建议)

### 🔴 严重
- **src/auth.py:45** — SQL 注入漏洞

### ⚠️ 警告
- **src/models.py:23** — 明文密码存储

### 💡 建议
- **src/utils.py:8** — 重复逻辑，考虑合并

### ✅ 看起来不错
- 清晰的 API 设计
- 中间件层的错误处理良好

---
*由 Hermes Agent 审查*
EOF
)"
```

### 步骤 9: 清理

```bash
git checkout main
git branch -D pr-$PR_NUMBER
```

### 决定: 批准 vs 请求变更 vs 评论

- **批准** — 没有严重或警告级别的问题，只有小建议或全部通过
- **请求变更** — 任何应该在合并前修复的严重或警告级别的问题
- **评论** — 观察和建议，但没有阻塞性内容（当您不确定或 PR 是草稿时使用）
