---
name: apple-reminders
description: 通过remindctl CLI管理Apple提醒事项（列出、添加、完成、删除）。
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [提醒事项, 任务, 待办, macOS, Apple]
prerequisites:
  commands: [remindctl]
---

# Apple提醒事项

使用`remindctl`直接从终端管理Apple提醒事项。任务通过iCloud在所有Apple设备之间同步。

## 先决条件

- 带Reminders.app的**macOS**
- 安装：`brew install steipete/tap/remindctl`
- 出现提示时授予提醒事项权限
- 检查：`remindctl status` / 请求授权：`remindctl authorize`

## 何时使用

- 用户提到"提醒"或"提醒事项应用"
- 创建带有截止日期的个人待办事项，同步到iOS
- 管理Apple提醒事项列表
- 用户希望任务显示在他们的iPhone/iPad上

## 何时不使用

- 安排代理提醒 → 改用cronjob工具
- 日历事件 → 使用Apple Calendar或Google Calendar
- 项目任务管理 → 使用GitHub Issues、Notion等
- 如果用户说"提醒我"但指的是代理提醒 → 先澄清

## 快速参考

### 查看提醒事项

```bash
remindctl                    # 今天的提醒事项
remindctl today              # 今天
remindctl tomorrow           # 明天
remindctl week               # 本周
remindctl overdue            # 已过期
remindctl all                # 全部
remindctl 2026-01-04         # 特定日期
```

### 管理列表

```bash
remindctl list               # 列出所有列表
remindctl list Work          # 显示特定列表
remindctl list Projects --create    # 创建列表
remindctl list Work --delete        # 删除列表
```

### 创建提醒事项

```bash
remindctl add "买牛奶"
remindctl add --title "给妈妈打电话" --list Personal --due tomorrow
remindctl add --title "会议准备" --due "2026-02-15 09:00"
```

### 完成/删除

```bash
remindctl complete 1 2 3          # 按ID完成
remindctl delete 4A83 --force     # 按ID删除
```

### 输出格式

```bash
remindctl today --json       # JSON用于脚本
remindctl today --plain      # TSV格式
remindctl today --quiet      # 仅计数
```

## 日期格式

`--due`和日期过滤器接受以下格式：
- `today`、`tomorrow`、`yesterday`
- `YYYY-MM-DD`
- `YYYY-MM-DD HH:mm`
- ISO 8601（`2026-01-04T12:34:56Z`）

## 规则

1. 当用户说"提醒我"时，澄清：Apple提醒事项（同步到手机）还是代理定时任务提醒
2. 创建前始终确认提醒内容和截止日期
3. 使用`--json`进行编程解析
