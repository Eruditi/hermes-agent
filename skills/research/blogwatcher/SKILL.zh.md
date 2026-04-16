---
name: blogwatcher
description: 使用blogwatcher-cli工具监控博客和RSS/Atom源的更新。添加博客、扫描新文章、跟踪阅读状态，并按类别过滤。
version: 2.0.0
author: JulienTant（Hyaxia/blogwatcher的分支）
license: MIT
metadata:
  hermes:
    tags: [RSS, 博客, 源阅读器, 监控]
    homepage: https://github.com/JulienTant/blogwatcher-cli
prerequisites:
  commands: [blogwatcher-cli]
---

# Blogwatcher

使用`blogwatcher-cli`工具跟踪博客和RSS/Atom源更新。支持自动源发现、HTML抓取回退、OPML导入和已读/未读文章管理。

## 安装

选择一种方法：

- **Go：** `go install github.com/JulienTant/blogwatcher-cli/cmd/blogwatcher-cli@latest`
- **Docker：** `docker run --rm -v blogwatcher-cli:/data ghcr.io/julientant/blogwatcher-cli`
- **二进制（Linux amd64）：** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
- **二进制（Linux arm64）：** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_linux_arm64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
- **二进制（macOS Apple Silicon）：** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_darwin_arm64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`
- **二进制（macOS Intel）：** `curl -sL https://github.com/JulienTant/blogwatcher-cli/releases/latest/download/blogwatcher-cli_darwin_amd64.tar.gz | tar xz -C /usr/local/bin blogwatcher-cli`

所有发布：https://github.com/JulienTant/blogwatcher-cli/releases

### 具有持久存储的Docker

默认情况下，数据库位于`~/.blogwatcher-cli/blogwatcher-cli.db`。在Docker中，这在容器重启时会丢失。使用`BLOGWATCHER_DB`或卷挂载来持久化它：

```bash
# 命名卷（最简单）
docker run --rm -v blogwatcher-cli:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan

# 主机绑定挂载
docker run --rm -v /path/on/host:/data -e BLOGWATCHER_DB=/data/blogwatcher-cli.db ghcr.io/julientant/blogwatcher-cli scan
```

### 从原始blogwatcher迁移

如果从`Hyaxia/blogwatcher`升级，请移动您的数据库：

```bash
mv ~/.blogwatcher/blogwatcher.db ~/.blogwatcher-cli/blogwatcher-cli.db
```

二进制名称从`blogwatcher`更改为`blogwatcher-cli`。

## 常用命令

### 管理博客

- 添加博客：`blogwatcher-cli add "我的博客" https://example.com`
- 使用显式源添加：`blogwatcher-cli add "我的博客" https://example.com --feed-url https://example.com/feed.xml`
- 使用HTML抓取添加：`blogwatcher-cli add "我的博客" https://example.com --scrape-selector "article h2 a"`
- 列出跟踪的博客：`blogwatcher-cli blogs`
- 删除博客：`blogwatcher-cli remove "我的博客" --yes`
- 从OPML导入：`blogwatcher-cli import subscriptions.opml`

### 扫描和阅读

- 扫描所有博客：`blogwatcher-cli scan`
- 扫描一个博客：`blogwatcher-cli scan "我的博客"`
- 列出未读文章：`blogwatcher-cli articles`
- 列出所有文章：`blogwatcher-cli articles --all`
- 按博客过滤：`blogwatcher-cli articles --blog "我的博客"`
- 按类别过滤：`blogwatcher-cli articles --category "工程"`
- 标记文章已读：`blogwatcher-cli read 1`
- 标记文章未读：`blogwatcher-cli unread 1`
- 标记全部已读：`blogwatcher-cli read-all`
- 标记博客的全部已读：`blogwatcher-cli read-all --blog "我的博客" --yes`

## 环境变量

所有标志都可以通过带有`BLOGWATCHER_`前缀的环境变量设置：

| 变量 | 描述 |
|---|---|
| `BLOGWATCHER_DB` | SQLite数据库文件的路径 |
| `BLOGWATCHER_WORKERS` | 并发扫描工作器的数量（默认：8） |
| `BLOGWATCHER_SILENT` | 扫描时仅输出"扫描完成" |
| `BLOGWATCHER_YES` | 跳过确认提示 |
| `BLOGWATCHER_CATEGORY` | 按类别过滤文章的默认值 |

## 示例输出

```
$ blogwatcher-cli blogs
跟踪的博客（1）：

  xkcd
    URL：https://xkcd.com
    源：https://xkcd.com/atom.xml
    上次扫描：2026-04-03 10:30
```

```
$ blogwatcher-cli scan
扫描1个博客...

  xkcd
    来源：RSS | 找到：4 | 新：4

总共找到4篇新文章！
```

```
$ blogwatcher-cli articles
未读文章（2）：

  [1] [新] 桶 - 第13部分
       博客：xkcd
       URL：https://xkcd.com/3095/
       发布：2026-04-02
       类别：漫画、科学

  [2] [新] 火山事实
       博客：xkcd
       URL：https://xkcd.com/3094/
       发布：2026-04-01
       类别：漫画
```

## 备注

- 当未提供`--feed-url`时，自动从博客主页发现RSS/Atom源。
- 如果RSS失败并且配置了`--scrape-selector`，则回退到HTML抓取。
- 存储来自RSS/Atom源的类别并可用于过滤文章。
- 从Feedly、Inoreader、NewsBlur等导出的OPML文件批量导入博客。
- 默认情况下，数据库存储在`~/.blogwatcher-cli/blogwatcher-cli.db`（使用`--db`或`BLOGWATCHER_DB`覆盖）。
- 使用`blogwatcher-cli <command> --help`发现所有标志和选项。
