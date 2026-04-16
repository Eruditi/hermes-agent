---
name: writing-plans
description: 当您有多步骤任务的规范或需求时使用。创建全面的实施计划，包含小任务、确切的文件路径和完整的代码示例。
version: 1.1.0
author: Hermes Agent (改编自 obra/superpowers)
license: MIT
metadata:
  hermes:
    tags: [规划, 设计, 实施, 工作流程, 文档]
    related_skills: [subagent-driven-development, test-driven-development, requesting-code-review]
---

# 编写实施计划

## 概述

编写全面的实施计划，假设实施者对代码库零上下文且品味可疑。记录他们需要的一切：要触摸哪些文件、完整的代码、测试命令、要检查的文档、如何验证。给他们小任务。DRY。YAGNI。TDD。频繁提交。

假设实施者是熟练的开发人员，但对工具集或问题领域几乎一无所知。假设他们不太了解良好的测试设计。

**核心原则：** 好的计划使实施变得显而易见。如果有人必须猜测，计划就不完整。

## 何时使用

**在以下情况前始终使用：**
- 实施多步骤功能
- 分解复杂需求
- 通过 subagent-driven-development 委托给子代理

**在以下情况时不要跳过：**
- 功能看起来简单（假设导致 bug）
- 您计划自己实施（未来的您需要指导）
- 独自工作（文档很重要）

## 小任务粒度

**每个任务 = 2-5 分钟的专注工作。**

每个步骤都是一个动作：
- "编写失败的测试" — 步骤
- "运行它以确保它失败" — 步骤
- "实施最小代码以使测试通过" — 步骤
- "运行测试并确保它们通过" — 步骤
- "提交" — 步骤

**太大:**
```markdown
### 任务 1: 构建身份验证系统
[5 个文件中的 50 行代码]
```

**正确大小:**
```markdown
### 任务 1: 创建带 email 字段的 User 模型
[10 行，1 个文件]

### 任务 2: 向 User 添加密码哈希字段
[8 行，1 个文件]

### 任务 3: 创建密码哈希工具
[15 行，1 个文件]
```

## 计划文档结构

### 标题（必需）

每个计划必须以：

```markdown
# [功能名称] 实施计划

> **对于 Hermes:** 使用 subagent-driven-development 技能逐任务实施此计划。

**目标:** [一句话描述构建的内容]

**架构:** [2-3 句话关于方法]

**技术栈:** [关键技术/库]

---
```

### 任务结构

每个任务遵循此格式：

````markdown
### 任务 N: [描述性名称]

**目标:** 此任务完成的内容（一句话）

**文件:**
- 创建: `exact/path/to/new_file.py`
- 修改: `exact/path/to/existing.py:45-67`（如果已知行号）
- 测试: `tests/path/to/test_file.py`

**步骤 1: 编写失败的测试**

```python
def test_specific_behavior():
    result = function(input)
    assert result == expected
```

**步骤 2: 运行测试以验证失败**

运行: `pytest tests/path/test.py::test_specific_behavior -v`
预期: 失败 — "function not defined"

**步骤 3: 编写最小实施**

```python
def function(input):
    return expected
```

**步骤 4: 运行测试以验证通过**

运行: `pytest tests/path/test.py::test_specific_behavior -v`
预期: 通过

**步骤 5: 提交**

```bash
git add tests/path/test.py src/path/file.py
git commit -m "feat: 添加特定功能"
```
````

## 编写过程

### 步骤 1: 理解需求

阅读和理解：
- 功能需求
- 设计文档或用户描述
- 验收标准
- 约束条件

### 步骤 2: 探索代码库

使用 Hermes 工具理解项目：

```python
# 理解项目结构
search_files("*.py", target="files", path="src/")

# 查看类似功能
search_files("similar_pattern", path="src/", file_glob="*.py")

# 检查现有测试
search_files("*.py", target="files", path="tests/")

# 阅读关键文件
read_file("src/app.py")
```

### 步骤 3: 设计方法

决定：
- 架构模式
- 文件组织
- 需要的依赖
- 测试策略

### 步骤 4: 编写任务

按顺序创建任务：
1. 设置/基础设施
2. 核心功能（每个都用 TDD）
3. 边缘情况
4. 集成
5. 清理/文档

### 步骤 5: 添加完整细节

对于每个任务，包括：
- **确切的文件路径**（不是"配置文件"而是 `src/config/settings.py`）
- **完整的代码示例**（不是"添加验证"而是实际代码）
- **带有预期输出的确切命令**
- **证明任务有效的验证步骤**

### 步骤 6: 审查计划

检查：
- [ ] 任务是顺序且逻辑的
- [ ] 每个任务都是小任务（2-5 分钟）
- [ ] 文件路径确切
- [ ] 代码示例完整（可复制粘贴）
- [ ] 命令确切且带有预期输出
- [ ] 没有缺失的上下文
- [ ] 应用了 DRY、YAGNI、TDD 原则

### 步骤 7: 保存计划

```bash
mkdir -p docs/plans
# 将计划保存到 docs/plans/YYYY-MM-DD-feature-name.md
git add docs/plans/
git commit -m "docs: 添加 [功能] 的实施计划"
```

## 原则

### DRY（不要重复自己）

**糟糕:** 在 3 个地方复制粘贴验证
**良好:** 提取验证函数，在各处使用

### YAGNI（您不会需要它）

**糟糕:** 为未来需求添加"灵活性"
**良好:** 只实施现在需要的内容

```python
# 糟糕 — YAGNI 违规
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
        self.preferences = {}  # 还不需要！
        self.metadata = {}     # 还不需要！

# 良好 — YAGNI
class User:
    def __init__(self, name, email):
        self.name = name
        self.email = email
```

### TDD（测试驱动开发）

每个生成代码的任务都应包含完整的 TDD 循环：
1. 编写失败的测试
2. 运行以验证失败
3. 编写最小代码
4. 运行以验证通过

详细信息请参见 `test-driven-development` 技能。

### 频繁提交

每个任务后提交：
```bash
git add [files]
git commit -m "type: description"
```

## 常见错误

### 模糊任务

**糟糕:** "添加身份验证"
**良好:** "创建带 email 和 password_hash 字段的 User 模型"

### 不完整的代码

**糟糕:** "步骤 1: 添加验证函数"
**良好:** "步骤 1: 添加验证函数" 后跟完整的函数代码

### 缺少验证

**糟糕:** "步骤 3: 测试它是否工作"
**良好:** "步骤 3: 运行 `pytest tests/test_auth.py -v`，预期: 3 个通过"

### 缺少文件路径

**糟糕:** "创建模型文件"
**良好:** "创建: `src/models/user.py`"

## 执行移交

保存计划后，提供执行方法：

**"计划完成并保存。准备使用 subagent-driven-development 执行 — 我将为每个任务分派一个新的子代理，并进行两阶段审查（规范合规性然后代码质量）。是否继续？"**

执行时，使用 `subagent-driven-development` 技能：
- 每个任务有完整上下文的新 `delegate_task`
- 每个任务后进行规范合规性审查
- 规范通过后进行代码质量审查
- 仅当两个审查都批准时才继续

## 记住

```
小任务（每个 2-5 分钟）
确切的文件路径
完整的代码（可复制粘贴）
带有预期输出的确切命令
验证步骤
DRY, YAGNI, TDD
频繁提交
```

**好的计划使实施变得显而易见。**
