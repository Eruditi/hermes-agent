---
name: openhue
description: 通过OpenHue CLI控制Philips Hue灯光、房间和场景。打开/关闭灯光，调整亮度、颜色、色温，并激活场景。
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [Smart-Home, Hue, Lights, IoT, Automation, 智能家居, 灯光, 物联网, 自动化]
    homepage: https://www.openhue.io/cli
prerequisites:
  commands: [openhue]
---

# OpenHue CLI

通过终端中的Hue Bridge控制Philips Hue灯光和场景。

## 先决条件

```bash
# Linux（预构建二进制文件）
curl -sL https://github.com/openhue/openhue-cli/releases/latest/download/openhue-linux-amd64 -o ~/.local/bin/openhue && chmod +x ~/.local/bin/openhue

# macOS
brew install openhue/cli/openhue-cli
```

首次运行需要按Hue Bridge上的按钮进行配对。Bridge必须在同一本地网络上。

## 何时使用

- "打开/关闭灯光"
- "调暗客厅灯光"
- "设置场景"或"电影模式"
- 控制特定的Hue房间、区域或单个灯泡
- 调整亮度、颜色或色温

## 常见命令

### 列出资源

```bash
openhue get light       # 列出所有灯光
openhue get room        # 列出所有房间
openhue get scene       # 列出所有场景
```

### 控制灯光

```bash
# 打开/关闭
openhue set light "Bedroom Lamp" --on
openhue set light "Bedroom Lamp" --off

# 亮度（0-100）
openhue set light "Bedroom Lamp" --on --brightness 50

# 色温（从暖到冷：153-500 mirek）
openhue set light "Bedroom Lamp" --on --temperature 300

# 颜色（按名称或十六进制）
openhue set light "Bedroom Lamp" --on --color red
openhue set light "Bedroom Lamp" --on --rgb "#FF5500"
```

### 控制房间

```bash
# 关闭整个房间
openhue set room "Bedroom" --off

# 设置房间亮度
openhue set room "Bedroom" --on --brightness 30
```

### 场景

```bash
openhue set scene "Relax" --room "Bedroom"
openhue set scene "Concentrate" --room "Office"
```

## 快速预设

```bash
# 睡前（昏暗温暖）
openhue set room "Bedroom" --on --brightness 20 --temperature 450

# 工作模式（明亮凉爽）
openhue set room "Office" --on --brightness 100 --temperature 250

# 电影模式（昏暗）
openhue set room "Living Room" --on --brightness 10

# 全部关闭
openhue set room "Bedroom" --off
openhue set room "Office" --off
openhue set room "Living Room" --off
```

## 注意事项

- Bridge必须与运行Hermes的机器在同一本地网络上
- 首次运行需要物理按Hue Bridge上的按钮进行授权
- 颜色仅在支持颜色的灯泡上工作（不适用于仅白色型号）
- 灯光和房间名称区分大小写 — 使用`openhue get light`检查确切名称
- 非常适合用于定时照明的cron作业（例如，睡前调暗，醒来时调亮）