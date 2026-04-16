---
name: manim-video
description: "使用Manim社区版制作数学和技术动画的生产管道。创建3Blue1Brown风格的解释视频、算法可视化、公式推导、架构图和数据故事。当用户请求：动画解释、数学动画、概念可视化、算法演练、技术解释器、3Blue1Brown风格视频或任何具有几何/数学内容的程序化动画时使用。"
version: 1.0.0
---

# Manim视频生产管道

## 创意标准

这是教育性的电影。每一帧都在教学。每个动画都揭示结构。

**在编写任何代码之前**，阐明叙事弧。这纠正了什么误解？"啊哈时刻"是什么？什么视觉故事将观众从困惑带到理解？用户的提示是一个起点 — 用教学雄心来解释它。

**先几何后代数。** 先展示形状，再展示公式。视觉记忆比符号记忆编码更快。当观众在公式之前看到几何图案时，公式会感觉是应得的。

**首次渲染卓越是不可谈判的。** 输出必须在视觉上清晰且美学上连贯，无需修订轮次。如果某些东西看起来杂乱、时间安排不当或像"AI生成的幻灯片"，那就是错的。

**不透明度分层引导注意力。** 永远不要以全亮度显示所有内容。主要元素为1.0，上下文元素为0.4，结构元素（轴、网格）为0.15。大脑分层处理视觉显著性。

**呼吸空间。** 每个动画之后都需要`self.wait()`。观众需要时间来吸收刚刚出现的内容。永远不要从一个动画匆忙到下一个动画。关键揭示后2秒的暂停永远不会被浪费。

**连贯的视觉语言。** 所有场景共享调色板、一致的排版大小、匹配的动画速度。一个技术上正确但每个场景使用随机不同颜色的视频是美学失败。

## 先决条件

运行`scripts/setup.sh`以验证所有依赖项。需要：Python 3.10+、Manim社区版v0.20+（`pip install manim`）、LaTeX（Linux上的`texlive-full`，macOS上的`mactex`）和ffmpeg。参考文档针对Manim CE v0.20.1进行了测试。

## 模式

| 模式 | 输入 | 输出 | 参考 |
|------|-------|--------|-----------|
| **概念解释器** | 主题/概念 | 具有几何直觉的动画解释 | `references/scene-planning.md` |
| **公式推导** | 数学表达式 | 分步动画证明 | `references/equations.md` |
| **算法可视化** | 算法描述 | 带数据结构的分步执行 | `references/graphs-and-data.md` |
| **数据故事** | 数据/指标 | 动画图表、比较、计数器 | `references/graphs-and-data.md` |
| **架构图** | 系统描述 | 带连接的组件构建 | `references/mobjects.md` |
| **论文解释器** | 研究论文 | 关键发现和方法动画化 | `references/scene-planning.md` |
| **3D可视化** | 3D概念 | 旋转表面、参数曲线、空间几何 | `references/camera-and-3d.md` |

## 技术栈

每个项目一个Python脚本。无需浏览器，无需Node.js，无需GPU。

| 层 | 工具 | 用途 |
|-------|------|---------|
| 核心 | Manim社区版 | 场景渲染、动画引擎 |
| 数学 | LaTeX（texlive/MiKTeX） | 通过`MathTex`进行公式渲染 |
| 视频I/O | ffmpeg | 场景拼接、格式转换、音频混合 |
| TTS | ElevenLabs / Qwen3-TTS（可选） | 旁白画外音 |

## 管道

```
计划 --> 代码 --> 渲染 --> 拼接 --> 音频（可选） --> 审查
```

1. **计划** — 编写`plan.md`，包含叙事弧、场景列表、视觉元素、调色板、画外音脚本
2. **代码** — 编写`script.py`，每个场景一个类，每个都可独立渲染
3. **渲染** — `manim -ql script.py Scene1 Scene2 ...`用于草稿，`-qh`用于生产
4. **拼接** — 使用ffmpeg将场景剪辑连接到`final.mp4`
5. **音频**（可选）— 通过ffmpeg添加画外音和/或背景音乐。查看`references/rendering.md`
6. **审查** — 渲染预览静止图像，对照计划验证，调整

## 项目结构

```
project-name/
  plan.md                # 叙事弧、场景分解
  script.py              # 所有场景在一个文件中
  concat.txt             # ffmpeg场景列表
  final.mp4              # 拼接输出
  media/                 # Manim自动生成
    videos/script/480p15/
```

## 创意方向

### 调色板

| 调色板 | 背景 | 主要 | 次要 | 强调 | 用例 |
|---------|-----------|---------|-----------|--------|----------|
| **经典3B1B** | `#1C1C1C` | `#58C4DD`（蓝色）| `#83C167`（绿色）| `#FFFF00`（黄色）| 一般数学/CS |
| **温暖学术** | `#2D2B55` | `#FF6B6B` | `#FFD93D` | `#6BCB77` | 平易近人 |
| **霓虹科技** | `#0A0A0A` | `#00F5FF` | `#FF00FF` | `#39FF14` | 系统、架构 |
| **单色** | `#1A1A2E` | `#EAEAEA` | `#888888` | `#FFFFFF` | 极简主义 |

### 动画速度

| 上下文 | run_time | 之后的self.wait() |
|---------|----------|-------------------|
| 标题/介绍出现 | 1.5s | 1.0s |
| 关键公式揭示 | 2.0s | 2.0s |
| 变换/变形 | 1.5s | 1.5s |
| 支持标签 | 0.8s | 0.5s |
| FadeOut清理 | 0.5s | 0.3s |
| "啊哈时刻"揭示 | 2.5s | 3.0s |

### 排版比例

| 角色 | 字体大小 | 用法 |
|------|-----------|-------|
| 标题 | 48 | 场景标题、开场文本 |
| 副标题 | 36 | 场景内的章节标题 |
| 正文 | 30 | 解释性文本 |
| 标签 | 24 | 注释、轴标签 |
| 说明文字 | 20 | 字幕、小号字体 |

### 字体

**对所有文本使用等宽字体。** Manim的Pango渲染器在所有大小下都会与比例字体产生断字间距。查看`references/visual-design.md`获取完整建议。

```python
MONO = "Menlo"  # 在文件顶部定义一次

Text("Fourier Series", font_size=48, font=MONO, weight=BOLD)  # 标题
Text("n=1: sin(x)", font_size=20, font=MONO)                  # 标签
MathTex(r"\nabla L")                                            # 数学（使用LaTeX）
```

可读性的最小`font_size=18`。

### 每个场景的变化

永远不要对所有场景使用相同的配置。对于每个场景：
- **从调色板中选择不同的主色**
- **不同的布局** — 不要总是将所有内容居中
- **不同的动画进入** — 在Write、FadeIn、GrowFromCenter、Create之间变化
- **不同的视觉权重** — 一些场景密集，其他场景稀疏

## 工作流程

### 步骤1：计划（plan.md）

在任何代码之前，编写`plan.md`。查看`references/scene-planning.md`获取全面模板。

### 步骤2：代码（script.py）

每个场景一个类。每个场景都可独立渲染。

```python
from manim import *

BG = "#1C1C1C"
PRIMARY = "#58C4DD"
SECONDARY = "#83C167"
ACCENT = "#FFFF00"
MONO = "Menlo"

class Scene1_Introduction(Scene):
    def construct(self):
        self.camera.background_color = BG
        title = Text("为什么这有效？", font_size=48, color=PRIMARY, weight=BOLD, font=MONO)
        self.add_subcaption("为什么这有效？", duration=2)
        self.play(Write(title), run_time=1.5)
        self.wait(1.0)
        self.play(FadeOut(title), run_time=0.5)
```

关键模式：
- **每个动画的字幕**：`self.add_subcaption("text", duration=N)`或`self.play()`上的`subcaption="text"`
- **文件顶部的共享颜色常量**用于跨场景一致性
- **在每个场景中设置`self.camera.background_color`**
- **干净的退出** — 在场景结束时FadeOut所有mobjects：`self.play(FadeOut(Group(*self.mobjects)))`

### 步骤3：渲染

```bash
manim -ql script.py Scene1_Introduction Scene2_CoreConcept  # 草稿
manim -qh script.py Scene1_Introduction Scene2_CoreConcept  # 生产
```

### 步骤4：拼接

```bash
cat > concat.txt << 'EOF'
file 'media/videos/script/480p15/Scene1_Introduction.mp4'
file 'media/videos/script/480p15/Scene2_CoreConcept.mp4'
EOF
ffmpeg -y -f concat -safe 0 -i concat.txt -c copy final.mp4
```

### 步骤5：审查

```bash
manim -ql --format=png -s script.py Scene2_CoreConcept  # 预览静止图像
```

## 关键实现说明

### LaTeX的原始字符串
```python
# 错误：MathTex("\frac{1}{2}")
# 正确：
MathTex(r"\frac{1}{2}")
```

### 边缘文本的buff >= 0.5
```python
label.to_edge(DOWN, buff=0.5)  # 永远不要 < 0.5
```

### 替换文本前先FadeOut
```python
self.play(ReplacementTransform(note1, note2))  # 不是在顶部Write(note2)
```

### 永远不要动画化未添加的Mobjects
```python
self.play(Create(circle))  # 必须先添加
self.play(circle.animate.set_color(RED))  # 然后动画化
```

## 性能目标

| 质量 | 分辨率 | FPS | 速度 |
|---------|-----------|-----|-------|
| `-ql`（草稿）| 854x480 | 15 | 5-15s/场景 |
| `-qm`（中等）| 1280x720 | 30 | 15-60s/场景 |
| `-qh`（生产）| 1920x1080 | 60 | 30-120s/场景 |

始终在`-ql`下迭代。仅为最终输出渲染`-qh`。

## 参考

| 文件 | 内容 |
|------|----------|
| `references/animations.md` | 核心动画、速率函数、合成、`.animate`语法、计时模式 |
| `references/mobjects.md` | 文本、形状、VGroup/Group、定位、样式、自定义mobjects |
| `references/visual-design.md` | 12条设计原则、不透明度分层、布局模板、调色板 |
| `references/equations.md` | Manim中的LaTeX、TransformMatchingTex、推导模式 |
| `references/graphs-and-data.md` | 轴、绘图、BarChart、动画数据、算法可视化 |
| `references/camera-and-3d.md` | MovingCameraScene、ThreeDScene、3D表面、相机控制 |
| `references/scene-planning.md` | 叙事弧、布局模板、场景过渡、计划模板 |
| `references/rendering.md` | CLI参考、质量预设、ffmpeg、画外音工作流、GIF导出 |
| `references/troubleshooting.md` | LaTeX错误、动画错误、常见错误、调试 |
| `references/animation-design-thinking.md` | 何时动画化与显示静态、分解、节奏、旁白同步 |
| `references/updaters-and-trackers.md` | ValueTracker、add_updater、always_redraw、基于时间的更新器、模式 |
| `references/paper-explainer.md` | 将研究论文转换为动画 — 工作流、模板、领域模式 |
| `references/decorations.md` | SurroundingRectangle、Brace、箭头、DashedLine、Angle、注释生命周期 |
| `references/production-quality.md` | 代码前、渲染前、渲染后检查清单、空间布局、颜色、节奏 |

---

## 创意分歧（仅在用户请求实验性/创意/独特输出时使用）

如果用户要求创意、实验性或非常规的解释方法，在设计动画之前选择一个策略并推理其步骤。

- **SCAMPER** — 当用户想要对标准解释进行全新诠释时
- **假设逆转** — 当用户想要挑战通常教授某事物的方式时

### SCAMPER变换
采用标准的数学/技术可视化并变换它：
- **替代**：替换标准的视觉隐喻（数轴 → 蜿蜒路径，矩阵 → 城市网格）
- **组合**：合并两种解释方法（同时代数 + 几何）
- **逆转**：向后推导 — 从结果开始，解构为公理
- **修改**：夸大一个参数以显示为什么它重要（10倍学习率，1000倍样本大小）
- **消除**：删除所有符号 — 纯粹通过动画和空间关系解释

### 假设逆转
1. 列出关于该主题如何可视化的"标准"内容（从左到右、2D、离散步骤、正式符号）
2. 选择最基本的假设
3. 逆转它（从右到左推导、2D概念的3D嵌入、连续变形而不是步骤、零符号）
4. 探索逆转揭示了标准方法隐藏的内容
