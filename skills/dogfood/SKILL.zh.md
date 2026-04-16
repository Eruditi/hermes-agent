---
name: dogfood
description: Web应用程序的系统化探索性QA测试 — 查找bug，捕获证据，并生成结构化报告
version: 1.0.0
metadata:
  hermes:
    tags: [qa, testing, browser, web, dogfood, 测试, 浏览器]
    related_skills: []
---

# Dogfood：系统化Web应用QA测试

## 概述

此技能指导您使用浏览器工具集对Web应用程序进行系统化探索性QA测试。您将导航应用程序、与元素交互、捕获问题证据，并生成结构化的bug报告。

## 先决条件

- 浏览器工具集必须可用（`browser_navigate`、`browser_snapshot`、`browser_click`、`browser_type`、`browser_vision`、`browser_console`、`browser_scroll`、`browser_back`、`browser_press`）
- 用户提供的目标URL和测试范围

## 输入

用户提供：
1. **目标URL** — 测试的入口点
2. **范围** — 要关注哪些区域/功能（或"完整站点"进行全面测试）
3. **输出目录**（可选） — 保存截图和报告的位置（默认：`./dogfood-output`）

## 工作流程

遵循此5阶段系统化工作流程：

### 阶段1：计划

1. 创建输出目录结构：
   ```
   {output_dir}/
   ├── screenshots/       # 证据截图
   └── report.md          # 最终报告（在阶段5生成）
   ```
2. 根据用户输入确定测试范围。
3. 通过规划要测试的页面和功能来构建粗略的站点地图：
   - 着陆/主页
   - 导航链接（页眉、页脚、侧边栏）
   - 关键用户流程（注册、登录、搜索、结账等）
   - 表单和交互元素
   - 边界情况（空状态、错误页面、404）

### 阶段2：探索

对于计划中的每个页面或功能：

1. **导航**到页面：
   ```
   browser_navigate(url="https://example.com/page")
   ```

2. **获取快照**以了解DOM结构：
   ```
   browser_snapshot()
   ```

3. **检查控制台**是否有JavaScript错误：
   ```
   browser_console(clear=true)
   ```
   在每次导航后和每次重要交互后执行此操作。静默JS错误是高价值发现。

4. **获取带注释的截图**以视觉评估页面并识别交互元素：
   ```
   browser_vision(question="Describe the page layout, identify any visual issues, broken elements, or accessibility concerns", annotate=true)
   ```
   `annotate=true`标志在交互元素上叠加编号的`[N]`标签。每个`[N]`映射到ref`@eN`，用于后续浏览器命令。

5. **系统测试交互元素**：
   - 点击按钮和链接：`browser_click(ref="@eN")`
   - 填写表单：`browser_type(ref="@eN", text="test input")`
   - 测试键盘导航：`browser_press(key="Tab")`，`browser_press(key="Enter")`
   - 滚动内容：`browser_scroll(direction="down")`
   - 使用无效输入测试表单验证
   - 测试空提交

6. **每次交互后**，检查：
   - 控制台错误：`browser_console()`
   - 视觉更改：`browser_vision(question="What changed after the interaction?")`
   - 预期与实际行为

### 阶段3：收集证据

对于发现的每个问题：

1. **获取显示问题的截图**：
   ```
   browser_vision(question="Capture and describe the issue visible on this page", annotate=false)
   ```
   保存响应中的`screenshot_path` — 您将在报告中引用它。

2. **记录详细信息**：
   - 问题发生的URL
   - 重现步骤
   - 预期行为
   - 实际行为
   - 控制台错误（如果有）
   - 截图路径

3. **使用问题分类法对问题进行分类**（参见`references/issue-taxonomy.md`）：
   - 严重程度：严重 / 高 / 中 / 低
   - 类别：功能 / 视觉 / 可访问性 / 控制台 / UX / 内容

### 阶段4：分类

1. 审查所有收集的问题。
2. 去重 — 合并在不同地方表现的相同bug的问题。
3. 为每个问题分配最终严重程度和类别。
4. 按严重程度排序（先严重，然后高、中、低）。
5. 为执行摘要按严重程度和类别计算问题数。

### 阶段5：报告

使用`templates/dogfood-report-template.md`中的模板生成最终报告。

报告必须包括：
1. **执行摘要**，包含总问题数、按严重程度的细分和测试范围
2. **每个问题的部分**，包含：
   - 问题编号和标题
   - 严重程度和类别徽章
   - 观察到的URL
   - 问题描述
   - 重现步骤
   - 预期与实际行为
   - 截图引用（使用`MEDIA:<screenshot_path>`进行内联图像）
   - 相关的控制台错误
3. **所有问题的摘要表**
4. **测试说明** — 测试了什么，未测试什么，任何阻塞因素

将报告保存到`{output_dir}/report.md`。

## 工具参考

| 工具 | 用途 |
|------|------|
| `browser_navigate` | 转到URL |
| `browser_snapshot` | 获取DOM文本快照（可访问性树） |
| `browser_click` | 通过ref（`@eN`）或文本点击元素 |
| `browser_type` | 输入到输入字段 |
| `browser_scroll` | 在页面上上下滚动 |
| `browser_back` | 在浏览器历史中返回 |
| `browser_press` | 按下键盘键 |
| `browser_vision` | 截图 + AI分析；对元素标签使用`annotate=true` |
| `browser_console` | 获取JS控制台输出和错误 |

## 提示

- **导航后和重要交互后始终检查`browser_console()`**。静默JS错误是最有价值的发现之一。
- 当您需要推理交互元素位置或快照refs不清楚时，**对`browser_vision`使用`annotate=true`**。
- **使用有效和无效输入测试** — 表单验证bug很常见。
- **滚动长页面** — 折叠下方的内容可能有渲染问题。
- **测试导航流程** — 从头到尾点击多步骤流程。
- **通过注意截图中可见的任何布局问题来检查响应行为**。
- **不要忘记边界情况**：空状态、很长的文本、特殊字符、快速点击。
- 向用户报告截图时，包含`MEDIA:<screenshot_path>`，以便他们可以内联看到证据。