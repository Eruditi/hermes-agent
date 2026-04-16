---
name: obsidian
description: 读取、搜索和创建 Obsidian 仓库中的笔记。
---

# Obsidian 仓库

**位置：** 通过 `OBSIDIAN_VAULT_PATH` 环境变量设置（例如在 `~/.hermes/.env` 中）。

如果未设置，默认为 `~/Documents/Obsidian Vault`。

注意：仓库路径可能包含空格 - 始终引用它们。

## 读取笔记

```bash
VAULT=\"${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}\"
cat \"$VAULT/Note Name.md\"
```

## 列出笔记

```bash
VAULT=\"${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}\"

# 所有笔记
find \"$VAULT\" -name \"*.md\" -type f

# 在特定文件夹中
ls \"$VAULT/Subfolder/\"
```

## 搜索

```bash
VAULT=\"${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}\"

# 按文件名
find \"$VAULT\" -name \"*.md\" -iname \"*keyword*\"

# 按内容
grep -rli \"keyword\" \"$VAULT\" --include=\"*.md\"
```

## 创建笔记

```bash
VAULT=\"${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}\"
cat > \"$VAULT/New Note.md\" << 'ENDNOTE'
# 标题

内容在这里。
ENDNOTE
```

## 追加到笔记

```bash
VAULT=\"${OBSIDIAN_VAULT_PATH:-$HOME/Documents/Obsidian Vault}\"
echo \"
新内容在这里。\" >> \"$VAULT/Existing Note.md\"
```

## Wiki 链接

Obsidian 使用 `[[Note Name]]` 语法链接笔记。创建笔记时，使用这些链接相关内容。
