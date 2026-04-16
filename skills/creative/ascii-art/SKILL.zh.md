---
name: ascii-art
description: 使用pyfiglet（571种字体）、cowsay、boxes、toilet、image-to-ascii、远程API（asciified、ascii.co.uk）和LLM回退生成ASCII艺术。无需API密钥。
version: 4.0.0
author: 0xbyt4, Hermes Agent
license: MIT
dependencies: []
metadata:
  hermes:
    tags: [ASCII, 艺术, 横幅, 创意, Unicode, 文本艺术, pyfiglet, figlet, cowsay, boxes]
    related_skills: [excalidraw]

---

# ASCII艺术技能

多种工具满足不同的ASCII艺术需求。所有工具都是本地CLI程序或免费REST API — 无需API密钥。

## 工具1：文本横幅（pyfiglet — 本地）

将文本渲染为大型ASCII艺术横幅。571种内置字体。

### 设置

```bash
pip install pyfiglet --break-system-packages -q
```

### 使用

```bash
python3 -m pyfiglet "你的文本" -f slant
python3 -m pyfiglet "文本" -f doom -w 80    # 设置宽度
python3 -m pyfiglet --list_fonts             # 列出所有571种字体
```

### 推荐字体

| 风格 | 字体 | 最适合 |
|------|------|--------|
| 干净现代 | `slant` | 项目名称，标题 |
| 粗体块状 | `doom` | 标题，标志 |
| 大而易读 | `big` | 横幅 |
| 经典横幅 | `banner3` | 宽显示屏 |
| 紧凑 | `small` | 副标题 |
| 赛博朋克 | `cyberlarge` | 科技主题 |
| 3D效果 | `3-d` | 启动屏幕 |
| 哥特式 | `gothic` | 戏剧性文本 |

### 提示

- 预览2-3种字体，让用户选择他们喜欢的
- 短文本（1-8个字符）最适合使用详细字体，如`doom`或`block`
- 长文本更适合使用紧凑字体，如`small`或`mini`

## 工具2：文本横幅（asciified API — 远程，无需安装）

将文本转换为ASCII艺术的免费REST API。250+ FIGlet字体。直接返回纯文本 — 无需解析。当pyfiglet未安装或作为快速替代方案时使用。

### 使用（通过终端curl）

```bash
# 基本文本横幅（默认字体）
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello+World"

# 使用特定字体
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Slant"
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Doom"
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Star+Wars"
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=3-D"
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=Hello&font=Banner3"

# 列出所有可用字体（返回JSON数组）
curl -s "https://asciified.thelicato.io/api/v2/fonts"
```

### 提示

- 在text参数中将空格URL编码为`+`
- 响应是纯文本ASCII艺术 — 无JSON包装，随时可显示
- 字体名称区分大小写；使用fonts端点获取确切名称
- 可在任何带有curl的终端上工作 — 无需Python或pip

## 工具3：Cowsay（消息艺术）

经典工具，将文本包装在带有ASCII字符的 speech bubble 中。

### 设置

```bash
sudo apt install cowsay -y    # Debian/Ubuntu
# brew install cowsay         # macOS
```

### 使用

```bash
cowsay "Hello World"
cowsay -f tux "Linux rules"       # Tux the penguin
cowsay -f dragon "Rawr!"          # 龙
cowsay -f stegosaurus "Roar!"     # 剑龙
cowthink "Hmm..."                  # 思考气泡
cowsay -l                          # 列出所有字符
```

### 可用字符（50+）

`beavis.zen`, `bong`, `bunny`, `cheese`, `daemon`, `default`, `dragon`,
`dragon-and-cow`, `elephant`, `eyes`, `flaming-skull`, `ghostbusters`,
`hellokitty`, `kiss`, `kitty`, `koala`, `luke-koala`, `mech-and-cow`,
`meow`, `moofasa`, `moose`, `ren`, `sheep`, `skeleton`, `small`,
`stegosaurus`, `stimpy`, `supermilker`, `surgery`, `three-eyes`,
`turkey`, `turtle`, `tux`, `udder`, `vader`, `vader-koala`, `www`

### 眼睛/舌头修饰符

```bash
cowsay -b "Borg"       # =_= 眼睛
cowsay -d "Dead"       # x_x 眼睛
cowsay -g "Greedy"     # $_$ 眼睛
cowsay -p "Paranoid"   # @_@ 眼睛
cowsay -s "Stoned"     # *_* 眼睛
cowsay -w "Wired"      # O_O 眼睛
cowsay -e "OO" "Msg"   # 自定义眼睛
cowsay -T "U " "Msg"   # 自定义舌头
```

## 工具4：Boxes（装饰边框）

在任何文本周围绘制装饰性ASCII艺术边框/框架。70+内置设计。

### 设置

```bash
sudo apt install boxes -y    # Debian/Ubuntu
# brew install boxes         # macOS
```

### 使用

```bash
echo "Hello World" | boxes                    # 默认框
echo "Hello World" | boxes -d stone           # 石头边框
echo "Hello World" | boxes -d parchment       # 羊皮纸卷轴
echo "Hello World" | boxes -d cat             # 猫边框
echo "Hello World" | boxes -d dog             # 狗边框
echo "Hello World" | boxes -d unicornsay      # 独角兽
echo "Hello World" | boxes -d diamonds        # 钻石图案
echo "Hello World" | boxes -d c-cmt           # C风格注释
echo "Hello World" | boxes -d html-cmt        # HTML注释
echo "Hello World" | boxes -a c               # 居中文本
boxes -l                                       # 列出所有70+设计
```

### 与pyfiglet或asciified结合

```bash
python3 -m pyfiglet "HERMES" -f slant | boxes -d stone
# 或未安装pyfiglet时：
curl -s "https://asciified.thelicato.io/api/v2/ascii?text=HERMES&font=Slant" | boxes -d stone
```

## 工具5：TOIlet（彩色文本艺术）

类似pyfiglet但带有ANSI颜色效果和视觉过滤器。非常适合终端视觉效果。

### 设置

```bash
sudo apt install toilet toilet-fonts -y    # Debian/Ubuntu
# brew install toilet                      # macOS
```

### 使用

```bash
toilet "Hello World"                    # 基本文本艺术
toilet -f bigmono12 "Hello"            # 特定字体
toilet --gay "Rainbow!"                 # 彩虹着色
toilet --metal "Metal!"                 # 金属效果
toilet -F border "Bordered"             # 添加边框
toilet -F border --gay "Fancy!"         # 组合效果
toilet -f pagga "Block"                 # 块状字体（toilet独有）
toilet -F list                          # 列出可用过滤器
```

### 过滤器

`crop`, `gay` (彩虹), `metal`, `flip`, `flop`, `180`, `left`, `right`, `border`

**注意**：toilet输出用于颜色的ANSI转义码 — 在终端中工作，但可能无法在所有上下文中渲染（例如，纯文本文件，某些聊天平台）。

## 工具6：图像转ASCII艺术

将图像（PNG、JPEG、GIF、WEBP）转换为ASCII艺术。

### 选项A：ascii-image-converter（推荐，现代）

```bash
# 安装
sudo snap install ascii-image-converter
# 或：go install github.com/TheZoraiz/ascii-image-converter@latest
```

```bash
ascii-image-converter image.png                  # 基本
ascii-image-converter image.png -C               # 彩色输出
ascii-image-converter image.png -d 60,30         # 设置尺寸
ascii-image-converter image.png -b               # 盲文字符
ascii-image-converter image.png -n               # 负片/反转
ascii-image-converter https://url/image.jpg      # 直接URL
ascii-image-converter image.png --save-txt out   # 保存为文本
```

### 选项B：jp2a（轻量级，仅JPEG）

```bash
sudo apt install jp2a -y
jp2a --width=80 image.jpg
jp2a --colors image.jpg              # 彩色
```

## 工具7：搜索预制ASCII艺术

从网络搜索精选ASCII艺术。使用`terminal`和`curl`。

### 来源A：ascii.co.uk（推荐用于预制艺术）

按主题组织的经典ASCII艺术大集合。艺术位于HTML `<pre>`标签内。使用curl获取页面，然后使用小Python代码段提取艺术。

**URL模式**：`https://ascii.co.uk/art/{subject}`

**步骤1 — 获取页面**：

```bash
curl -s 'https://ascii.co.uk/art/cat' -o /tmp/ascii_art.html
```

**步骤2 — 从pre标签提取艺术**：

```python
import re, html
with open('/tmp/ascii_art.html') as f:
    text = f.read()
arts = re.findall(r'<pre[^>]*>(.*?)</pre>', text, re.DOTALL)
for art in arts:
    clean = re.sub(r'<[^>]+>', '', art)
    clean = html.unescape(clean).strip()
    if len(clean) > 30:
        print(clean)
        print('\n---\n')
```

**可用主题**（用作URL路径）：
- 动物：`cat`, `dog`, `horse`, `bird`, `fish`, `dragon`, `snake`, `rabbit`, `elephant`, `dolphin`, `butterfly`, `owl`, `wolf`, `bear`, `penguin`, `turtle`
- 对象：`car`, `ship`, `airplane`, `rocket`, `guitar`, `computer`, `coffee`, `beer`, `cake`, `house`, `castle`, `sword`, `crown`, `key`
- 自然：`tree`, `flower`, `sun`, `moon`, `star`, `mountain`, `ocean`, `rainbow`
- 角色：`skull`, `robot`, `angel`, `wizard`, `pirate`, `ninja`, `alien`
- 节日：`christmas`, `halloween`, `valentine`

**提示**：
- 保留艺术家签名/首字母 — 重要的礼仪
- 每页多个艺术作品 — 为用户选择最好的一个
- 通过curl可靠工作，无需JavaScript

### 来源B：GitHub Octocat API（有趣的彩蛋）

返回带有明智引语的随机GitHub Octocat。无需认证。

```bash
curl -s https://api.github.com/octocat
```

## 工具8：有趣的ASCII实用工具（通过curl）

这些免费服务直接返回ASCII艺术 — 非常适合有趣的附加内容。

### 作为ASCII艺术的QR码

```bash
curl -s "qrenco.de/Hello+World"
curl -s "qrenco.de/https://example.com"
```

### 作为ASCII艺术的天气

```bash
curl -s "wttr.in/London"          # 带有ASCII图形的完整天气报告
curl -s "wttr.in/Moon"            # ASCII艺术中的月相
curl -s "v2.wttr.in/London"       # 详细版本
```

## 工具9：LLM生成的自定义艺术（回退）

当上述工具没有所需内容时，使用这些Unicode字符直接生成ASCII艺术：

### 字符调色板

**框绘制**：`╔ ╗ ╚ ╝ ║ ═ ╠ ╣ ╦ ╩ ╬ ┌ ┐ └ ┘ │ ─ ├ ┤ ┬ ┴ ┼ ╭ ╮ ╰ ╯`

**块元素**：`░ ▒ ▓ █ ▄ ▀ ▌ ▐ ▖ ▗ ▘ ▝ ▚ ▞`

**几何与符号**：`◆ ◇ ◈ ● ○ ◉ ■ □ ▲ △ ▼ ▽ ★ ☆ ✦ ✧ ◀ ▶ ◁ ▷ ⬡ ⬢ ⌂`

### 规则

- 最大宽度：每行60个字符（终端安全）
- 最大高度：横幅15行，场景25行
- 仅等宽：输出必须在固定宽度字体中正确渲染

## 决策流程

1. **文本作为横幅** → 如果已安装pyfiglet，否则通过curl使用asciified API
2. **将消息包装在有趣的字符艺术中** → cowsay
3. **添加装饰性边框/框架** → boxes（可与pyfiglet/asciified结合）
4. **特定事物的艺术**（猫、火箭、龙）→ 通过curl + 解析使用ascii.co.uk
5. **将图像转换为ASCII** → ascii-image-converter或jp2a
6. **QR码** → 通过curl使用qrenco.de
7. **天气/月亮艺术** → 通过curl使用wttr.in
8. **自定义/创意内容** → 使用Unicode调色板的LLM生成
9. **任何未安装的工具** → 安装它，或回退到下一个选项