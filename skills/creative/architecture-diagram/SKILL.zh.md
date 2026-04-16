---
name: architecture-diagram
description: 生成专业的深色主题系统架构图作为独立的HTML/SVG文件。自包含的输出，没有外部依赖项。基于Cocoon AI的architecture-diagram-generator（MIT）。
version: 1.0.0
author: Cocoon AI (hello@cocoon-ai.com), ported by Hermes Agent
license: MIT
dependencies: []
metadata:
  hermes:
    tags: [架构, 图表, SVG, HTML, 可视化, 基础设施, 云]
    related_skills: [excalidraw]
---

# 架构图技能

生成专业的深色主题技术架构图作为独立的HTML文件，带有内联SVG图形。没有外部工具，没有API密钥，没有渲染库 — 只需编写HTML文件并在浏览器中打开它。

基于[Cocoon AI的architecture-diagram-generator](https://github.com/Cocoon-AI/architecture-diagram-generator)（MIT）。

## 工作流程

1. 用户描述他们的系统架构（组件、连接、技术）
2. 按照下面的设计系统生成HTML文件
3. 使用`write_file`保存到`.html`文件（例如`~/architecture-diagram.html`）
4. 用户在任何浏览器中打开 — 离线工作，没有依赖项

### 输出位置

将图表保存到用户指定的路径，或默认为当前工作目录：
```
./[project-name]-architecture.html
```

### 预览

保存后，建议用户打开它：
```bash
# macOS
open ./my-architecture.html
# Linux
xdg-open ./my-architecture.html
```

## 设计系统和视觉语言

### 调色板（语义映射）

使用特定的`rgba`填充和十六进制描边来分类组件：

| 组件类型 | 填充（rgba） | 描边（十六进制） |
| :--- | :--- | :--- |
| **前端** | `rgba(8, 51, 68, 0.4)` | `#22d3ee`（青色-400） |
| **后端** | `rgba(6, 78, 59, 0.4)` | `#34d399`（翡翠-400） |
| **数据库** | `rgba(76, 29, 149, 0.4)` | `#a78bfa`（紫罗兰-400） |
| **AWS/云** | `rgba(120, 53, 15, 0.3)` | `#fbbf24`（琥珀-400） |
| **安全** | `rgba(136, 19, 55, 0.4)` | `#fb7185`（玫瑰-400） |
| **消息总线** | `rgba(251, 146, 60, 0.3)` | `#fb923c`（橙色-400） |
| **外部** | `rgba(30, 41, 59, 0.5)` | `#94a3b8`（石板-400） |

### 排版和背景
- **字体：** JetBrains Mono（等宽），从Google Fonts加载
- **大小：** 12px（名称），9px（子标签），8px（注释），7px（微小标签）
- **背景：** 石板-950（`#020617`），带有微妙的40px网格图案

```svg
<!-- 背景网格图案 -->
<pattern id="grid" width="40" height="40" patternUnits="userSpaceOnUse">
  <path d="M 40 0 L 0 0 0 40" fill="none" stroke="#1e293b" stroke-width="0.5"/>
</pattern>
```

## 技术实现细节

### 组件渲染
组件是圆角矩形（`rx="6"`），带有1.5px描边。为了防止箭头透过半透明填充显示，请使用**双矩形遮罩技术**：
1. 绘制一个不透明的背景矩形（`#0f172a`）
2. 在顶部绘制半透明的样式化矩形

### 连接规则
- **Z顺序：** 在SVG中*早期*绘制箭头（在网格之后），以便它们渲染在组件框后面
- **箭头：** 通过SVG标记定义
- **安全流：** 使用玫瑰色（`#fb7185`）的虚线
- **边界：**
  - *安全组：* 虚线（`4,4`），玫瑰色
  - *区域：* 大虚线（`8,4`），琥珀色，`rx="12"`

### 间距和布局逻辑
- **标准高度：** 60px（服务）；80-120px（大型组件）
- **垂直间隙：** 组件之间最小40px
- **消息总线：** 必须放置在服务之间的*间隙中*，不要重叠它们
- **图例位置：** **关键。** 必须放置在所有边界框之外。计算所有边界的最低Y坐标，并将图例放置在其下方至少20px处。

## 文档结构

生成的HTML文件遵循四部分布局：
1. **标题：** 带有脉冲点指示器和副标题的标题
2. **主SVG：** 包含在圆角边框卡片中的图表
3. **摘要卡：** 图表下方的三张卡网格，用于高级详细信息
4. **页脚：** 最小元数据

### 信息卡模式
```html
<div class="card">
  <div class="card-header">
    <div class="card-dot cyan"></div>
    <h3>Title</h3>
  </div>
  <ul>
    <li>• Item one</li>
    <li>• Item two</li>
  </ul>
</div>
```

## 输出要求
- **单个文件：** 一个自包含的`.html`文件
- **没有外部依赖项：** 所有CSS和SVG必须内联（除了Google Fonts）
- **没有JavaScript：** 使用纯CSS进行任何动画（如脉冲点）
- **兼容性：** 必须在任何现代Web浏览器中正确渲染

## 模板参考

加载完整的HTML模板以获取确切的结构、CSS和SVG组件示例：

```
skill_view(name="architecture-diagram", file_path="templates/template.html")
```

模板包含每种组件类型（前端、后端、数据库、云、安全）、箭头样式（标准、虚线、弯曲）、安全组、区域边界和图例的工作示例 — 在生成图表时将其用作结构参考。
