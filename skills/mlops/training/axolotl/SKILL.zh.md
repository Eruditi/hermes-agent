
---
name: axolotl
description: 使用Axolotl微调LLM的专家指南 - YAML配置、100+模型、LoRA/QLoRA、DPO/KTO/ORPO/GRPO、多模态支持
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [axolotl, torch, transformers, datasets, peft, accelerate, deepspeed]
metadata:
  hermes:
    tags: [微调, Axolotl, LLM, LoRA, QLoRA, DPO, KTO, ORPO, GRPO, YAML, HuggingFace, DeepSpeed, 多模态]

---

# Axolotl 技能

使用Axolotl开发的综合辅助，从官方文档生成。

## 何时使用此技能

此技能应在以下情况下触发：
- 使用axolotl工作
- 询问axolotl功能或API
- 实现axolotl解决方案
- 调试axolotl代码
- 学习axolotl最佳实践

## 快速参考

### 常见模式

**模式1：** 要验证您的训练作业存在可接受的数据传输速度，运行NCCL测试可以帮助定位瓶颈，例如：

```
./build/all_reduce_perf -b 8 -e 128M -f 2 -g 3
```

**模式2：** 在Axolotl yaml中配置您的模型以使用FSDP。例如：

```
fsdp_version: 2
fsdp_config:
  offload_params: true
  state_dict_type: FULL_STATE_DICT
  auto_wrap_policy: TRANSFORMER_BASED_WRAP
  transformer_layer_cls_to_wrap: LlamaDecoderLayer
  reshard_after_forward: true
```

**模式3：** context_parallel_size应该是GPU总数的除数。例如：

```
context_parallel_size
```

**模式4：** 例如：- 使用8个GPU且无序列并行：每步处理8个不同的批次 - 使用8个GPU且context_parallel_size=4：每步仅处理2个不同的批次（每个在4个GPU上拆分）- 如果您的每个GPU micro_batch_size为2，则全局批大小从16减少到4

```
context_parallel_size=4
```

**模式5：** 在配置中设置save_compressed: true可以启用以压缩格式保存模型，这：- 减少约40%的磁盘空间使用 - 保持与vLLM的兼容性以进行加速推理 - 保持与llmcompressor的兼容性以进行进一步优化（例如：量化）

```
save_compressed: true
```

**模式6：** 注意，没有必要将您的集成放在integrations文件夹中。它可以在任何位置，只要它安装在您的python环境中的包中。请参阅此仓库作为示例：https://github.com/axolotl-ai-cloud/diff-transformer

```
integrations
```

**模式7：** 处理单个示例和批量数据。- 单个示例：sample['input_ids']是list[int] - 批量数据：sample['input_ids']是list[list[int]]

```
utils.trainer.drop_long_seq(sample, sequence_len=2048, min_sequence_len=2)
```

### 示例代码模式

**示例1**（python）：
```python
cli.cloud.modal_.ModalCloud(config, app=None)
```

**示例2**（python）：
```python
cli.cloud.modal_.run_cmd(cmd, run_folder, volumes=None)
```

**示例3**（python）：
```python
core.trainers.base.AxolotlTrainer(
    *_args,
    bench_data_collator=None,
    eval_data_collator=None,
    dataset_tags=None,
    **kwargs,
)
```

**示例4**（python）：
```python
core.trainers.base.AxolotlTrainer.log(logs, start_time=None)
```

**示例5**（python）：
```python
prompt_strategies.input_output.RawInputOutputPrompter()
```

## 参考文件

此技能在`references/`中包含综合文档：

- **api.md** - Api文档
- **dataset-formats.md** - 数据集格式文档
- **other.md** - 其他文档

当需要详细信息时，使用`view`读取特定参考文件。

## 使用此技能

### 对于初学者
从入门或教程参考文件开始学习基础概念。

### 对于特定功能
使用适当的类别参考文件（api、指南等）获取详细信息。

### 对于代码示例
上面的快速参考部分包含从官方文档中提取的常见模式。

## 资源

### references/
从官方来源提取的有组织文档。这些文件包含：
- 详细解释
- 带语言注释的代码示例
- 指向原始文档的链接
- 用于快速导航的目录

### scripts/
在此处添加用于常见自动化任务的辅助脚本。

### assets/
在此处添加模板、样板或示例项目。

## 注意事项

- 此技能是从官方文档自动生成的
- 参考文件保留了源文档的结构和示例
- 代码示例包括语言检测以获得更好的语法高亮
- 快速参考模式是从文档中的常见使用示例中提取的

## 更新

要使用更新的文档刷新此技能：
1. 使用相同的配置重新运行抓取器
2. 技能将使用最新信息重建
