---
name: arxiv
description: 使用 arXiv 的免费 REST API 搜索和检索学术论文。无需 API 密钥。按关键词、作者、类别或 ID 搜索。结合 web_extract 或 ocr-and-documents 技能读取完整论文内容。
version: 1.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [Research, Arxiv, Papers, Academic, Science, API]
    related_skills: [ocr-and-documents]
---

# arXiv 研究

通过 arXiv 的免费 REST API 搜索和检索学术论文。无需 API 密钥，无需依赖项 — 只需 curl。

## 快速参考

| 操作 | 命令 |
|--------|---------|
| 搜索论文 | `curl \"https://export.arxiv.org/api/query?search_query=all:QUERY&max_results=5\"` |
| 获取特定论文 | `curl \"https://export.arxiv.org/api/query?id_list=2402.03300\"` |
| 读取摘要（网页） | `web_extract(urls=[\"https://arxiv.org/abs/2402.03300\"])` |
| 读取完整论文（PDF） | `web_extract(urls=[\"https://arxiv.org/pdf/2402.03300\"])` |

## 搜索论文

API 返回 Atom XML。使用 `grep`/`sed` 解析或通过 `python3` 管道以获得清晰输出。

### 基本搜索

```bash
curl -s \"https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5\"
```

### 清晰输出（将 XML 解析为可读格式）

```bash
curl -s \"https://export.arxiv.org/api/query?search_query=all:GRPO+reinforcement+learning&max_results=5&sortBy=submittedDate&sortOrder=descending\" | python3 -c \"
import sys, xml.etree.ElementTree as ET
ns = {'a': 'http://www.w3.org/2005/Atom'}
root = ET.parse(sys.stdin).getroot()
for i, entry in enumerate(root.findall('a:entry', ns)):
    title = entry.find('a:title', ns).text.strip().replace('\\n', ' ')
    arxiv_id = entry.find('a:id', ns).text.strip().split('/abs/')[-1]
    published = entry.find('a:published', ns).text[:10]
    authors = ', '.join(a.find('a:name', ns).text for a in entry.findall('a:author', ns))
    summary = entry.find('a:summary', ns).text.strip()[:200]
    cats = ', '.join(c.get('term') for c in entry.findall('a:category', ns))
    print(f'{i+1}. [{arxiv_id}] {title}')
    print(f'   Authors: {authors}')
    print(f'   Published: {published} | Categories: {cats}')
    print(f'   Abstract: {summary}...')
    print(f'   PDF: https://arxiv.org/pdf/{arxiv_id}')
    print()
\"
```

## 搜索查询语法

| 前缀 | 搜索范围 | 示例 |
|--------|----------|---------|
| `all:` | 所有字段 | `all:transformer+attention` |
| `ti:` | 标题 | `ti:large+language+models` |
| `au:` | 作者 | `au:vaswani` |
| `abs:` | 摘要 | `abs:reinforcement+learning` |
| `cat:` | 类别 | `cat:cs.AI` |
| `co:` | 评论 | `co:accepted+NeurIPS` |

### 布尔运算符

```
# AND（使用 + 时为默认）
search_query=all:transformer+attention

# OR
search_query=all:GPT+OR+all:BERT

# AND NOT
search_query=all:language+model+ANDNOT+all:vision

# 精确短语
search_query=ti:\"chain+of+thought\"

# 组合
search_query=au:hinton+AND+cat:cs.LG
```

## 排序和分页

| 参数 | 选项 |
|-----------|---------|
| `sortBy` | `relevance`、`lastUpdatedDate`、`submittedDate` |
| `sortOrder` | `ascending`、`descending` |
| `start` | 结果偏移量（0 基） |
| `max_results` | 结果数量（默认 10，最多 30000） |

```bash
# cs.AI 中最新的 10 篇论文
curl -s \"https://export.arxiv.org/api/query?search_query=cat:cs.AI&sortBy=submittedDate&sortOrder=descending&max_results=10\"
```

## 常见类别

| 类别 | 领域 |
|----------|-------|
| `cs.AI` | 人工智能 |
| `cs.CL` | 计算语言学（NLP） |
| `cs.CV` | 计算机视觉 |
| `cs.LG` | 机器学习 |
| `cs.CR` | 密码学与安全 |
| `stat.ML` | 机器学习（统计学） |

完整列表：https://arxiv.org/category_taxonomy
