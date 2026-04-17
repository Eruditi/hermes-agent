---
name: unsloth
description: 使用Unsloth进行快速微调的专家指导 - 2-5倍更快的训练，50-80%更少的内存，LoRA/QLoRA优化
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [unsloth, torch, transformers, trl, datasets, peft]
metadata:
  hermes:
    tags: [微调, Unsloth, 快速训练, LoRA, QLoRA, 内存高效, 优化, Llama, Mistral, Gemma, Qwen]

---

# Unsloth 技能

使用unsloth开发的全面帮助，从官方文档生成。

## 何时使用此技能

当出现以下情况时应触发此技能：
- 正在使用unsloth
- 询问unsloth功能或API
- 实现unsloth解决方案
- 调试unsloth代码
- 学习unsloth最佳实践

## 快速参考

### 常见模式

*快速参考模式将在您使用技能时添加。*

## 参考文件

此技能在`references/`中包含全面的文档：

- **llms-txt.md** - Llms-Txt文档

当需要详细信息时，使用`view`读取特定的参考文件。

## 使用此技能

### 对于初学者
从getting_started或tutorials参考文件开始，了解基础概念。

### 对于特定功能
使用适当的类别参考文件（api、guides等）获取详细信息。

### 对于代码示例
上面的快速参考部分包含从官方文档中提取的常见模式。

## 资源

### references/
从官方来源提取的有组织文档。这些文件包含：
- 详细说明
- 带有语言注释的代码示例
- 原始文档的链接
- 用于快速导航的目录

### scripts/
在此处添加用于常见自动化任务的辅助脚本。

### assets/
在此处添加模板、样板或示例项目。

## 注意

- 此技能是从官方文档自动生成的
- 参考文件保留了源文档的结构和示例
- 代码示例包括语言检测以获得更好的语法高亮
- 快速参考模式是从文档中的常见使用示例中提取的

## 更新

要使用更新的文档刷新此技能：
1. 使用相同的配置重新运行爬虫
2. 技能将使用最新信息重建

<!-- 触发重新上传 1763621536 -->
