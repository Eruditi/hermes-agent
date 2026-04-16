---
name: huggingface-hub
description: Hugging Face Hub CLI (hf) — 搜索、下载和上传模型和数据集，管理存储库，用SQL查询数据集，部署推理端点，管理Spaces和存储桶。
version: 1.0.0
author: Hugging Face
license: MIT
tags: [huggingface, hf, models, datasets, hub, mlops]
---

# Hugging Face CLI (`hf`) 参考指南

`hf`命令是与Hugging Face Hub交互的现代命令行界面，提供管理存储库、模型、数据集和Spaces的工具。

> **重要：** `hf`命令取代了现已弃用的`huggingface-cli`命令。

## 快速开始
*   **安装：** `curl -LsSf https://hf.co/cli/install.sh | bash -s`
*   **帮助：** 使用`hf --help`查看所有可用功能和真实世界示例。
*   **认证：** 推荐通过`HF_TOKEN`环境变量或`--token`标志。

---

## 核心命令

### 一般操作
*   `hf download REPO_ID`：从Hub下载文件。
*   `hf upload REPO_ID`：上传文件/文件夹（推荐用于单次提交）。
*   `hf upload-large-folder REPO_ID LOCAL_PATH`：推荐用于大型目录的可恢复上传。
*   `hf sync`：在本地目录和存储桶之间同步文件。
*   `hf env` / `hf version`：查看环境和版本详情。

### 认证 (`hf auth`)
*   `login` / `logout`：使用[huggingface.co/settings/tokens](https://huggingface.co/settings/tokens)的令牌管理会话。
*   `list` / `switch`：管理和在多个存储的访问令牌之间切换。
*   `whoami`：识别当前登录的账户。

### 存储库管理 (`hf repos`)
*   `create` / `delete`：创建或永久删除存储库。
*   `duplicate`：将模型、数据集或Space克隆到新ID。
*   `move`：在命名空间之间转移存储库。
*   `branch` / `tag`：管理Git类引用。
*   `delete-files`：使用模式删除特定文件。

---

## 专门的Hub交互

### 数据集和模型
*   **数据集：** `hf datasets list`、`info`和`parquet`（列出parquet URL）。
*   **SQL查询：** `hf datasets sql SQL` — 通过DuckDB对数据集parquet URL执行原始SQL。
*   **模型：** `hf models list`和`info`。
*   **论文：** `hf papers list` — 查看每日论文。

### 讨论和拉取请求 (`hf discussions`)
*   管理Hub贡献的生命周期：`list`、`create`、`info`、`comment`、`close`、`reopen`和`rename`。
*   `diff`：查看PR中的更改。
*   `merge`：完成拉取请求。

### 基础设施和计算
*   **端点：** 部署和管理推理端点（`deploy`、`pause`、`resume`、`scale-to-zero`、`catalog`）。
*   **作业：** 在HF基础设施上运行计算任务。包括`hf jobs uv`用于运行带有内联依赖的Python脚本，以及`stats`用于资源监控。
*   **Spaces：** 管理交互式应用。包括`dev-mode`和`hot-reload`，用于Python文件的无需完全重启的热重载。

### 存储和自动化
*   **存储桶：** 完整的S3类存储桶管理（`create`、`cp`、`mv`、`rm`、`sync`）。
*   **缓存：** 使用`list`、`prune`（移除分离的修订）和`verify`（校验和检查）管理本地存储。
*   **Webhooks：** 通过管理Hub webhooks（`create`、`watch`、`enable`/`disable`）自动化工作流。
*   **集合：** 将Hub项目组织到集合中（`add-item`、`update`、`list`）。

---

## 高级用法和提示

### 全局标志
*   `--format json`：生成用于自动化的机器可读输出。
*   `-q` / `--quiet`：将输出限制为仅ID。

### 扩展和技能
*   **扩展：** 通过`hf extensions install REPO_ID`使用GitHub存储库扩展CLI功能。
*   **技能：** 使用`hf skills add`管理AI助手技能。