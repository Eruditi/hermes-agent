---
name: apple-notes
description: 通过macOS上的memo CLI管理Apple Notes（创建、查看、搜索、编辑）。
version: 1.0.0
author: Hermes Agent
license: MIT
platforms: [macos]
metadata:
  hermes:
    tags: [Notes, Apple, macOS, 笔记]
    related_skills: [obsidian]
prerequisites:
  commands: [memo]
---

# Apple Notes

使用`memo`直接从终端管理Apple Notes。笔记通过iCloud在所有Apple设备上同步。

## 先决条件

- **macOS** 带Notes.app
- 安装：`brew tap antoniorodr/memo && brew install antoniorodr/memo/memo`
- 当提示时，授予Notes.app自动化访问权限（系统设置 → 隐私 → 自动化）

## 何时使用

- 用户要求创建、查看或搜索Apple Notes
- 将信息保存到Notes.app以进行跨设备访问
- 将笔记组织到文件夹中
- 将笔记导出到Markdown/HTML

## 何时不使用

- Obsidian库管理 → 使用`obsidian`技能
- Bear Notes → 单独的应用（此处不支持）
- 快速代理专用笔记 → 改为使用`memory`工具

## 快速参考

### 查看笔记

```bash
memo notes                        # 列出所有笔记
memo notes -f "Folder Name"       # 按文件夹过滤
memo notes -s "query"             # 搜索笔记（模糊）
```

### 创建笔记

```bash
memo notes -a                     # 交互式编辑器
memo notes -a "Note Title"        # 快速添加标题
```

### 编辑笔记

```bash
memo notes -e                     # 交互式选择编辑
```

### 删除笔记

```bash
memo notes -d                     # 交互式选择删除
```

### 移动笔记

```bash
memo notes -m                     # 将笔记移动到文件夹（交互式）
```

### 导出笔记

```bash
memo notes -ex                    # 导出到HTML/Markdown
```

## 限制

- 无法编辑包含图像或附件的笔记
- 交互式提示需要终端访问（如需要，使用pty=true）
- 仅限macOS — 需要Apple Notes.app

## 规则

1. 当用户需要跨设备同步（iPhone/iPad/Mac）时，首选Apple Notes
2. 使用`memory`工具存储不需要同步的代理内部笔记
3. 使用`obsidian`技能进行Markdown原生知识管理