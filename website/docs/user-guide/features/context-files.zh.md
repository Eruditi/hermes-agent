---
sidebar_position: 8
title: "上下文文件"
description: "项目上下文文件 — .hermes.md、AGENTS.md、CLAUDE.md、全局 SOUL.md 和 .cursorrules — 自动注入到每个对话中"
---

# 上下文文件

Hermes Agent 自动发现并加载塑造其行为方式的上下文文件。有些是项目本地的，从您的工作目录中发现。`SOUL.md` 现在是 Hermes 实例的全局文件，仅从 `HERMES_HOME` 加载。

## 支持的上下文文件

| 文件 | 用途 | 发现 |
|------|---------|-----------| 
| **.hermes.md** / **HERMES.md** | 项目指令（最高优先级） | 遍历到 git 根目录 |
| **AGENTS.md** | 项目指令、约定、架构 | 启动时的 CWD + 逐步子目录 |
| **CLAUDE.md** | Claude Code 上下文文件（也被检测） | 启动时的 CWD + 逐步子目录 |
| **SOUL.md** | 此 Hermes 实例的全局个性和语气自定义 | 仅 `HERMES_HOME/SOUL.md` |
| **.cursorrules** | Cursor IDE 编码约定 | 仅 CWD |
| **.cursor/rules/*.mdc** | Cursor IDE 规则模块 | 仅 CWD |

:::info 优先级系统
每个会话仅加载**一个**项目上下文类型（第一个匹配获胜）：`.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`。**SOUL.md** 始终作为代理身份（插槽 #1）独立加载。
:::

## AGENTS.md

`AGENTS.md` 是主要的项目上下文文件。它告诉代理您的项目结构、要遵循的约定以及任何特殊指令。

### 渐进式子目录发现

在会话开始时，Hermes 将工作目录中的 `AGENTS.md` 加载到系统提示中。随着代理在会话期间导航到子目录（通过 `read_file`、`terminal`、`search_files` 等），它**逐步发现**这些目录中的上下文文件，并在它们变得相关时将它们注入到对话中。

```
my-project/
├── AGENTS.md              ← 在启动时加载（系统提示）
├── frontend/
│   └── AGENTS.md          ← 当代理读取 frontend/ 文件时发现
├── backend/
│   └── AGENTS.md          ← 当代理读取 backend/ 文件时发现
└── shared/
    └── AGENTS.md          ← 当代理读取 shared/ 文件时发现
```

与启动时加载所有内容相比，这种方法有两个优势：
- **无系统提示膨胀** — 子目录提示仅在需要时出现
- **提示缓存保留** — 系统提示在各个回合保持稳定

每个子目录每个会话最多检查一次。发现还遍历父目录，因此读取 `backend/src/main.py` 将发现 `backend/AGENTS.md`，即使 `backend/src/` 没有自己的上下文文件。

:::info
子目录上下文文件通过与启动上下文文件相同的[安全扫描](#安全提示注入保护)。恶意文件被阻止。
:::

### 示例 AGENTS.md

```markdown
# Project Context

This is a Next.js 14 web application with a Python FastAPI backend.

## Architecture
- Frontend: Next.js 14 with App Router in `/frontend`
- Backend: FastAPI in `/backend`, uses SQLAlchemy ORM
- Database: PostgreSQL 16
- Deployment: Docker Compose on a Hetzner VPS

## Conventions
- Use TypeScript strict mode for all frontend code
- Python code follows PEP 8, use type hints everywhere
- All API endpoints return JSON with `{data, error, meta}` shape
- Tests go in `__tests__/` directories (frontend) or `tests/` (backend)

## Important Notes
- Never modify migration files directly — use Alembic commands
- The `.env.local` file has real API keys, don't commit it
- Frontend port is 3000, backend is 8000, DB is 5432
```

## SOUL.md

`SOUL.md` 控制代理的个性、语气和沟通风格。请参阅[个性](/docs/user-guide/features/personality)页面获取完整详细信息。

**位置：**

- `~/.hermes/SOUL.md`
- 或者如果您使用自定义主目录运行 Hermes，则为 `$HERMES_HOME/SOUL.md`

重要详细信息：

- 如果尚不存在，Hermes 会自动种子化默认 `SOUL.md`
- Hermes 仅从 `HERMES_HOME` 加载 `SOUL.md`
- Hermes 不会在工作目录中探测 `SOUL.md`
- 如果文件为空，则不会从 `SOUL.md` 向提示添加任何内容
- 如果文件有内容，则在扫描和截断后逐字注入内容

## .cursorrules

Hermes 与 Cursor IDE 的 `.cursorrules` 文件和 `.cursor/rules/*.mdc` 规则模块兼容。如果这些文件存在于您的项目根目录中，并且没有找到更高优先级的上下文文件（`.hermes.md`、`AGENTS.md` 或 `CLAUDE.md`），它们将作为项目上下文加载。

这意味着当使用 Hermes 时，您现有的 Cursor 约定会自动应用。

## 上下文文件如何加载

### 在启动时（系统提示）

上下文文件由 `agent/prompt_builder.py` 中的 `build_context_files_prompt()` 加载：

1. **扫描工作目录** — 检查 `.hermes.md` → `AGENTS.md` → `CLAUDE.md` → `.cursorrules`（第一个匹配获胜）
2. **读取内容** — 每个文件作为 UTF-8 文本读取
3. **安全扫描** — 检查内容中的提示注入模式
4. **截断** — 超过 20,000 字符的文件被头/尾截断（70% 头、20% 尾，中间有标记）
5. **组装** — 所有部分在 `# Project Context` 标题下组合
6. **注入** — 组装的内容被添加到系统提示中

### 在会话期间（逐步发现）

`agent/subdirectory_hints.py` 中的 `SubdirectoryHintTracker` 监视工具调用参数中的文件路径：

1. **路径提取** — 每次工具调用后，从参数（`path`、`workdir`、shell 命令）中提取文件路径
2. **祖先遍历** — 检查目录和最多 5 个父目录（在已访问目录处停止）
3. **提示加载** — 如果找到 `AGENTS.md`、`CLAUDE.md` 或 `.cursorrules`，则加载它（每个目录第一个匹配）
4. **安全扫描** — 与启动文件相同的提示注入扫描
5. **截断** — 每个文件上限为 8,000 字符
6. **注入** — 附加到工具结果，因此模型在上下文中自然看到它

最终提示部分大致如下：

```text
# Project Context

The following project context files have been loaded and should be followed:

## AGENTS.md

[Your AGENTS.md content here]

## .cursorrules

[Your .cursorrules content here]

[Your SOUL.md content here]
```

请注意，SOUL 内容直接插入，没有额外的包装文本。

## 安全：提示注入保护

所有上下文文件在包含之前都会被扫描以查找潜在的提示注入。扫描器检查：

- **指令覆盖尝试**："ignore previous instructions"、"disregard your rules"
- **欺骗模式**："do not tell the user"
- **系统提示覆盖**："system prompt override"
- **隐藏 HTML 注释**：`<!-- ignore instructions -->`
- **隐藏 div 元素**：`<div style="display:none">`
- **凭据泄露**：`curl ... $API_KEY`
- **机密文件访问**：`cat .env`、`cat credentials`
- **不可见字符**：零宽度空格、双向覆盖、单词连接符

如果检测到任何威胁模式，文件会被阻止：

```
[BLOCKED: AGENTS.md contained potential prompt injection (prompt_injection). Content not loaded.]
```

:::warning
此扫描器可防止常见的注入模式，但它不能替代在共享存储库中审查上下文文件。始终验证您未创作的项目中的 AGENTS.md 内容。
:::

## 大小限制

| 限制 | 值 |
|-------|-------|
| 每个文件的最大字符数 | 20,000（~7,000 tokens） |
| 头截断比率 | 70% |
| 尾截断比率 | 20% |
| 截断标记 | 10%（显示字符计数并建议使用文件工具） |

当文件超过 20,000 字符时，截断消息读取：

```
[...truncated AGENTS.md: kept 14000+4000 of 25000 chars. Use file tools to read the full file.]
```

## 有效上下文文件的提示

:::tip AGENTS.md 的最佳实践
1. **保持简洁** — 保持远低于 20K 字符；代理每个回合都会阅读它
2. **使用标题结构化** — 使用 `##` 部分用于架构、约定、重要说明
3. **包含具体示例** — 显示首选代码模式、API 形状、命名约定
4. **提到不要做什么** — "never modify migration files directly"
5. **列出关键路径和端口** — 代理将这些用于终端命令
6. **随着项目的发展进行更新** — 过时的上下文比没有上下文更糟
:::

### 每个子目录的上下文

对于单体存储库，将子目录特定的指令放在嵌套的 AGENTS.md 文件中：

```markdown
<!-- frontend/AGENTS.md -->
# Frontend Context

- Use `pnpm` not `npm` for package management
- Components go in `src/components/`, pages in `src/app/`
- Use Tailwind CSS, never inline styles
- Run tests with `pnpm test`
```

```markdown
<!-- backend/AGENTS.md -->
# Backend Context

- Use `poetry` for dependency management
- Run the dev server with `poetry run uvicorn main:app --reload`
- All endpoints need OpenAPI docstrings
- Database models are in `models/`, schemas in `schemas/`
```
