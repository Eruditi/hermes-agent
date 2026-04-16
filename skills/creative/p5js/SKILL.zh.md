---
name: p5js
description: "使用p5.js制作交互式和生成式视觉艺术的生产管道。创建基于浏览器的草图、生成式艺术、数据可视化、交互式体验、3D场景、音频反应式视觉效果和动态图形 — 导出为HTML、PNG、GIF、MP4或SVG。涵盖：2D/3D渲染、噪声和粒子系统、流场、着色器（GLSL）、像素操作、动态排版、WebGL场景、音频分析、鼠标/键盘交互和无头高分辨率导出。当用户请求：p5.js草图、创意编码、生成式艺术、交互式可视化、画布动画、基于浏览器的视觉艺术、数据可视化、着色器效果或任何p5.js项目时使用。"
version: 1.0.0
metadata:
  hermes:
    tags: [创意编码, 生成式艺术, p5js, 画布, 交互式, 可视化, webgl, 着色器, 动画]
    related_skills: [ascii-video, manim-video, excalidraw]
---

# p5.js生产管道

## 创意标准

这是在浏览器中渲染的视觉艺术。画布是媒介；算法是画笔。

**在编写任何代码之前**，阐明创意概念。这件作品传达了什么？是什么让观众停止滚动？是什么将这与代码教程示例区分开来？用户的提示是一个起点 — 用创意雄心来解释它。

**首次渲染卓越是不可谈判的。** 输出必须在首次加载时在视觉上引人注目。如果它看起来像一个p5.js教程练习、一个默认配置或"AI生成的创意编码"，那就是错的。在发布之前重新思考。

**超越参考词汇。** 参考中的噪声函数、粒子系统、调色板和着色器效果是一个起始词汇。对于每个项目，组合、分层和发明。目录是一个调色板 — 你写这幅画。

**主动创意。** 如果用户要求"一个粒子系统"，交付一个具有涌现群体行为、拖尾幽灵回声、调色板偏移深度雾和一个呼吸的背景噪声场的粒子系统。至少包含一个用户没有要求但会欣赏的视觉细节。

**密集、分层、深思熟虑。** 每一帧都应该奖励观看。永远不要平坦的白色背景。始终构图层次。始终有意的颜色。始终只有在仔细检查时才会出现的微观细节。

**连贯的美学胜过功能数量。** 所有元素必须服务于统一的视觉语言 — 共享色温、一致的描边粗细词汇、和谐的运动速度。一个具有十个不相关效果的草图比一个具有三个属于一起的效果的草图更差。

## 模式

| 模式 | 输入 | 输出 | 参考 |
|------|-------|--------|-----------|
| **生成式艺术** | 种子 / 参数 | 程序化视觉构图（静止或动画）| `references/visual-effects.md` |
| **数据可视化** | 数据集 / API | 交互式图表、图形、自定义数据显示 | `references/interaction.md` |
| **交互式体验** | 无（用户驱动）| 鼠标/键盘/触摸驱动的草图 | `references/interaction.md` |
| **动画 / 动态图形** | 时间线 / 故事板 | 定时序列、动态排版、过渡 | `references/animation.md` |
| **3D场景** | 概念描述 | WebGL几何、照明、相机、材质 | `references/webgl-and-3d.md` |
| **图像处理** | 图像文件 | 像素操作、滤镜、马赛克、点彩画 | `references/visual-effects.md` § 像素操作 |
| **音频反应式** | 音频文件 / 麦克风 | 声音驱动的生成式视觉效果 | `references/interaction.md` § 音频输入 |

## 技术栈

每个项目一个自包含的HTML文件。无需构建步骤。

| 层 | 工具 | 用途 |
|-------|------|---------|
| 核心 | p5.js 1.11.3（CDN）| 画布渲染、数学、变换、事件处理 |
| 3D | p5.js WebGL模式 | 3D几何、相机、照明、GLSL着色器 |
| 音频 | p5.sound.js（CDN）| FFT分析、振幅、麦克风输入、振荡器 |
| 导出 | 内置`saveCanvas()` / `saveGif()` / `saveFrames()` | PNG、GIF、帧序列输出 |
| 捕获 | CCapture.js（可选）| 确定性帧率视频捕获（WebM、GIF）|
| 无头 | Puppeteer + Node.js（可选）| 自动化高分辨率渲染，通过ffmpeg生成MP4 |
| SVG | p5.js-svg 1.6.0（可选）| 打印用矢量输出 — 需要p5.js 1.x |
| 自然媒体 | p5.brush（可选）| 水彩、炭笔、钢笔 — 需要p5.js 2.x + WEBGL |
| 纹理 | p5.grain（可选）| 胶片颗粒、纹理叠加 |
| 字体 | Google Fonts / `loadFont()` | 通过OTF/TTF/WOFF2的自定义排版 |

### 版本说明

**p5.js 1.x**（1.11.3）是默认 — 稳定、文档完善、最广泛的库兼容性。除非项目需要2.x功能，否则使用此版本。

**p5.js 2.x**（2.2+）添加：`async setup()`替换`preload()`、OKLCH/OKLAB颜色模式、`splineVertex()`、着色器`.modify()` API、可变字体、`textToContours()`、指针事件。p5.brush需要。查看`references/core-api.md` § p5.js 2.0。

## 管道

每个项目都遵循相同的6阶段路径：

```
概念 --> 设计 --> 代码 --> 预览 --> 导出 --> 验证
```

1. **概念** — 阐明创意愿景：心情、颜色世界、运动词汇、是什么让这独特
2. **设计** — 选择模式、画布大小、交互模型、颜色系统、导出格式。将概念映射到技术决策
3. **代码** — 编写单个HTML文件，内联p5.js。结构：全局变量 → `preload()` → `setup()` → `draw()` → 辅助函数 → 类 → 事件处理程序
4. **预览** — 在浏览器中打开，验证视觉质量。在目标分辨率下测试。检查性能
5. **导出** — 捕获输出：PNG用`saveCanvas()`，GIF用`saveGif()`，MP4用`saveFrames()` + ffmpeg，无头批处理用Puppeteer
6. **验证** — 输出是否与概念匹配？在预期显示大小下是否视觉引人注目？你会装裱它吗？

## 创意方向

### 美学维度

| 维度 | 选项 | 参考 |
|-----------|---------|-----------|
| **颜色系统** | HSB/HSL、RGB、命名调色板、程序化和谐、渐变插值 | `references/color-systems.md` |
| **噪声词汇** | Perlin噪声、单纯形、分形（八度）、域扭曲、卷曲噪声 | `references/visual-effects.md` § 噪声 |
| **粒子系统** | 基于物理、群体、拖尾绘制、吸引子驱动、流场跟随 | `references/visual-effects.md` § 粒子 |
| **形状语言** | 几何基元、自定义顶点、贝塞尔曲线、SVG路径 | `references/shapes-and-geometry.md` |
| **运动风格** | 缓动、基于弹簧、噪声驱动、物理模拟、lerped、步进 | `references/animation.md` |
| **排版** | 系统字体、加载的OTF、`textToPoints()`粒子文本、动态 | `references/typography.md` |
| **着色器效果** | GLSL片段/顶点、滤镜着色器、后处理、反馈循环 | `references/webgl-and-3d.md` § 着色器 |
| **构图** | 网格、径向、黄金比例、三分法则、有机散布、平铺 | `references/core-api.md` § 构图 |
| **交互模型** | 鼠标跟随、点击生成、拖动、键盘状态、滚动驱动、麦克风输入 | `references/interaction.md` |
| **混合模式** | `BLEND`、`ADD`、`MULTIPLY`、`SCREEN`、`DIFFERENCE`、`EXCLUSION`、`OVERLAY` | `references/color-systems.md` § 混合模式 |
| **分层** | `createGraphics()`离屏缓冲区、alpha合成、遮罩 | `references/core-api.md` § 离屏缓冲区 |
| **纹理** | Perlin表面、点画、阴影线、半色调、像素排序 | `references/visual-effects.md` § 纹理生成 |

### 每个项目的变化规则

永远不要使用默认配置。对于每个项目：
- **自定义调色板** — 永远不要原始`fill(255, 0, 0)`。始终是一个设计的3-7种颜色的调色板
- **自定义描边粗细词汇** — 细强调（0.5）、中等结构（1-2）、粗强调（3-5）
- **背景处理** — 永远不要简单的`background(0)`或`background(255)`。始终纹理化、渐变或分层
- **运动多样性** — 不同元素的不同速度。主要为1x，次要为0.3x，环境为0.1x
- **至少一个发明的元素** — 自定义粒子行为、新颖的噪声应用、独特的交互响应

### 项目特定的发明

对于每个项目，至少发明以下之一：
- 与心情匹配的自定义调色板（不是预设）
- 新颖的噪声场组合（例如，卷曲噪声 + 域扭曲 + 反馈）
- 独特的粒子行为（自定义力、自定义拖尾、自定义生成）
- 用户没有要求但提升作品的交互机制
- 创建视觉层次的构图技术

### 参数设计理念

参数应该从算法中涌现，而不是从通用菜单中。问："*这个*系统的哪些属性应该是可调的？"

**好的参数**暴露算法的特征：
- **数量** — 多少粒子、分支、单元格（控制密度）
- **比例** — 噪声频率、元素大小、间距（控制纹理）
- **速率** — 速度、增长率、衰减（控制能量）
- **阈值** — 行为何时改变？（控制戏剧性）
- **比率** — 比例、力之间的平衡（控制和谐）

**坏的参数**是与算法无关的通用控件：
- "color1"、"color2"、"size" — 没有上下文就没有意义
- 不相关效果的切换开关
- 只改变化妆品而不改变行为的参数

每个参数都应该改变算法*思考*的方式，而不仅仅是它*看起来*的方式。改变噪声八度的"湍流"参数是好的。只改变`ellipse()`半径的"粒子大小"滑块是肤浅的。

## 工作流程

### 步骤1：创意愿景

在任何代码之前，阐明：

- **心情 / 氛围**：观众应该感觉什么？沉思的？精力充沛的？不安的？好玩的？
- **视觉故事**：随着时间的推移（或交互时）会发生什么？构建？衰变？变换？振荡？
- **颜色世界**：温暖/凉爽？单色？互补？主色调是什么？强调色是什么？
- **形状语言**：有机曲线？锐利几何？点？线？混合？
- **运动词汇**：缓慢漂移？爆炸性爆发？呼吸脉冲？机械精度？
- **是什么让*这个*不同**：是什么让这个草图独特的一件事？

将用户的提示映射到美学选择。"放松的生成式背景"需要与"故障数据可视化"完全不同的一切。

### 步骤2：技术设计

- **模式** — 上面表格中的7种模式中的哪一种
- **画布大小** — 横向1920x1080、纵向1080x1920、方形1080x1080或响应式`windowWidth/windowHeight`
- **渲染器** — `P2D`（默认）或`WEBGL`（用于3D、着色器、高级混合模式）
- **帧率** — 60fps（交互式）、30fps（环境动画）或`noLoop()`（静态生成式）
- **导出目标** — 浏览器显示、PNG静止图像、GIF循环、MP4视频、SVG矢量
- **交互模型** — 被动（无输入）、鼠标驱动、键盘驱动、音频反应式、滚动驱动
- **查看器UI** — 对于交互式生成式艺术，从`templates/viewer.html`开始，它提供种子导航、参数滑块和下载。对于简单草图或视频导出，使用裸HTML

### 步骤3：编码草图

对于**交互式生成式艺术**（种子探索、参数调整）：从`templates/viewer.html`开始。首先阅读模板，保持固定部分（种子导航、操作），替换算法和参数控件。这为用户提供了种子上一个/下一个/随机/跳转、带实时更新的参数滑块和PNG下载 — 全部已连接。

对于**动画、视频导出或简单草图**：使用裸HTML：

单个HTML文件。结构：

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>项目名称</title>
  <script>p5.disableFriendlyErrors = true;</script>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/p5.min.js"></script>
  <!-- <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.11.3/addons/p5.sound.min.js"></script> -->
  <!-- <script src="https://unpkg.com/p5.js-svg@1.6.0"></script> -->  <!-- SVG导出 -->
  <!-- <script src="https://cdn.jsdelivr.net/npm/ccapture.js-npmfixed/build/CCapture.all.min.js"></script> -->  <!-- 视频捕获 -->
  <style>
    html, body { margin: 0; padding: 0; overflow: hidden; }
    canvas { display: block; }
  </style>
</head>
<body>
<script>
// === 配置 ===
const CONFIG = {
  seed: 42,
  // ... 项目特定参数
};

// === 调色板 ===
const PALETTE = {
  bg: '#0a0a0f',
  primary: '#e8d5b7',
  // ...
};

// === 全局状态 ===
let particles = [];

// === Preload（字体、图像、数据）===
function preload() {
  // font = loadFont('...');
}

// === Setup ===
function setup() {
  createCanvas(1920, 1080);
  randomSeed(CONFIG.seed);
  noiseSeed(CONFIG.seed);
  colorMode(HSB, 360, 100, 100, 100);
  // 初始化状态...
}

// === Draw循环 ===
function draw() {
  // 渲染帧...
}

// === 辅助函数 ===
// ...

// === 类 ===
class Particle {
  // ...
}

// === 事件处理程序 ===
function mousePressed() { /* ... */ }
function keyPressed() { /* ... */ }
function windowResized() { resizeCanvas(windowWidth, windowHeight); }
</script>
</body>
</html>
```

关键实现模式：
- **种子随机性**：始终`randomSeed()` + `noiseSeed()`以保证可重复性
- **颜色模式**：使用`colorMode(HSB, 360, 100, 100, 100)`进行直观的颜色控制
- **状态分离**：CONFIG用于参数，PALETTE用于颜色，全局变量用于可变状态
- **基于类的实体**：粒子、代理、形状作为具有`update()` + `display()`方法的类
- **离屏缓冲区**：`createGraphics()`用于分层合成、拖尾、遮罩

### 步骤4：预览和迭代

- 直接在浏览器中打开HTML文件 — 基本草图不需要服务器
- 对于从本地文件`loadImage()`/`loadFont()`：使用`scripts/serve.sh`或`python3 -m http.server`
- Chrome DevTools性能选项卡验证60fps
- 在目标导出分辨率下测试，而不仅仅是窗口大小
- 调整参数，直到视觉效果与步骤1的概念匹配

### 步骤5：导出

| 格式 | 方法 | 命令 |
|--------|--------|---------|
| **PNG** | `keyPressed()`中的`saveCanvas('output', 'png')` | 按's'保存 |
| **高分辨率PNG** | Puppeteer无头捕获 | `node scripts/export-frames.js sketch.html --width 3840 --height 2160 --frames 1` |
| **GIF** | `saveGif('output', 5)` — 捕获N秒 | 按'g'保存 |
| **帧序列** | `saveFrames('frame', 'png', 10, 30)` — 10s @ 30fps | 然后`ffmpeg -i frame-%04d.png -c:v libx264 output.mp4` |
| **MP4** | Puppeteer帧捕获 + ffmpeg | `bash scripts/render.sh sketch.html output.mp4 --duration 30 --fps 30` |
| **SVG** | 使用p5.js-svg的`createCanvas(w, h, SVG)` | `save('output.svg')` |

### 步骤6：质量验证

- **它与愿景匹配吗？** 将输出与创意概念进行比较。如果看起来通用，回到步骤1
- **分辨率检查**：在目标显示大小下是否锐利？没有锯齿伪影？
- **性能检查**：在浏览器中保持60fps吗？（动画最低30fps）
- **颜色检查**：颜色一起工作吗？在浅色和深色显示器上测试
- **边缘情况**：画布边缘发生了什么？调整大小后？运行10分钟后？

## 关键实现说明

### 性能 — 首先禁用FES

友好错误系统（FES）增加了高达10倍的开销。在每个生产草图中禁用它：

```javascript
p5.disableFriendlyErrors = true;  // 在setup()之前

function setup() {
  pixelDensity(1);  // 防止视网膜上的2x-4x过度绘制
  createCanvas(1920, 1080);
}
```

在热循环（粒子、像素操作）中，使用`Math.*`而不是p5包装器 — 明显更快：

```javascript
// 在draw()或update()热路径中：
let a = Math.sin(t);          // 不是sin(t)
let r = Math.sqrt(dx*dx+dy*dy); // 不是dist() — 或者更好：跳过sqrt，比较magSq
let v = Math.random();        // 不是random() — 当不需要种子时
let m = Math.min(a, b);       // 不是min(a, b)
```

永远不要在`draw()`内部`console.log()`。永远不要在`draw()`中操作DOM。查看`references/troubleshooting.md` § 性能。

### 种子随机性 — 始终

每个生成式草图必须是可重复的。相同的种子，相同的输出。

```javascript
function setup() {
  randomSeed(CONFIG.seed);
  noiseSeed(CONFIG.seed);
  // 所有random()和noise()调用现在都是确定性的
}
```

永远不要将`Math.random()`用于生成式内容 — 仅用于性能关键的非视觉代码。始终将`random()`用于视觉元素。如果你需要一个随机种子：`CONFIG.seed = floor(random(99999))`。

### 生成式艺术平台支持（fxhash / Art Blocks）

对于生成式艺术平台，用平台的确定性随机替换p5的PRNG：

```javascript
// fxhash约定
const SEED = $fx.hash;              // 每个铸造唯一
const rng = $fx.rand;               // 确定性PRNG
$fx.features({ palette: 'warm', complexity: 'high' });

// 在setup()中：
randomSeed(SEED);   // 用于p5的noise()
noiseSeed(SEED);

// 用rng()替换random()以实现平台确定性
let x = rng() * width;  // 而不是random(width)
```

查看`references/export-pipeline.md` § 平台导出。

### 颜色模式 — 使用HSB

HSB（色相、饱和度、亮度）对于生成式艺术比RGB更容易使用：

```javascript
colorMode(HSB, 360, 100, 100, 100);
// 现在：fill(hue, sat, bri, alpha)
// 旋转色相：fill((baseHue + offset) % 360, 80, 90)
// 去饱和：fill(hue, sat * 0.3, bri)
// 变暗：fill(hue, sat, bri * 0.5)
```

永远不要硬编码原始RGB值。定义一个调色板对象，程序化地推导变化。查看`references/color-systems.md`。

### 噪声 — 多八度，而不是原始

原始`noise(x, y)`看起来像平滑的斑点。分层八度以获得自然纹理：

```javascript
function fbm(x, y, octaves = 4) {
  let val = 0, amp = 1, freq = 1, sum = 0;
  for (let i = 0; i < octaves; i++) {
    val += noise(x * freq, y * freq) * amp;
    sum += amp;
    amp *= 0.5;
    freq *= 2;
  }
  return val / sum;
}
```

对于流动的有机形式，使用**域扭曲**：将噪声输出反馈为噪声输入坐标。查看`references/visual-effects.md`。

### 分层的createGraphics() — 不是可选的

平坦的单次渲染看起来平坦。使用离屏缓冲区进行合成：

```javascript
let bgLayer, fgLayer, trailLayer;
function setup() {
  createCanvas(1920, 1080);
  bgLayer = createGraphics(width, height);
  fgLayer = createGraphics(width, height);
  trailLayer = createGraphics(width, height);
}
function draw() {
  renderBackground(bgLayer);
  renderTrails(trailLayer);   // 持久的，褪色的
  renderForeground(fgLayer);  // 每帧清除
  image(bgLayer, 0, 0);
  image(trailLayer, 0, 0);
  image(fgLayer, 0, 0);
}
```

### 性能 — 在可能的情况下向量化

p5.js绘制调用很昂贵。对于数千个粒子：

```javascript
// 慢：单个形状
for (let p of particles) {
  ellipse(p.x, p.y, p.size);
}

// 快：带beginShape()的单个形状
beginShape(POINTS);
for (let p of particles) {
  vertex(p.x, p.y);
}
endShape();

// 最快：用于海量计数的像素缓冲区
loadPixels();
for (let p of particles) {
  let idx = 4 * (floor(p.y) * width + floor(p.x));
  pixels[idx] = r; pixels[idx+1] = g; pixels[idx+2] = b; pixels[idx+3] = 255;
}
updatePixels();
```

查看`references/troubleshooting.md` § 性能。

### 多个草图的实例模式

全局模式污染`window`。对于生产，使用实例模式：

```javascript
const sketch = (p) => {
  p.setup = function() {
    p.createCanvas(800, 800);
  };
  p.draw = function() {
    p.background(0);
    p.ellipse(p.mouseX, p.mouseY, 50);
  };
};
new p5(sketch, 'canvas-container');
```

在一个页面上嵌入多个草图或与框架集成时需要。

### WebGL模式陷阱

- `createCanvas(w, h, WEBGL)` — 原点是中心，而不是左上角
- Y轴是反转的（WEBGL中Y向上，P2D中Y向下）
- `translate(-width/2, -height/2)`以获得类似P2D的坐标
- 每个变换周围都有`push()`/`pop()` — 矩阵堆栈静默溢出
- `texture()`在`rect()`/`plane()`之前 — 不是之后
- 自定义着色器：`createShader(vert, frag)` — 在多个浏览器上测试

### 导出 — 键绑定约定

每个草图都应该在`keyPressed()`中包含这些：

```javascript
function keyPressed() {
  if (key === 's' || key === 'S') saveCanvas('output', 'png');
  if (key === 'g' || key === 'G') saveGif('output', 5);
  if (key === 'r' || key === 'R') { randomSeed(millis()); noiseSeed(millis()); }
  if (key === ' ') CONFIG.paused = !CONFIG.paused;
}
```

### 无头视频导出 — 使用noLoop()

对于通过Puppeteer的无头渲染，草图**必须**在setup中使用`noLoop()`。没有它，当截图很慢时，p5的draw循环会自由运行 — 草图会提前，你会得到跳过/重复的帧。

```javascript
function setup() {
  createCanvas(1920, 1080);
  pixelDensity(1);
  noLoop();                    // 捕获脚本控制帧前进
  window._p5Ready = true;      // 向捕获脚本发出准备就绪信号
}
```

捆绑的`scripts/export-frames.js`检测`_p5Ready`并每次捕获调用`redraw()`一次，以获得精确的1:1帧对应。查看`references/export-pipeline.md` § 确定性捕获。

对于多场景视频，使用每个剪辑架构：每个场景一个HTML，独立渲染，用`ffmpeg -f concat`拼接。查看`references/export-pipeline.md` § 每个剪辑架构。

### 代理工作流程

构建p5.js草图时：

1. **编写HTML文件** — 单个自包含文件，所有代码内联
2. **在浏览器中打开** — `open sketch.html`（macOS）或`xdg-open sketch.html`（Linux）
3. **本地资产**（字体、图像）需要服务器：在项目目录中`python3 -m http.server 8080`，然后打开`http://localhost:8080/sketch.html`
4. **导出PNG/GIF** — 按上面所示添加`keyPressed()`快捷方式，告诉用户按哪个键
5. **无头导出** — `node scripts/export-frames.js sketch.html --frames 300`用于自动帧捕获（草图必须使用`noLoop()` + `_p5Ready`）
6. **MP4渲染** — `bash scripts/render.sh sketch.html output.mp4 --duration 30`
7. **迭代细化** — 编辑HTML文件，用户刷新浏览器以查看更改
8. **按需加载参考** — 在实施期间使用`skill_view(name="p5js", file_path="references/...")`根据需要加载特定参考文件

## 性能目标

| 指标 | 目标 |
|--------|--------|
| 帧率（交互式）| 持续60fps |
| 帧率（动画导出）| 最低30fps |
| 粒子计数（P2D形状）| 60fps时5,000-10,000 |
| 粒子计数（像素缓冲区）| 60fps时50,000-100,000 |
| 画布分辨率 | 高达3840x2160（导出），1920x1080（交互式）|
| 文件大小（HTML）| < 100KB（不包括CDN库）|
| 加载时间 | < 2s到第一帧 |

## 参考

| 文件 | 内容 |
|------|----------|
| `references/core-api.md` | 画布设置、坐标系、draw循环、`push()`/`pop()`、离屏缓冲区、合成模式、`pixelDensity()`、响应式设计 |
| `references/shapes-and-geometry.md` | 2D基元、`beginShape()`/`endShape()`、贝塞尔/Catmull-Rom曲线、`vertex()`系统、自定义形状、`p5.Vector`、有符号距离场、SVG路径转换 |
| `references/visual-effects.md` | 噪声（Perlin、分形、域扭曲、卷曲）、流场、粒子系统（物理、群体、拖尾）、像素操作、纹理生成（点画、阴影线、半色调）、反馈循环、反应扩散 |
| `references/animation.md` | 基于帧的动画、缓动函数、`lerp()`/`map()`、弹簧物理、状态机、时间线排序、基于`millis()`的计时、过渡模式 |
| `references/typography.md` | `text()`、`loadFont()`、`textToPoints()`、动态排版、文本遮罩、字体指标、响应式文本大小 |
| `references/color-systems.md` | `colorMode()`、HSB/HSL/RGB、`lerpColor()`、`paletteLerp()`、程序化调色板、颜色和谐、`blendMode()`、渐变渲染、策划的调色板库 |
| `references/webgl-and-3d.md` | WEBGL渲染器、3D基元、相机、照明、材质、自定义几何、GLSL着色器（`createShader()`、`createFilterShader()`）、帧缓冲区、后处理 |
| `references/interaction.md` | 鼠标事件、键盘状态、触摸输入、DOM元素、`createSlider()`/`createButton()`、音频输入（p5.sound FFT/振幅）、滚动驱动动画、响应式事件 |
| `references/export-pipeline.md` | `saveCanvas()`、`saveGif()`、`saveFrames()`、确定性无头捕获、ffmpeg帧到视频、CCapture.js、SVG导出、每个剪辑架构、平台导出（fxhash）、视频陷阱 |
| `references/troubleshooting.md` | 性能分析、每像素预算、常见错误、浏览器兼容性、WebGL调试、字体加载问题、像素密度陷阱、内存泄漏、CORS |
| `templates/viewer.html` | 交互式查看器模板：种子导航（上一个/下一个/随机/跳转）、参数滑块、下载PNG、响应式画布。从这个开始用于可探索的生成式艺术 |

---

## 创意分歧（仅在用户请求实验性/创意/独特输出时使用）

如果用户要求创意、实验性、令人惊讶或非常规的输出，在生成代码之前选择最适合的策略并推理其步骤。

- **概念混合** — 当用户命名两个要组合的事物或想要混合美学时
- **SCAMPER** — 当用户想要对已知的生成式艺术模式进行扭曲时
- **距离关联** — 当用户给出单个概念并想要探索时（"制作关于时间的东西"）

### 概念混合
1. 命名两个不同的视觉系统（例如，粒子物理 + 手写）
2. 映射对应关系（粒子 = 墨水滴，力 = 笔压，场 = 字母形式）
3. 选择性地混合 — 保持产生有趣的涌现视觉效果的映射
4. 将混合编码为一个统一的系统，而不是两个并排的系统

### SCAMPER变换
采用已知的生成式模式（流场、粒子系统、L系统、元胞自动机）并系统地变换它：
- **替代**：用文本字符替换圆形，用渐变替换线条
- **组合**：合并两个模式（流场 + 沃罗诺伊）
- **适应**：将2D模式应用于3D投影
- **修改**：夸大比例，扭曲坐标空间
- **用途**：将物理模拟用于排版，将排序算法用于颜色
- **消除**：删除网格，删除颜色，删除对称性
- **逆转**：向后运行模拟，反转参数空间

### 距离关联
1. 锚定在用户的概念上（例如，"孤独"）
2. 在三个距离生成关联：
   - 接近（明显）：空房间、单个身影、沉默
   - 中等（有趣）：一群鱼中一条鱼游错方向、没有通知的手机、地铁车厢之间的间隙
   - 遥远（抽象）：质数、渐近曲线、凌晨3点的颜色
3. 开发中等距离的关联 — 它们足够具体可以可视化，但又足够出乎意料可以有趣
