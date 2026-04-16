---
name: nano-pdf
description: 使用nano-pdf CLI通过自然语言指令编辑PDF。修改文本、修复拼写错误、更新标题，并在特定页面上进行内容更改，无需手动编辑。
version: 1.0.0
author: community
license: MIT
metadata:
  hermes:
    tags: [PDF, 文档, 编辑, NLP, 生产力]
    homepage: https://pypi.org/project/nano-pdf/
---

# nano-pdf

使用自然语言指令编辑PDF。指向一个页面并描述要更改的内容。

## 先决条件

```bash
# 使用uv安装（推荐 — 已在Hermes中可用）
uv pip install nano-pdf

# 或使用pip
pip install nano-pdf
```

## 使用

```bash
nano-pdf edit <file.pdf> <page_number> "<instruction>"
```

## 示例

```bash
# 更改第1页的标题
nano-pdf edit deck.pdf 1 "将标题更改为'Q3结果'并修复副标题中的拼写错误"

# 更新特定页面上的日期
nano-pdf edit report.pdf 3 "将日期从2026年1月更新为2026年2月"

# 修复内容
nano-pdf edit contract.pdf 2 "将客户名称从'Acme Corp'更改为'Acme Industries'"
```

## 备注

- 页码可能是0-based或1-based，具体取决于版本 — 如果编辑命中了错误的页面，请重试±1
- 编辑后始终验证输出PDF（使用`read_file`检查文件大小，或打开它）
- 该工具在底层使用LLM — 需要API密钥（检查`nano-pdf --help`以获取配置）
- 适用于文本更改；复杂的布局修改可能需要不同的方法
