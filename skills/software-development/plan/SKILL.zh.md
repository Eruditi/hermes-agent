---
name: plan
description: Hermes 的计划模式 — 检查上下文，将 markdown 计划写入活动工作区的 `.hermes/plans/` 目录，并且不执行工作。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [规划, 计划模式, 实施, 工作流程]
    related_skills: [writing-plans, subagent-driven-development]
---

# 计划模式

当用户想要计划而不是执行时使用此技能。

## 核心行为

对于这个回合，您只在规划。

- 不要实施代码。
- 除了计划 markdown 文件外，不要编辑项目文件。
- 不要运行变更性的终端命令、提交、推送或执行外部操作。
- 您可以在需要时使用只读命令/工具检查仓库或其他上下文。
- 您的交付物是保存在活动工作区 `.hermes/plans/` 下的 markdown 计划。

## 输出要求

编写具体且可操作的 markdown 计划。

在相关时包括：
- 目标
- 当前上下文 / 假设
- 提议的方法
- 分步计划
- 可能变更的文件
- 测试 / 验证
- 风险、权衡和开放性问题

如果任务与代码相关，包括确切的文件路径、可能的测试目标和验证步骤。

## 保存位置

使用 `write_file` 将计划保存在：
- `.hermes/plans/YYYY-MM-DD_HHMMSS-<slug>.md`

将其视为相对于活动工作目录 / 后端工作区。Hermes 文件工具是后端感知的，因此使用此相对路径将计划与本地、docker、ssh、modal 和 daytona 后端上的工作区保持在一起。

如果运行时提供了特定的目标路径，请使用该确切路径。
如果没有，请自己在 `.hermes/plans/` 下创建一个合理的带时间戳的文件名。

## 交互风格

- 如果请求足够清晰，直接编写计划。
- 如果 `/plan` 没有明确的指令，从当前对话上下文中推断任务。
- 如果它真的未指定，问一个简短的澄清问题而不是猜测。
- 保存计划后，简要回复您计划的内容和保存的路径。
