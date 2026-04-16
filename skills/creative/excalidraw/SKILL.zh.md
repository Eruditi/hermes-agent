---
name: excalidraw
description: 使用Excalidraw JSON格式创建手绘风格的图表。生成.excalidraw文件用于架构图、流程图、序列图、概念图等。文件可以在excalidraw.com打开或上传以获取可共享的链接。
version: 1.0.0
author: Hermes Agent
license: MIT
dependencies: []
metadata:
  hermes:
    tags: [Excalidraw, 图表, 流程图, 架构, 可视化, JSON]
    related_skills: []

---

# Excalidraw图表技能

通过编写标准Excalidraw元素JSON并保存为`.excalidraw`文件来创建图表。这些文件可以拖放到 [excalidraw.com](https://excalidraw.com) 进行查看和编辑。无需账户，无需API密钥，无需渲染库 — 只需要JSON。

## 工作流程

1. **加载这个技能**（你已经做了）
2. **编写元素JSON** — 一个Excalidraw元素对象数组
3. **保存文件** 使用`write_file`创建一个`.excalidraw`文件
4. **可选上传** 使用`scripts/upload.py`通过`terminal`获取可共享链接

### 保存图表

将你的元素数组包装在标准的`.excalidraw`信封中，并使用`write_file`保存：

```json
{
  "type": "excalidraw",
  "version": 2,
  "source": "hermes-agent",
  "elements": [ ...你的元素数组在这里... ],
  "appState": {
    "viewBackgroundColor": "#ffffff"
  }
}
```

保存到任何路径，例如 `~/diagrams/my_diagram.excalidraw`。

### 上传获取可共享链接

通过终端运行上传脚本（位于此技能的`scripts/`目录中）：

```bash
python skills/diagramming/excalidraw/scripts/upload.py ~/diagrams/my_diagram.excalidraw
```

这会上传到excalidraw.com（无需账户）并打印可共享的URL。需要`cryptography` pip包（`pip install cryptography`）。

---

## 元素格式参考

### 必需字段（所有元素）
`type`、`id`（唯一字符串）、`x`、`y`、`width`、`height`

### 默认值（跳过这些 — 它们会自动应用）
- `strokeColor`: `"#1e1e1e"`
- `backgroundColor`: `"transparent"`
- `fillStyle`: `"solid"`
- `strokeWidth`: `2`
- `roughness`: `1`（手绘外观）
- `opacity`: `100`

画布背景是白色的。

### 元素类型

**矩形**：
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 100 }
```
- `roundness: { "type": 3 }` 用于圆角
- `backgroundColor: "#a5d8ff"`、`fillStyle: "solid"` 用于填充

**椭圆**：
```json
{ "type": "ellipse", "id": "e1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**菱形**：
```json
{ "type": "diamond", "id": "d1", "x": 100, "y": 100, "width": 150, "height": 150 }
```

**带标签的形状（容器绑定）** — 创建一个绑定到形状的文本元素：

> **警告：** 不要在形状上使用`"label": { "text": "..." }`。这不是一个有效的Excalidraw属性，会被默默忽略，产生空白形状。你必须使用下面的容器绑定方法。

形状需要`boundElements`列出文本，文本需要`containerId`指回：
```json
{ "type": "rectangle", "id": "r1", "x": 100, "y": 100, "width": 200, "height": 80,
  "roundness": { "type": 3 }, "backgroundColor": "#a5d8ff", "fillStyle": "solid",
  "boundElements": [{ "id": "t_r1", "type": "text" }] },
{ "type": "text", "id": "t_r1", "x": 105, "y": 110, "width": 190, "height": 25,
  "text": "Hello", "fontSize": 20, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "r1", "originalText": "Hello", "autoResize": true }
```
- 适用于矩形、椭圆、菱形
- 当设置`containerId`时，文本会被Excalidraw自动居中
- 文本的`x`/`y`/`width`/`height`是近似的 — Excalidraw在加载时会重新计算它们
- `originalText`应该与`text`匹配
- 始终包含`fontFamily: 1`（Virgil/手绘字体）

**带标签的箭头** — 相同的容器绑定方法：
```json
{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow",
  "boundElements": [{ "id": "t_a1", "type": "text" }] },
{ "type": "text", "id": "t_a1", "x": 370, "y": 130, "width": 60, "height": 20,
  "text": "connects", "fontSize": 16, "fontFamily": 1, "strokeColor": "#1e1e1e",
  "textAlign": "center", "verticalAlign": "middle",
  "containerId": "a1", "originalText": "connects", "autoResize": true }
```

**独立文本**（仅标题和注释 — 无容器）：
```json
{ "type": "text", "id": "t1", "x": 150, "y": 138, "text": "Hello", "fontSize": 20,
  "fontFamily": 1, "strokeColor": "#1e1e1e", "originalText": "Hello", "autoResize": true }
```
- `x`是左边缘。要在位置`cx`居中：`x = cx - (text.length * fontSize * 0.5) / 2`
- 不要依赖`textAlign`或`width`进行定位

**箭头**：
```json
{ "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 200, "height": 0,
  "points": [[0,0],[200,0]], "endArrowhead": "arrow" }
```
- `points`：从元素`x`、`y`的`[dx, dy]`偏移
- `endArrowhead`：`null` | `"arrow"` | `"bar"` | `"dot"` | `"triangle"`
- `strokeStyle`：`"solid"`（默认）| `"dashed"` | `"dotted"`

### 箭头绑定（将箭头连接到形状）

```json
{
  "type": "arrow", "id": "a1", "x": 300, "y": 150, "width": 150, "height": 0,
  "points": [[0,0],[150,0]], "endArrowhead": "arrow",
  "startBinding": { "elementId": "r1", "fixedPoint": [1, 0.5] },
  "endBinding": { "elementId": "r2", "fixedPoint": [0, 0.5] }
}
```

`fixedPoint`坐标：`top=[0.5,0]`、`bottom=[0.5,1]`、`left=[0,0.5]`、`right=[1,0.5]`

### 绘制顺序（z顺序）
- 数组顺序 = z顺序（第一个 = 后面，最后一个 = 前面）
- 渐进式发出：背景区域 → 形状 → 其绑定文本 → 其箭头 → 下一个形状
- 不好：所有矩形，然后所有文本，然后所有箭头
- 好：bg_zone → shape1 → text_for_shape1 → arrow1 → arrow_label_text → shape2 → text_for_shape2 → ...
- 始终将绑定文本元素紧跟在其容器形状之后放置

### 大小指南

**字体大小：**
- 正文、标签、描述的最小`fontSize`：**16**
- 标题和副标题的最小`fontSize`：**20**
- 仅次要注释的最小`fontSize`：**14**（谨慎使用）
- 永远不要使用低于14的`fontSize`

**元素大小：**
- 带标签的矩形/椭圆的最小形状大小：120x60
- 元素之间至少留有20-30px的间隙
- 更喜欢更少、更大的元素，而不是许多小元素

### 调色板

查看 `references/colors.md` 获取完整的颜色表。快速参考：

| 用途 | 填充颜色 | 十六进制 |
|-----|-----------|-----|
| 主要 / 输入 | 浅蓝色 | `#a5d8ff` |
| 成功 / 输出 | 浅绿色 | `#b2f2bb` |
| 警告 / 外部 | 浅橙色 | `#ffd8a8` |
| 处理 / 特殊 | 浅紫色 | `#d0bfff` |
| 错误 / 关键 | 浅红色 | `#ffc9c9` |
| 注释 / 决策 | 浅黄色 | `#fff3bf` |
| 存储 / 数据 | 浅青色 | `#c3fae8` |

### 提示
- 在整个图表中一致使用调色板
- **文本对比度至关重要** — 永远不要在白色背景上使用浅灰色。白色上的最小文本颜色：`#757575`
- 不要在文本中使用表情符号 — 它们在Excalidraw的字体中不渲染
- 对于深色模式图表，查看 `references/dark-mode.md`
- 对于更大的示例，查看 `references/examples.md`
