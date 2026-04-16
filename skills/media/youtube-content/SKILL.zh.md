---
name: youtube-content
description: >
  获取YouTube视频字幕并将其转换为结构化内容
  （章节、摘要、线程、博客文章）。当用户分享YouTube
  URL或视频链接，要求总结视频，请求字幕，或希望
  从任何YouTube视频中提取和重新格式化内容时使用。
---

# YouTube内容工具

从YouTube视频中提取字幕并将其转换为有用的格式。

## 设置

```bash
pip install youtube-transcript-api
```

## 辅助脚本

`SKILL_DIR`是包含此SKILL.md文件的目录。该脚本接受任何标准YouTube URL格式、短链接（youtu.be）、shorts、嵌入、直播链接或原始11字符视频ID。

```bash
# 带元数据的JSON输出
python3 SKILL_DIR/scripts/fetch_transcript.py "https://youtube.com/watch?v=VIDEO_ID"

# 纯文本（适合通过管道进行进一步处理）
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --text-only

# 带时间戳
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --timestamps

# 特定语言，带回退链
python3 SKILL_DIR/scripts/fetch_transcript.py "URL" --language tr,en
```

## 输出格式

获取字幕后，根据用户的要求格式化：

- **章节**：按主题转移分组，输出带时间戳的章节列表
- **摘要**：整个视频的简洁5-10句概述
- **章节摘要**：章节，每个章节有一个简短的段落摘要
- **线程**：Twitter/X线程格式 — 编号帖子，每个不超过280字符
- **博客文章**：完整文章，包含标题、部分和关键要点
- **引用**：带时间戳的显著引用

### 示例 — 章节输出

```
00:00 引言 — 主持人以问题陈述开始
03:45 背景 — 先前的工作以及现有解决方案为何不足
12:20 核心方法 — 所提出方法的详细说明
24:10 结果 — 基准比较和关键要点
31:55 问答 — 观众关于可扩展性和后续步骤的问题
```

## 工作流程

1. **获取**：使用`--text-only --timestamps`选项的辅助脚本获取字幕。
2. **验证**：确认输出非空且为预期语言。如果为空，重试时不使用`--language`以获取任何可用的字幕。如果仍然为空，告诉用户视频可能禁用了字幕。
3. **如果需要，分块**：如果字幕超过~50K字符，将其分割为重叠的块（~40K，2K重叠），并在合并前总结每个块。
4. **转换**：转换为请求的输出格式。如果用户未指定格式，默认为摘要。
5. **验证**：在呈现之前重新读取转换后的输出，检查连贯性、正确的时间戳和完整性。

## 错误处理

- **字幕禁用**：告诉用户；建议他们检查视频页面是否有字幕。
- **私人/不可用视频**：转达错误并要求用户验证URL。
- **无匹配语言**：重试时不使用`--language`以获取任何可用的字幕，然后向用户注明实际语言。
- **缺少依赖**：运行`pip install youtube-transcript-api`并重试。