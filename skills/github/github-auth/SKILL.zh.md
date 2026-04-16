---
name: github-auth
description: 使用 git（通用可用）或 gh CLI 为代理设置 GitHub 身份验证。涵盖 HTTPS 令牌、SSH 密钥、凭据助手和 gh auth — 带有自动选择正确方法的检测流程。
version: 1.1.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [GitHub, 身份验证, Git, gh-cli, SSH, 设置]
    related_skills: [github-pr-workflow, github-code-review, github-issues, github-repo-management]
---

# GitHub 身份验证设置

此技能设置身份验证，以便代理可以与 GitHub 仓库、PR、issues 和 CI 一起工作。它涵盖两条路径：

- **`git`（始终可用）** — 使用 HTTPS 个人访问令牌或 SSH 密钥
- **`gh` CLI（如果已安装）** — 更丰富的 GitHub API 访问，身份验证流程更简单

## 检测流程

当用户要求您与 GitHub 一起工作时，首先运行此检查：

```bash
# 检查可用的内容
git --version
gh --version 2>/dev/null || echo "gh not installed"

# 检查是否已通过身份验证
gh auth status 2>/dev/null || echo "gh not authenticated"
git config --global credential.helper 2>/dev/null || echo "no git credential helper"
```

**决策树：**
1. 如果 `gh auth status` 显示已通过身份验证 → 您很好，对所有内容使用 `gh`
2. 如果 `gh` 已安装但未通过身份验证 → 使用下面的"gh auth"方法
3. 如果 `gh` 未安装 → 使用下面的"仅 git"方法（不需要 sudo）

---

## 方法 1: 仅 Git 身份验证（无 gh，无 sudo）

这适用于任何安装了 `git` 的机器。不需要 root 访问权限。

### 选项 A: 带个人访问令牌的 HTTPS（推荐）

这是最便携的方法 — 适用于任何地方，不需要 SSH 配置。

**步骤 1: 创建个人访问令牌**

告诉用户前往：**https://github.com/settings/tokens**

- 点击"Generate new token (classic)"
- 给它一个名称，如"hermes-agent"
- 选择作用域：
  - `repo`（完整仓库访问 — 读取、写入、推送、PR）
  - `workflow`（触发和管理 GitHub Actions）
  - `read:org`（如果与组织仓库一起工作）
- 设置过期时间（90 天是个好的默认值）
- 复制令牌 — 它不会再显示

**步骤 2: 配置 git 存储令牌**

```bash
# 设置凭据助手以缓存凭据
# "store" 以明文保存到 ~/.git-credentials（简单、持久）
git config --global credential.helper store

# 现在执行一个触发身份验证的测试操作 — git 将提示输入凭据
# 用户名: <their-github-username>
# 密码: <粘贴个人访问令牌，不是他们的 GitHub 密码>
git ls-remote https://github.com/<their-username>/<any-repo>.git
```

输入一次凭据后，它们会被保存并在所有未来操作中重用。

**替代：缓存助手（凭据从内存中过期）**

```bash
# 在内存中缓存 8 小时（28800 秒）而不是保存到磁盘
git config --global credential.helper 'cache --timeout=28800'
```

**替代：直接在远程 URL 中设置令牌（每个仓库）**

```bash
# 在远程 URL 中嵌入令牌（完全避免凭据提示）
git remote set-url origin https://<username>:<token>@github.com/<owner>/<repo>.git
```

**步骤 3: 配置 git 身份**

```bash
# 提交所需 — 设置姓名和邮箱
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

**步骤 4: 验证**

```bash
# 测试推送访问（这现在应该可以在没有任何提示的情况下工作）
git ls-remote https://github.com/<their-username>/<any-repo>.git

# 验证身份
git config --global user.name
git config --global user.email
```

### 选项 B: SSH 密钥身份验证

适用于更喜欢 SSH 或已经设置了密钥的用户。

**步骤 1: 检查现有 SSH 密钥**

```bash
ls -la ~/.ssh/id_*.pub 2>/dev/null || echo "No SSH keys found"
```

**步骤 2: 如果需要生成密钥**

```bash
# 生成 ed25519 密钥（现代、安全、快速）
ssh-keygen -t ed25519 -C "their-email@example.com" -f ~/.ssh/id_ed25519 -N ""

# 显示公钥供他们添加到 GitHub
cat ~/.ssh/id_ed25519.pub
```

告诉用户在以下位置添加公钥：**https://github.com/settings/keys**
- 点击"New SSH key"
- 粘贴公钥内容
- 给它一个标题，如"hermes-agent-<machine-name>"

**步骤 3: 测试连接**

```bash
ssh -T git@github.com
# 预期: "Hi <username>! You've successfully authenticated..."
```

**步骤 4: 配置 git 为 GitHub 使用 SSH**

```bash
# 自动将 HTTPS GitHub URL 重写为 SSH
git config --global url."git@github.com:".insteadOf "https://github.com/"
```

**步骤 5: 配置 git 身份**

```bash
git config --global user.name "Their Name"
git config --global user.email "their-email@example.com"
```

---

## 方法 2: gh CLI 身份验证

如果安装了 `gh`，它一步处理 API 访问和 git 凭据。

### 交互式浏览器登录（桌面）

```bash
gh auth login
# 选择: GitHub.com
# 选择: HTTPS
# 通过浏览器进行身份验证
```

### 基于令牌的登录（无头 / SSH 服务器）

```bash
echo "<THEIR_TOKEN>" | gh auth login --with-token

# 通过 gh 设置 git 凭据
gh auth setup-git
```

### 验证

```bash
gh auth status
```

---

## 不使用 gh 使用 GitHub API

当 `gh` 不可用时，您仍然可以使用 `curl` 和个人访问令牌访问完整的 GitHub API。这就是其他 GitHub 技能实现其回退方案的方式。

### 为 API 调用设置令牌

```bash
# 选项 1: 导出为环境变量（首选 — 使其不在命令中）
export GITHUB_TOKEN="<token>"

# 然后在 curl 调用中使用：
curl -s -H "Authorization: token $GITHUB_TOKEN" \
  https://api.github.com/user
```

### 从 Git 凭据中提取令牌

如果 git 凭据已配置（通过 credential.helper store），可以提取令牌：

```bash
# 从 git 凭据存储中读取
grep "github.com" ~/.git-credentials 2>/dev/null | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|'
```

### 助手: 检测身份验证方法

在任何 GitHub 工作流程开始时使用此模式：

```bash
# 首先尝试 gh，回退到 git + curl
if command -v gh &>/dev/null && gh auth status &>/dev/null; then
  echo "AUTH_METHOD=gh"
elif [ -n "$GITHUB_TOKEN" ]; then
  echo "AUTH_METHOD=curl"
elif [ -f ~/.hermes/.env ] && grep -q "^GITHUB_TOKEN=" ~/.hermes/.env; then
  export GITHUB_TOKEN=$(grep "^GITHUB_TOKEN=" ~/.hermes/.env | head -1 | cut -d= -f2 | tr -d '\n\r')
  echo "AUTH_METHOD=curl"
elif grep -q "github.com" ~/.git-credentials 2>/dev/null; then
  export GITHUB_TOKEN=$(grep "github.com" ~/.git-credentials | head -1 | sed 's|https://[^:]*:\([^@]*\)@.*|\1|')
  echo "AUTH_METHOD=curl"
else
  echo "AUTH_METHOD=none"
  echo "Need to set up authentication first"
fi
```

---

## 故障排除

| 问题 | 解决方案 |
|---------|----------|
| `git push` 要求输入密码 | GitHub 已禁用密码身份验证。使用个人访问令牌作为密码，或切换到 SSH |
| `remote: Permission to X denied` | 令牌可能缺少 `repo` 作用域 — 使用正确的作用域重新生成 |
| `fatal: Authentication failed` | 缓存的凭据可能已过期 — 运行 `git credential reject` 然后重新身份验证 |
| `ssh: connect to host github.com port 22: Connection refused` | 尝试通过 HTTPS 端口的 SSH：将 `Host github.com` 与 `Port 443` 和 `Hostname ssh.github.com` 添加到 `~/.ssh/config` |
| 凭据不持久 | 检查 `git config --global credential.helper` — 必须是 `store` 或 `cache` |
| 多个 GitHub 账户 | 在 `~/.ssh/config` 中使用每个主机别名的不同 SSH 密钥，或每个仓库的凭据 URL |
| `gh: command not found` + 无 sudo | 使用上面的仅 git 方法 1 — 不需要安装 |
