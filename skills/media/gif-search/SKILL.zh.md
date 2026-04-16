---
name: gif-search
description: 使用curl从Tenor搜索和下载GIF。除了curl和jq之外没有依赖项。用于查找反应GIF、创建视觉内容以及在聊天中发送GIF。
version: 1.1.0
author: Hermes Agent
license: MIT
prerequisites:
  env_vars: [TENOR_API_KEY]
  commands: [curl, jq]
metadata:
  hermes:
    tags: [GIF, 媒体, 搜索, Tenor, API]
---

# GIF搜索（Tenor API）

使用curl直接通过Tenor API搜索和下载GIF。不需要额外的工具。

## 设置

在您的环境中设置Tenor API密钥（添加到`~/.hermes/.env`）：

```bash
TENOR_API_KEY=your_key_here
```

在https://developers.google.com/tenor/guides/quickstart获取免费API密钥 — Google Cloud Console Tenor API密钥是免费的，并且有慷慨的速率限制。

## 先决条件

- `curl`和`jq`（两者在macOS/Linux上都是标准的）
- `TENOR_API_KEY`环境变量

## 搜索GIF

```bash
# 搜索并获取GIF URL
curl -s "https://tenor.googleapis.com/v2/search?q=thumbs+up&limit=5&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.gif.url'

# 获取较小/预览版本
curl -s "https://tenor.googleapis.com/v2/search?q=nice+work&limit=3&key=${TENOR_API_KEY}" | jq -r '.results[].media_formats.tinygif.url'
```

## 下载GIF

```bash
# 搜索并下载顶部结果
URL=$(curl -s "https://tenor.googleapis.com/v2/search?q=celebration&limit=1&key=${TENOR_API_KEY}" | jq -r '.results[0].media_formats.gif.url')
curl -sL "$URL" -o celebration.gif
```

## 获取完整元数据

```bash
curl -s "https://tenor.googleapis.com/v2/search?q=cat&limit=3&key=${TENOR_API_KEY}" | jq '.results[] | {title: .title, url: .media_formats.gif.url, preview: .media_formats.tinygif.url, dimensions: .media_formats.gif.dims}'
```

## API参数

| 参数 | 描述 |
|-----------|-------------|
| `q` | 搜索查询（将空格URL编码为`+`） |
| `limit` | 最大结果数（1-50，默认20） |
| `key` | API密钥（来自`$TENOR_API_KEY`环境变量） |
| `media_filter` | 过滤格式：`gif`、`tinygif`、`mp4`、`tinymp4`、`webm` |
| `contentfilter` | 安全性：`off`、`low`、`medium`、`high` |
| `locale` | 语言：`en_US`、`es`、`fr`等 |

## 可用的媒体格式

每个结果在`.media_formats`下都有多种格式：

| 格式 | 用例 |
|--------|----------|
| `gif` | 全质量GIF |
| `tinygif` | 小预览GIF |
| `mp4` | 视频版本（文件大小更小） |
| `tinymp4` | 小预览视频 |
| `webm` | WebM视频 |
| `nanogif` | 微小缩略图 |

## 备注

- URL编码查询：空格为`+`，特殊字符为`%XX`
- 对于在聊天中发送，`tinygif` URL更轻量
- GIF URL可以直接在markdown中使用：`![alt](url)`
