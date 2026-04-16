---
name: llm-wiki
description: "Karpathy's LLM Wiki — 构建和维护一个持久的、相互链接的 Markdown 知识库。摄取来源，查询编译的知识，并检查一致性。"
version: 2.0.0
author: Hermes Agent
license: MIT
metadata:
  hermes:
    tags: [wiki, knowledge-base, research, notes, markdown, rag-alternative]
    category: research
    related_skills: [obsidian, arxiv, agentic-research-ideas]
    config:
      - key: wiki.path
        description: Path to the LLM Wiki knowledge base directory
        default: "~/wiki"
        prompt: Wiki directory path
---

# Karpathy's LLM Wiki

构建和维护一个持久的、复合的知识库，以相互链接的 Markdown 文件形式存在。
基于 [Andrej Karpathy 的 LLM Wiki 模式](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f)。

与传统 RAG（每次查询都从头重新发现知识）不同，wiki
编译知识一次并保持其最新状态。交叉引用已经存在。
矛盾已经被标记。综合反映了所有摄取的内容。

**分工：** 人类策划来源并指导分析。代理
进行总结、交叉引用、归档和维护一致性。

## 此技能何时激活

当用户：
- 要求创建、构建或启动 wiki 或知识库
- 要求摄取、添加或处理来源到他们的 wiki
- 提出问题并且在配置路径中存在现有 wiki
- 要求检查、审计或健康检查他们的 wiki
- 在研究上下文中引用他们的 wiki、知识库或 "笔记"

## Wiki 位置

通过 `~/.hermes/config.yaml` 中的 `skills.config.wiki.path` 配置（在 `hermes config migrate` 或 `hermes setup` 期间提示）：

```yaml
skills:
  config:
    wiki:
      path: ~/wiki
```

默认为 `~/wiki`。当此
技能加载时会注入解析的路径 — 检查上方的 `[Skill config: ...]` 块以获取活动值。

wiki 只是一个 Markdown 文件目录 — 在 Obsidian、VS Code 或
任何编辑器中打开它。不需要数据库，不需要特殊工具。

## 架构：三层

```
wiki/
├── SCHEMA.md           # 约定、结构规则、域配置
├── index.md            # 分区内容目录，带有单行摘要
├── log.md              # 按时间顺序的操作日志（仅追加，每年轮换）
├── raw/                # 第 1 层：不可变的源材料
│   ├── articles/       # 网络文章、剪报
│   ├── papers/         # PDF、arxiv 论文
│   ├── transcripts/    # 会议记录、访谈
│   └── assets/         # 源引用的图像、图表
├── entities/           # 第 2 层：实体页面（人物、组织、产品、模型）
├── concepts/           # 第 2 层：概念/主题页面
├── comparisons/        # 第 2 层：并排分析
└── queries/            # 第 2 层：值得保留的归档查询结果
```

**第 1 层 — 原始源：** 不可变。代理读取但从不修改这些。
**第 2 层 — Wiki：** 代理拥有的 Markdown 文件。由代理创建、更新和
交叉引用。
**第 3 层 — 模式：** `SCHEMA.md` 定义结构、约定和标签分类法。

## 恢复现有 Wiki（关键 — 每次会话都要这样做）

当用户拥有现有 wiki 时，**在做任何事情之前始终先定位自己**：

① **读取 `SCHEMA.md`** — 了解域、约定和标签分类法。
② **读取 `index.md`** — 了解存在哪些页面及其摘要。
③ **扫描最近的 `log.md`** — 阅读最后 20-30 条条目以了解最近的活动。

```bash
WIKI="${wiki_path:-$HOME/wiki}"
# 会话开始时的定位读取
read_file "$WIKI/SCHEMA.md"
read_file "$WIKI/index.md"
read_file "$WIKI/log.md" offset=<last 30 lines>
```

只有在定位后才能摄取、查询或检查。这可以防止：
- 为已存在的实体创建重复页面
- 错过对现有内容的交叉引用
- 与模式约定相矛盾
- 重复已经记录的工作

对于大型 wiki（100+ 页面），在创建任何新内容之前，也应对相关主题运行快速 `search_files`。

## 初始化新 Wiki

当用户要求创建或启动 wiki 时：

1. 确定 wiki 路径（从配置、环境变量或询问用户；默认为 `~/wiki`）
2. 创建上述目录结构
3. 询问用户 wiki 覆盖什么域 — 要具体
4. 编写针对该域的 `SCHEMA.md`（见下面的模板）
5. 编写带有分区标题的初始 `index.md`
6. 编写带有创建条目的初始 `log.md`
7. 确认 wiki 已准备就绪并建议首先摄取的来源

### SCHEMA.md 模板

适应用户的域。模式约束代理行为并确保一致性：

```markdown
# Wiki Schema

## Domain
[此 wiki 覆盖的内容 — 例如，"AI/ML 研究"、"个人健康"、"创业情报"]

## Conventions
- 文件名：小写，连字符，无空格（例如，`transformer-architecture.md`）
- 每个 wiki 页面以 YAML frontmatter 开始（见下文）
- 使用 `[[wikilinks]]` 在页面之间链接（每页至少 2 个出站链接）
- 更新页面时，始终更新 `updated` 日期
- 每个新页面必须添加到 `index.md` 的正确部分
- 每个操作必须附加到 `log.md`

## Frontmatter
  ```yaml
  ---
title: Page Title
created: YYYY-MM-DD
updated: YYYY-MM-DD
type: entity | concept | comparison | query | summary
tags: [from taxonomy below]
sources: [raw/articles/source-name.md]
  ---
  ```

## Tag Taxonomy
[定义 10-20 个域的顶级标签。在此之前添加新标签。]

AI/ML 示例：
- Models: model, architecture, benchmark, training
- People/Orgs: person, company, lab, open-source
- Techniques: optimization, fine-tuning, inference, alignment, data
- Meta: comparison, timeline, controversy, prediction

规则：页面上的每个标签必须出现在此分类法中。如果需要新标签，
先在此处添加，然后使用它。这可以防止标签蔓延。

## Page Thresholds
- **创建页面** 当实体/概念出现在 2+ 个来源中或对一个来源至关重要时
- **添加到现有页面** 当来源提及已经涵盖的内容时
- **不要创建页面** 对于传递性提及、次要细节或域外内容
- **拆分页面** 当页面超过 ~200 行时 — 拆分为带有交叉链接的子主题
- **归档页面** 当内容完全被取代时 — 移至 `_archive/`，从索引中删除

## Entity Pages
每个值得注意的实体一页。包括：
- 概述 / 它是什么
- 关键事实和日期
- 与其他实体的关系（[[wikilinks]]）
- 来源引用

## Concept Pages
每个概念或主题一页。包括：
- 定义 / 解释
- 知识的当前状态
- 开放问题或辩论
- 相关概念（[[wikilinks]]）

## Comparison Pages
并排分析。包括：
- 比较的内容及其原因
- 比较维度（首选表格格式）
- 结论或综合
- 来源

## Update Policy
当新信息与现有内容冲突时：
1. 检查日期 — 较新的来源通常取代较旧的来源
2. 如果确实存在矛盾，记录两种立场及其日期和来源
3. 在 frontmatter 中标记矛盾：`contradictions: [page-name]`
4. 在检查报告中标记以供用户审查
```

### index.md 模板

索引按类型分区。每个条目一行：wikilink + 摘要。

```markdown
# Wiki Index

> Content catalog. Every wiki page listed under its type with a one-line summary.
> Read this first to find relevant pages for any query.
> Last updated: YYYY-MM-DD | Total pages: N

## Entities
<!-- Alphabetical within section -->

## Concepts

## Comparisons

## Queries
```

**扩展规则：** 当任何部分超过 50 个条目时，按首字母或子域将其拆分为子部分。当索引总条目超过 200 个时，创建 `_meta/topic-map.md`，按主题分组页面以加快导航。

### log.md 模板

```markdown
# Wiki Log

> Chronological record of all wiki actions. Append-only.
> Format: `## [YYYY-MM-DD] action | subject`
> Actions: ingest, update, query, lint, create, archive, delete
> When this file exceeds 500 entries, rotate: rename to log-YYYY.md, start fresh.

## [YYYY-MM-DD] create | Wiki initialized
- Domain: [domain]
- Structure created with SCHEMA.md, index.md, log.md
```

## 核心操作

### 1. 摄取

当用户提供来源（URL、文件、粘贴）时，将其集成到 wiki 中：

① **捕获原始来源：**
   - URL → 使用 `web_extract` 获取 Markdown，保存到 `raw/articles/`
   - PDF → 使用 `web_extract`（处理 PDF），保存到 `raw/papers/`
   - 粘贴文本 → 保存到适当的 `raw/` 子目录
   - 给文件起描述性名称：`raw/articles/karpathy-llm-wiki-2026.md`

② **与用户讨论要点** — 什么有趣，对
   域有什么重要性。（在自动/cron 上下文中跳过此步骤 — 直接继续。）

③ **检查已存在的内容** — 搜索 index.md 并使用 `search_files` 查找
   提到的实体/概念的现有页面。这是
   成长中的 wiki 和一堆重复内容之间的区别。

④ **编写或更新 wiki 页面：**
   - **新实体/概念：** 仅当它们满足 SCHEMA.md 中的页面阈值时创建页面
     （2+ 个来源提及，或对一个来源至关重要）
   - **现有页面：** 添加新信息，更新事实，更新 `updated` 日期。
     当新信息与现有内容冲突时，遵循更新策略。
   - **交叉引用：** 每个新或更新的页面必须通过 `[[wikilinks]]` 链接到至少 2 个其他
     页面。检查现有页面是否链接回来。
   - **标签：** 仅使用 SCHEMA.md 分类法中的标签

⑤ **更新导航：**
   - 将新页面按字母顺序添加到 `index.md` 的正确部分
   - 更新索引标题中的 "Total pages" 计数和 "Last updated" 日期
   - 附加到 `log.md`：`## [YYYY-MM-DD] ingest | Source Title`
   - 在日志条目中列出创建或更新的每个文件

⑥ **报告更改** — 向用户列出创建或更新的每个文件。

单个来源可以触发 5-15 个 wiki 页面的更新。这是正常的
并且是期望的 — 这是复合效应。

### 2. 查询

当用户询问关于 wiki 域的问题时：

① **读取 `index.md`** 以识别相关页面。
② **对于有 100+ 页面的 wiki**，也对所有 `.md` 文件进行 `search_files`
   关键词 — 仅索引可能会错过相关内容。
③ **使用 `read_file` 读取相关页面**。
④ **从编译的知识中综合答案**。引用您从中获取的 wiki 页面
   ："基于 [[page-a]] 和 [[page-b]]..."
⑤ **将有价值的答案归档** — 如果答案是实质性比较、
   深入探讨或新颖综合，在 `queries/` 或 `comparisons/` 中创建页面。
   不要归档琐碎的查找 — 只归档重新推导会很痛苦的答案。
⑥ **更新 log.md** 与查询以及它是否被归档。

### 3. 检查

当用户要求检查、健康检查或审计 wiki 时：

① **孤立页面：** 查找没有来自其他页面的入站 `[[wikilinks]]` 的页面。
```python
# 使用 execute_code 进行此操作 — 对所有 wiki 页面进行程序化扫描
import os, re
from collections import defaultdict
wiki = "<WIKI_PATH>"
# 扫描 entities/、concepts/、comparisons/、queries/ 中的所有 .md 文件
# 提取所有 [[wikilinks]] — 构建入站链接映射
# 入站链接为零的页面是孤立页面
```

② **损坏的 wikilinks：** 查找指向不存在页面的 `[[links]]`。

③ **索引完整性：** 每个 wiki 页面都应出现在 `index.md` 中。比较
   文件系统与索引条目。

④ **Frontmatter 验证：** 每个 wiki 页面必须具有所有必填字段
   （title, created, updated, type, tags, sources）。标签必须在分类法中。

⑤ **过时内容：** `updated` 日期比最近的
   提及相同实体的来源早 >90 天的页面。

⑥ **矛盾：** 同一主题的页面有冲突的声明。寻找
   共享标签/实体但陈述不同事实的页面。

⑦ **页面大小：** 标记超过 200 行的页面 — 拆分候选。

⑧ **标签审计：** 列出所有使用的标签，标记任何不在 SCHEMA.md 分类法中的标签。

⑨ **日志轮换：** 如果 log.md 超过 500 个条目，将其轮换。

⑩ **报告发现** 带有特定文件路径和建议操作，按
   严重程度分组（损坏的链接 > 孤立页面 > 过时内容 > 样式问题）。

⑪ **附加到 log.md：** `## [YYYY-MM-DD] lint | N issues found`

## 使用 Wiki

### 搜索

```bash
# 按内容查找页面
search_files "transformer" path="$WIKI" file_glob="*.md"

# 按文件名查找页面
search_files "*.md" target="files" path="$WIKI"

# 按标签查找页面
search_files "tags:.*alignment" path="$WIKI" file_glob="*.md"

# 最近活动
read_file "$WIKI/log.md" offset=<last 20 lines>
```

### 批量摄取

当一次摄取多个来源时，批量更新：
1. 首先阅读所有来源
2. 识别所有来源中的所有实体和概念
3. 检查所有这些的现有页面（一次搜索，不是 N 次）
4. 一次更新创建/更新页面（避免冗余更新）
5. 最后一次更新 index.md
6. 编写涵盖批次的单个日志条目

### 归档

当内容完全被取代或域范围更改时：
1. 如果不存在，创建 `_archive/` 目录
2. 将页面移动到 `_archive/` 及其原始路径（例如，`_archive/entities/old-page.md`）
3. 从 `index.md` 中删除
4. 更新任何链接到它的页面 — 将 wikilink 替换为纯文本 + "(archived)"
5. 记录归档操作

### Obsidian 集成

wiki 目录可以直接作为 Obsidian 仓库使用：
- `[[wikilinks]]` 渲染为可点击链接
- 图形视图可视化知识网络
- YAML frontmatter 为 Dataview 查询提供支持
- `raw/assets/` 文件夹保存通过 `![[image.png]]` 引用的图像

最佳效果：
- 将 Obsidian 的附件文件夹设置为 `raw/assets/`
- 在 Obsidian 设置中启用 "Wikilinks"（通常默认启用）
- 安装 Dataview 插件以进行查询，如 `TABLE tags FROM "entities" WHERE contains(tags, "company")`

如果与此技能一起使用 Obsidian 技能，请将 `OBSIDIAN_VAULT_PATH` 设置为
与 wiki 路径相同的目录。

### Obsidian 无头（服务器和无头机器）

在没有显示的机器上，使用 `obsidian-headless` 而不是桌面应用。
它通过 Obsidian Sync 同步仓库，无需 GUI — 非常适合在
服务器上运行的代理写入 wiki，而 Obsidian 桌面在另一台设备上读取它。

**设置：**
```bash
# 需要 Node.js 22+
npm install -g obsidian-headless

# 登录（需要带有 Sync 订阅的 Obsidian 账户）
ob login --email <email> --password '<password>'

# 为 wiki 创建远程仓库
ob sync-create-remote --name "LLM Wiki"

# 将 wiki 目录连接到仓库
cd ~/wiki
ob sync-setup --vault "<vault-id>"

# 初始同步
ob sync

# 连续同步（前台 — 使用 systemd 后台运行）
ob sync --continuous
```

**通过 systemd 进行连续后台同步：**
```ini
# ~/.config/systemd/user/obsidian-wiki-sync.service
[Unit]
Description=Obsidian LLM Wiki Sync
After=network-online.target
Wants=network-online.target

[Service]
ExecStart=/path/to/ob sync --continuous
WorkingDirectory=/home/user/wiki
Restart=on-failure
RestartSec=10

[Install]
WantedBy=default.target
```

```bash
systemctl --user daemon-reload
systemctl --user enable --now obsidian-wiki-sync
# 启用 linger 以便同步在注销后继续：
sudo loginctl enable-linger $USER
```

这允许代理在服务器上写入 `~/wiki`，而您在笔记本电脑/手机上的 Obsidian 中浏览同一个
仓库 — 更改在几秒钟内出现。

## 陷阱

- **永远不要修改 `raw/` 中的文件** — 来源是不可变的。更正应在 wiki 页面中进行。
- **始终首先定位** — 在新会话中的任何操作之前阅读 SCHEMA + 索引 + 最近的日志。
  跳过此步骤会导致重复和错过的交叉引用。
- **始终更新 index.md 和 log.md** — 跳过此步骤会使 wiki 退化。这些是
  导航主干。
- **不要为传递性提及创建页面** — 遵循 SCHEMA.md 中的页面阈值。一个名称
  在脚注中出现一次不值得创建实体页面。
- **不要创建没有交叉引用的页面** — 孤立页面是不可见的。每个页面必须
  链接到至少 2 个其他页面。
- **Frontmatter 是必需的** — 它启用搜索、过滤和过时检测。
- **标签必须来自分类法** — 自由格式标签会退化为噪音。先将新标签添加到 SCHEMA.md
  ，然后使用它们。
- **保持页面可扫描** — wiki 页面应该在 30 秒内可读。拆分超过
  200 行的页面。将详细分析移至专用的深入页面。
- **在大规模更新前询问** — 如果摄取会触及 10+ 现有页面，请先与用户确认
  范围。
- **轮换日志** — 当 log.md 超过 500 个条目时，将其重命名为 `log-YYYY.md` 并重新开始。
  代理应在检查期间检查日志大小。
- **明确处理矛盾** — 不要静默覆盖。记录带有日期的两种声明，
  在 frontmatter 中标记，标记以供用户审查。
