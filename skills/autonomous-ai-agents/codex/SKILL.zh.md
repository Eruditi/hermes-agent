---
name: codex
description: 将编码任务委托给 OpenAI Codex CLI 代理。用于构建功能、重构、PR 审查和批量修复问题。需要 codex CLI 和 git 仓库。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Coding-Agent, Codex, OpenAI, Code-Review, Refactoring]
    related_skills: [claude-code, hermes-agent]
---

# Codex CLI

通过 Hermes 终端将编码任务委托给 [Codex](https://github.com/openai/codex)。Codex 是 OpenAI 的自主编码代理 CLI。

## 前置条件

- 安装 Codex：`npm install -g @openai/codex`
- 配置 OpenAI API 密钥
- **必须在 git 仓库内运行** — Codex 拒绝在仓库外运行
- 在终端调用中使用 `pty=true` — Codex 是交互式终端应用

## 单次任务

```
terminal(command="codex exec 'Add dark mode toggle to settings'", workdir="~/project", pty=true)
```

对于临时工作（Codex 需要 git 仓库）：
```
terminal(command="cd $(mktemp -d) && git init && codex exec 'Build a snake game in Python'", pty=true)
```

## 后台模式（长任务）

```
# 带 PTY 在后台启动
terminal(command="codex exec --full-auto 'Refactor the auth module'", workdir="~/project", background=true, pty=true)
# 返回 session_id

# 监控进度
process(action="poll", session_id="<id>")
process(action="log", session_id="<id>")

# 如果 Codex 询问问题，发送输入
process(action="submit", session_id="<id>", data="yes")

# 必要时杀死
process(action="kill", session_id="<id>")
```

## 关键标志

| 标志 | 效果 |
|------|--------|
| `exec "prompt"` | 单次执行，完成后退出 |
| `--full-auto` | 沙盒化但自动批准工作区中的文件更改 |
| `--yolo` | 无沙盒，无批准（最快，最危险） |

## PR 审查

克隆到临时目录以进行安全审查：

```
terminal(command="REVIEW=$(mktemp -d) && git clone https://github.com/user/repo.git $REVIEW && cd $REVIEW && gh pr checkout 42 && codex review --base origin/main", pty=true)
```

## 使用工作树进行并行问题修复

```
# 创建工作树
terminal(command="git worktree add -b fix/issue-78 /tmp/issue-78 main", workdir="~/project")
terminal(command="git worktree add -b fix/issue-99 /tmp/issue-99 main", workdir="~/project")

# 在每个工作树中启动 Codex
terminal(command="codex --yolo exec 'Fix issue #78: <description>. Commit when done.'", workdir="/tmp/issue-78", background=true, pty=true)
terminal(command="codex --yolo exec 'Fix issue #99: <description>. Commit when done.'", workdir="/tmp/issue-99", background=true, pty=true)

# 监控
process(action="list")

# 完成后，推送并创建 PR
terminal(command="cd /tmp/issue-78 && git push -u origin fix/issue-78")
terminal(command="gh pr create --repo user/repo --head fix/issue-78 --title 'fix: ...' --body '...'")

# 清理
terminal(command="git worktree remove /tmp/issue-78", workdir="~/project")
```

## 批量 PR 审查

```
# 获取所有 PR 引用
terminal(command="git fetch origin '+refs/pull/*/head:refs/remotes/origin/pr/*'", workdir="~/project")

# 并行审查多个 PR
terminal(command="codex exec 'Review PR #86. git diff origin/main...origin/pr/86'", workdir="~/project", background=true, pty=true)
terminal(command="codex exec 'Review PR #87. git diff origin/main...origin/pr/87'", workdir="~/project", background=true, pty=true)

# 发布结果
terminal(command="gh pr comment 86 --body '<review>'", workdir="~/project")
```

## 规则

1. **始终使用 `pty=true`** — Codex 是交互式终端应用，没有 PTY 会挂起
2. **需要 Git 仓库** — Codex 不会在 git 目录外运行。使用 `mktemp -d && git init` 进行临时工作
3. **对单次任务使用 `exec`** — `codex exec "prompt"` 运行并干净退出
4. **对构建使用 `--full-auto`** — 自动批准沙盒内的更改
5. **对长任务使用后台** — 使用 `background=true` 并通过 `process` 工具监控
6. **不要干扰** — 使用 `poll`/`log` 监控，对长时间运行的任务保持耐心
7. **并行是可以的** — 同时运行多个 Codex 进程进行批处理工作
