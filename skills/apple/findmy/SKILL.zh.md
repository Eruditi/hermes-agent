---
name: findmy
description: 通过macOS上的FindMy.app使用AppleScript和屏幕截图追踪Apple设备和AirTag。
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [查找, AirTag, 位置, 追踪, macOS, Apple]
---

# 查找（Apple）

通过macOS上的FindMy.app追踪Apple设备和AirTag。由于Apple没有为FindMy提供CLI，此技能使用AppleScript打开应用并使用屏幕截图读取设备位置。

## 先决条件

- 已登录iCloud并带有Find My应用的**macOS**
- 已在Find My中注册的设备/AirTag
- 终端的屏幕录制权限（系统设置 → 隐私 → 屏幕录制）
- **可选但推荐**：安装`peekaboo`以获得更好的UI自动化：
  `brew install steipete/tap/peekaboo`

## 何时使用

- 用户询问"我的[设备/猫/钥匙/包]在哪里？"
- 追踪AirTag位置
- 检查设备位置（iPhone、iPad、Mac、AirPods）
- 随时间监控宠物或物品移动（AirTag巡逻路线）

## 方法1：AppleScript + 截图（基础）

### 打开FindMy并导航

```bash
# 打开Find My应用
osascript -e 'tell application "FindMy" to activate'

# 等待加载
sleep 3

# 截取Find My窗口的屏幕截图
screencapture -w -o /tmp/findmy.png
```

然后使用`vision_analyze`读取屏幕截图：
```
vision_analyze(image_url="/tmp/findmy.png", question="显示了哪些设备/物品，它们的位置是什么？")
```

### 在选项卡之间切换

```bash
# 切换到设备选项卡
osascript -e '
tell application "System Events"
    tell process "FindMy"
        click button "Devices" of toolbar 1 of window 1
    end tell
end tell'

# 切换到物品选项卡（AirTags）
osascript -e '
tell application "System Events"
    tell process "FindMy"
        click button "Items" of toolbar 1 of window 1
    end tell
end tell'
```

## 方法2：Peekaboo UI自动化（推荐）

如果已安装`peekaboo`，使用它进行更可靠的UI交互：

```bash
# 打开Find My
osascript -e 'tell application "FindMy" to activate'
sleep 3

# 捕获并标注UI
peekaboo see --app "FindMy" --annotate --path /tmp/findmy-ui.png

# 通过元素ID点击特定设备/物品
peekaboo click --on B3 --app "FindMy"

# 捕获详细视图
peekaboo image --app "FindMy" --path /tmp/findmy-detail.png
```

然后使用视觉分析：
```
vision_analyze(image_url="/tmp/findmy-detail.png", question="此设备/物品显示的位置是什么？如果可见，请包含地址和坐标。")
```

## 工作流程：随时间追踪AirTag位置

对于监控AirTag（例如，追踪猫的巡逻路线）：

```bash
# 1. 打开Find My到物品选项卡
osascript -e 'tell application "FindMy" to activate'
sleep 3

# 2. 点击AirTag物品（留在页面上 — AirTag仅在页面打开时更新）

# 3. 定期捕获位置
while true; do
    screencapture -w -o /tmp/findmy-$(date +%H%M%S).png
    sleep 300  # 每5分钟
done
```

使用视觉分析每个屏幕截图以提取坐标，然后编译路线。

## 限制

- FindMy**没有CLI或API** — 必须使用UI自动化
- AirTag仅在Find My页面主动显示时才更新位置
- 位置精度取决于Find My网络中附近的Apple设备
- 截图需要屏幕录制权限
- AppleScript UI自动化可能在macOS版本之间失效

## 规则

1. 追踪AirTag时保持Find My应用在前台（最小化时更新停止）
2. 使用`vision_analyze`读取屏幕截图内容 — 不要尝试解析像素
3. 对于持续追踪，使用定时任务定期捕获并记录位置
4. 尊重隐私 — 仅追踪用户拥有的设备/物品
