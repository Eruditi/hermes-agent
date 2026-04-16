---
name: ocr-and-documents
description: 从PDF和扫描文档中提取文本。对于远程URL使用web_extract，对于本地基于文本的PDF使用pymupdf，对于OCR/扫描文档使用marker-pdf。对于DOCX使用python-docx，对于PPTX请参阅powerpoint技能。
version: 2.3.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [PDF, 文档, 研究, Arxiv, 文本提取, OCR]
    related_skills: [powerpoint]
---

# PDF和文档提取

对于DOCX：使用`python-docx`（解析实际文档结构，远好于OCR）。
对于PPTX：请参阅`powerpoint`技能（使用带有完整幻灯片/备注支持的`python-pptx`）。
此技能涵盖**PDF和扫描文档**。

## 步骤1：远程URL可用？

如果文档有URL，**始终先尝试`web_extract`**：

```
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])
web_extract(urls=["https://example.com/report.pdf"])
```

这通过Firecrawl处理PDF到Markdown的转换，没有本地依赖项。

仅在以下情况下使用本地提取：文件是本地的，web_extract失败，或者您需要批量处理。

## 步骤2：选择本地提取器

| 功能 | pymupdf (~25MB) | marker-pdf (~3-5GB) |
|---------|-----------------|---------------------|
| **基于文本的PDF** | ✅ | ✅ |
| **扫描PDF（OCR）** | ❌ | ✅（90+种语言） |
| **表格** | ✅（基本） | ✅（高精度） |
| **方程式 / LaTeX** | ❌ | ✅ |
| **代码块** | ❌ | ✅ |
| **表单** | ❌ | ✅ |
| **页眉/页脚移除** | ❌ | ✅ |
| **阅读顺序检测** | ❌ | ✅ |
| **图像提取** | ✅（嵌入） | ✅（带有上下文） |
| **图像 → 文本（OCR）** | ❌ | ✅ |
| **EPUB** | ✅ | ✅ |
| **Markdown输出** | ✅（通过pymupdf4llm） | ✅（原生，更高质量） |
| **安装大小** | ~25MB | ~3-5GB（PyTorch + 模型） |
| **速度** | 即时 | ~1-14秒/页（CPU），~0.2秒/页（GPU） |

**决策**：使用pymupdf，除非您需要OCR、方程式、表单或复杂布局分析。

如果用户需要marker功能但系统缺少~5GB可用磁盘空间：
> "此文档需要OCR/高级提取（marker-pdf），这需要~5GB用于PyTorch和模型。您的系统有[X]GB可用。选项：释放空间，提供URL以便我可以使用web_extract，或者我可以尝试pymupdf，它适用于基于文本的PDF，但不适用于扫描文档或方程式。"

---

## pymupdf（轻量级）

```bash
pip install pymupdf pymupdf4llm
```

**通过辅助脚本**：
```bash
python scripts/extract_pymupdf.py document.pdf              # 纯文本
python scripts/extract_pymupdf.py document.pdf --markdown    # Markdown
python scripts/extract_pymupdf.py document.pdf --tables      # 表格
python scripts/extract_pymupdf.py document.pdf --images out/ # 提取图像
python scripts/extract_pymupdf.py document.pdf --metadata    # 标题、作者、页面
python scripts/extract_pymupdf.py document.pdf --pages 0-4   # 特定页面
```

**内联**：
```bash
python3 -c "
import pymupdf
doc = pymupdf.open('document.pdf')
for page in doc:
    print(page.get_text())
"
```

---

## marker-pdf（高质量OCR）

```bash
# 首先检查磁盘空间
python scripts/extract_marker.py --check

pip install marker-pdf
```

**通过辅助脚本**：
```bash
python scripts/extract_marker.py document.pdf                # Markdown
python scripts/extract_marker.py document.pdf --json         # 带有元数据的JSON
python scripts/extract_marker.py document.pdf --output_dir out/  # 保存图像
python scripts/extract_marker.py scanned.pdf                 # 扫描PDF（OCR）
python scripts/extract_marker.py document.pdf --use_llm      # LLM增强的准确性
```

**CLI**（与marker-pdf一起安装）：
```bash
marker_single document.pdf --output_dir ./output
marker /path/to/folder --workers 4    # 批量
```

---

## Arxiv论文

```
# 仅摘要（快速）
web_extract(urls=["https://arxiv.org/abs/2402.03300"])

# 完整论文
web_extract(urls=["https://arxiv.org/pdf/2402.03300"])

# 搜索
web_search(query="arxiv GRPO reinforcement learning 2026")
```

## 拆分、合并和搜索

pymupdf原生处理这些 — 使用`execute_code`或内联Python：

```python
# 拆分：将页面1-5提取到新PDF
import pymupdf
doc = pymupdf.open("report.pdf")
new = pymupdf.open()
for i in range(5):
    new.insert_pdf(doc, from_page=i, to_page=i)
new.save("pages_1-5.pdf")
```

```python
# 合并多个PDF
import pymupdf
result = pymupdf.open()
for path in ["a.pdf", "b.pdf", "c.pdf"]:
    result.insert_pdf(pymupdf.open(path))
result.save("merged.pdf")
```

```python
# 在所有页面中搜索文本
import pymupdf
doc = pymupdf.open("report.pdf")
for i, page in enumerate(doc):
    results = page.search_for("revenue")
    if results:
        print(f"Page {i+1}: {len(results)} match(es)")
        print(page.get_text("text"))
```

不需要额外的依赖项 — pymupdf在一个包中涵盖了拆分、合并、搜索和文本提取。

---

## 备注

- `web_extract`始终是URL的首选
- pymupdf是安全的默认值 — 即时、无模型、适用于任何地方
- marker-pdf用于OCR、扫描文档、方程式、复杂布局 — 仅在需要时安装
- 两个辅助脚本都接受`--help`以获取完整用法
- marker-pdf在首次使用时将~2.5GB的模型下载到`~/.cache/huggingface/`
- 对于Word文档：`pip install python-docx`（比OCR好 — 解析实际结构）
- 对于PowerPoint：请参阅`powerpoint`技能（使用python-pptx）
