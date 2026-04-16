---
name: popular-web-designs
description: >
  从真实网站提取的54个生产质量设计系统。加载模板以生成与Stripe、Linear、Vercel、Notion、Airbnb等网站视觉标识匹配的HTML/CSS。每个模板都包含颜色、排版、组件、布局规则和即用型CSS值。
version: 1.0.0
author: Hermes Agent + Teknium (design systems sourced from VoltAgent/awesome-design-md)
license: MIT
tags: [设计, css, html, ui, web开发, 设计系统, 模板]
triggers:
  - 构建一个看起来像的页面
  - 让它看起来像stripe
  - 像linear一样设计
  - vercel风格
  - 创建一个UI
  - 网页设计
  - 着陆页
  - 仪表板设计
  - 网站风格像
---

# 流行网页设计

54个真实世界的设计系统，可在生成HTML/CSS时使用。每个模板都捕获了网站的完整视觉语言：调色板、排版层次结构、组件样式、间距系统、阴影、响应式行为，以及带有精确CSS值的实用代理提示。

## 如何使用

1. 从下面的目录中选择一个设计
2. 加载它：`skill_view(name="popular-web-designs", file_path="templates/<site>.md")`
3. 在生成HTML时使用设计令牌和组件规范
4. 与`generative-widgets`技能配对，通过cloudflared隧道提供结果

每个模板在顶部都包含一个**Hermes实现说明**块，包含：
- CDN字体替代品和Google Fonts `<link>`标签（准备粘贴）
- 主要和等宽的CSS字体族堆栈
- 提醒使用`write_file`创建HTML和`browser_vision`进行验证

## HTML生成模式

```html
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>页面标题</title>
  <!-- 粘贴模板Hermes说明中的Google Fonts <link> -->
  <link href="https://fonts.googleapis.com/css2?family=..." rel="stylesheet">
  <style>
    /* 将模板的调色板应用为CSS自定义属性 */
    :root {
      --color-bg: #ffffff;
      --color-text: #171717;
      --color-accent: #533afd;
      /* ... 更多来自模板第2部分 */
    }
    /* 应用模板第3部分的排版 */
    body {
      font-family: 'Inter', system-ui, sans-serif;
      color: var(--color-text);
      background: var(--color-bg);
    }
    /* 应用模板第4部分的组件样式 */
    /* 应用模板第5部分的布局 */
    /* 应用模板第6部分的阴影 */
  </style>
</head>
<body>
  <!-- 使用模板中的组件规范构建 -->
</body>
</html>
```

使用`write_file`编写文件，使用`generative-widgets`工作流（cloudflared隧道）提供服务，并使用`browser_vision`验证结果以确认视觉准确性。

## 字体替换参考

大多数网站使用通过CDN不可用的专有字体。每个模板都映射到一个Google Fonts替代品，以保留设计的特征。常见映射：

| 专有字体 | CDN替代品 | 特征 |
|---|---|---|
| Geist / Geist Sans | Geist（在Google Fonts上）| 几何，紧凑的字距 |
| Geist Mono | Geist Mono（在Google Fonts上）| 干净的等宽，连字 |
| sohne-var（Stripe）| Source Sans 3 | 轻量优雅 |
| Berkeley Mono | JetBrains Mono | 技术等宽 |
| Airbnb Cereal VF | DM Sans | 圆润，友好的几何 |
| Circular（Spotify）| DM Sans | 几何，温暖 |
| figmaSans | Inter | 干净的人文主义 |
| Pin Sans（Pinterest）| DM Sans | 友好，圆润 |
| NVIDIA-EMEA | Inter（或Arial系统）| 工业，干净 |
| CoinbaseDisplay/Sans | DM Sans | 几何，值得信赖 |
| UberMove | DM Sans | 粗体，紧凑 |
| HashiCorp Sans | Inter | 企业，中性 |
| waldenburgNormal（Sanity）| Space Grotesk | 几何，略微紧凑 |
| IBM Plex Sans/Mono | IBM Plex Sans/Mono | 在Google Fonts上可用 |
| Rubik（Sentry）| Rubik | 在Google Fonts上可用 |

当模板的CDN字体与原始字体匹配时（Inter、IBM Plex、Rubik、Geist），不会发生替换损失。当使用替代品时（Circular用DM Sans，sohne-var用Source Sans 3），请密切遵循模板的粗细、大小和字间距值 — 这些比特定的字体面孔承载更多的视觉标识。

## 设计目录

### AI与机器学习

| 模板 | 网站 | 风格 |
|---|---|---|
| `claude.md` | Anthropic Claude | 温暖的陶土强调，干净的编辑布局 |
| `cohere.md` | Cohere | 充满活力的渐变，数据丰富的仪表板美学 |
| `elevenlabs.md` | ElevenLabs | 深色电影UI，音频波形美学 |
| `minimax.md` | Minimax | 粗体深色界面，带霓虹强调 |
| `mistral.ai.md` | Mistral AI | 法国工程极简主义，紫色调 |
| `ollama.md` | Ollama | 终端优先，单色简约 |
| `opencode.ai.md` | OpenCode AI | 以开发者为中心的深色主题，全等宽 |
| `replicate.md` | Replicate | 干净的白色画布，代码优先 |
| `runwayml.md` | RunwayML | 电影深色UI，媒体丰富的布局 |
| `together.ai.md` | Together AI | 技术，蓝图风格设计 |
| `voltagent.md` | VoltAgent | 虚空黑色画布，祖母绿强调，终端原生 |
| `x.ai.md` | xAI | 鲜明的单色，未来主义极简主义，全等宽 |

### 开发者工具与平台

| 模板 | 网站 | 风格 |
|---|---|---|
| `cursor.md` | Cursor | 时尚的深色界面，渐变强调 |
| `expo.md` | Expo | 深色主题，紧凑的字距，代码中心 |
| `linear.app.md` | Linear | 超极简深色模式，精确，紫色强调 |
| `lovable.md` | Lovable | 好玩的渐变，友好的开发者美学 |
| `mintlify.md` | Mintlify | 干净，绿色强调，阅读优化 |
| `posthog.md` | PostHog | 好玩的品牌，开发者友好的深色UI |
| `raycast.md` | Raycast | 时尚的深色铬，充满活力的渐变强调 |
| `resend.md` | Resend | 极简深色主题，等宽强调 |
| `sentry.md` | Sentry | 深色仪表板，数据密集，粉紫强调 |
| `supabase.md` | Supabase | 深色祖母绿主题，代码优先开发者工具 |
| `superhuman.md` | Superhuman | 高级深色UI，键盘优先，紫色发光 |
| `vercel.md` | Vercel | 黑白精确，Geist字体系统 |
| `warp.md` | Warp | 深色IDE类界面，基于块的命令UI |
| `zapier.md` | Zapier | 温暖橙色，友好的插图驱动 |

### 基础设施与云

| 模板 | 网站 | 风格 |
|---|---|---|
| `clickhouse.md` | ClickHouse | 黄色强调，技术文档风格 |
| `composio.md` | Composio | 现代深色，带彩色集成图标 |
| `hashicorp.md` | HashiCorp | 企业干净，黑白 |
| `mongodb.md` | MongoDB | 绿叶品牌，开发者文档重点 |
| `sanity.md` | Sanity | 红色强调，内容优先编辑布局 |
| `stripe.md` | Stripe | 标志性紫色渐变，weight-300优雅 |

### 设计与生产力

| 模板 | 网站 | 风格 |
|---|---|---|
| `airtable.md` | Airtable | 多彩，友好，结构化数据美学 |
| `cal.md` | Cal.com | 干净的中性UI，开发者导向的简约 |
| `clay.md` | Clay | 有机形状，柔和渐变，艺术导向布局 |
| `figma.md` | Figma | 充满活力的多色，好玩但专业 |
| `framer.md` | Framer | 粗体黑蓝，运动优先，设计前瞻 |
| `intercom.md` | Intercom | 友好的蓝色调色板，对话UI模式 |
| `miro.md` | Miro | 明亮黄色强调，无限画布美学 |
| `notion.md` | Notion | 温暖极简主义，衬线标题，柔和表面 |
| `pinterest.md` | Pinterest | 红色强调，石工网格，图像优先布局 |
| `webflow.md` | Webflow | 蓝色强调，抛光营销网站美学 |

### 金融科技与加密

| 模板 | 网站 | 风格 |
|---|---|---|
| `coinbase.md` | Coinbase | 干净的蓝色标识，信任聚焦，机构感 |
| `kraken.md` | Kraken | 紫色强调的深色UI，数据密集仪表板 |
| `revolut.md` | Revolut | 时尚的深色界面，渐变卡片，金融科技精确 |
| `wise.md` | Wise | 明亮绿色强调，友好清晰 |

### 企业与消费者

| 模板 | 网站 | 风格 |
|---|---|---|
| `airbnb.md` | Airbnb | 温暖珊瑚强调，摄影驱动，圆润UI |
| `apple.md` | Apple | 高级白色空间，SF Pro，电影图像 |
| `bmw.md` | BMW | 深色高级表面，精确工程美学 |
| `ibm.md` | IBM | Carbon设计系统，结构化蓝色调色板 |
| `nvidia.md` | NVIDIA | 绿黑能量，技术力量美学 |
| `spacex.md` | SpaceX | 鲜明的黑白，全出血图像，未来主义 |
| `spotify.md` | Spotify | 深色上的充满活力的绿色，粗体字体，专辑艺术驱动 |
| `uber.md` | Uber | 粗体黑白，紧凑字体，城市能量 |

## 选择设计

将设计与内容匹配：

- **开发者工具 / 仪表板：** Linear、Vercel、Supabase、Raycast、Sentry
- **文档 / 内容网站：** Mintlify、Notion、Sanity、MongoDB
- **营销 / 着陆页：** Stripe、Framer、Apple、SpaceX
- **深色模式UI：** Linear、Cursor、ElevenLabs、Warp、Superhuman
- **浅色 / 干净UI：** Vercel、Stripe、Notion、Cal.com、Replicate
- **好玩 / 友好：** PostHog、Figma、Lovable、Zapier、Miro
- **高级 / 奢华：** Apple、BMW、Stripe、Superhuman、Revolut
- **数据密集 / 仪表板：** Sentry、Kraken、Cohere、ClickHouse
- **等宽 / 终端美学：** Ollama、OpenCode、x.ai、VoltAgent
