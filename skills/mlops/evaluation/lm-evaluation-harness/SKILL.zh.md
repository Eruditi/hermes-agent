
---
name: evaluating-llms-harness
description: 在60多个学术基准上评估LLM（MMLU、HumanEval、GSM8K、TruthfulQA、HellaSwag）。用于基准测试模型质量、比较模型、报告学术结果或跟踪训练进度。EleutherAI、HuggingFace和主要实验室使用的行业标准。支持HuggingFace、vLLM和API。
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [lm-eval, transformers, vllm]
metadata:
  hermes:
    tags: [评估, LM评估框架, 基准测试, MMLU, HumanEval, GSM8K, EleutherAI, 模型质量, 学术基准, 行业标准]

---

# lm-evaluation-harness - LLM基准测试

## 快速开始

lm-evaluation-harness使用标准化的提示和指标在60多个学术基准上评估LLM。

**安装**:
```bash
pip install lm-eval
```

**评估任何HuggingFace模型**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag \
  --device cuda:0 \
  --batch_size 8
```

**查看可用任务**:
```bash
lm_eval --tasks list
```

## 常用工作流程

### 工作流程1：标准基准评估

在核心基准（MMLU、GSM8K、HumanEval）上评估模型。

复制此清单：

```
基准评估：
- [ ] 步骤1：选择基准套件
- [ ] 步骤2：配置模型
- [ ] 步骤3：运行评估
- [ ] 步骤4：分析结果
```

**步骤1：选择基准套件**

**核心推理基准**：
- **MMLU**（大规模多任务语言理解）- 57个主题，多项选择
- **GSM8K** - 小学数学应用题
- **HellaSwag** - 常识推理
- **TruthfulQA** - 真实性和事实性
- **ARC**（AI2推理挑战）- 科学问题

**代码基准**：
- **HumanEval** - Python代码生成（164个问题）
- **MBPP**（主要基础Python问题）- Python编码

**标准套件**（推荐用于模型发布）：
```bash
--tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge
```

**步骤2：配置模型**

**HuggingFace模型**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,dtype=bfloat16 \
  --tasks mmlu \
  --device cuda:0 \
  --batch_size auto  # 自动检测最佳批大小
```

**量化模型（4位/8位）**:
```bash
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,load_in_4bit=True \
  --tasks mmlu \
  --device cuda:0
```

**自定义检查点**:
```bash
lm_eval --model hf \
  --model_args pretrained=/path/to/my-model,tokenizer=/path/to/tokenizer \
  --tasks mmlu \
  --device cuda:0
```

**步骤3：运行评估**

```bash
# 完整MMLU评估（57个主题）
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu \
  --num_fewshot 5 \  # 5次评估（标准）
  --batch_size 8 \
  --output_path results/ \
  --log_samples  # 保存单个预测

# 同时运行多个基准
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu,gsm8k,hellaswag,truthfulqa,arc_challenge \
  --num_fewshot 5 \
  --batch_size 8 \
  --output_path results/llama2-7b-eval.json
```

**步骤4：分析结果**

保存到 `results/llama2-7b-eval.json` 的结果：

```json
{
  "results": {
    "mmlu": {
      "acc": 0.459,
      "acc_stderr": 0.004
    },
    "gsm8k": {
      "exact_match": 0.142,
      "exact_match_stderr": 0.006
    },
    "hellaswag": {
      "acc_norm": 0.765,
      "acc_norm_stderr": 0.004
    }
  },
  "config": {
    "model": "hf",
    "model_args": "pretrained=meta-llama/Llama-2-7b-hf",
    "num_fewshot": 5
  }
}
```

### 工作流程2：跟踪训练进度

在训练期间评估检查点。

```
训练进度跟踪：
- [ ] 步骤1：设置定期评估
- [ ] 步骤2：选择快速基准
- [ ] 步骤3：自动化评估
- [ ] 步骤4：绘制学习曲线
```

**步骤1：设置定期评估**

每N个训练步骤评估一次：

```bash
#!/bin/bash
# eval_checkpoint.sh

CHECKPOINT_DIR=$1
STEP=$2

lm_eval --model hf \
  --model_args pretrained=$CHECKPOINT_DIR/checkpoint-$STEP \
  --tasks gsm8k,hellaswag \
  --num_fewshot 0 \  # 0次用于速度
  --batch_size 16 \
  --output_path results/step-$STEP.json
```

**步骤2：选择快速基准**

用于频繁评估的快速基准：
- **HellaSwag**: 1个GPU上约10分钟
- **GSM8K**: 约5分钟
- **PIQA**: 约2分钟

避免用于频繁评估（太慢）：
- **MMLU**: 约2小时（57个主题）
- **HumanEval**: 需要代码执行

**步骤3：自动化评估**

与训练脚本集成：

```python
# 在训练循环中
if step % eval_interval == 0:
    model.save_pretrained(f"checkpoints/step-{step}")

    # 运行评估
    os.system(f"./eval_checkpoint.sh checkpoints step-{step}")
```

或者使用PyTorch Lightning回调：

```python
from pytorch_lightning import Callback

class EvalHarnessCallback(Callback):
    def on_validation_epoch_end(self, trainer, pl_module):
        step = trainer.global_step
        checkpoint_path = f"checkpoints/step-{step}"

        # 保存检查点
        trainer.save_checkpoint(checkpoint_path)

        # 运行lm-eval
        os.system(f"lm_eval --model hf --model_args pretrained={checkpoint_path} ...")
```

**步骤4：绘制学习曲线**

```python
import json
import matplotlib.pyplot as plt

# 加载所有结果
steps = []
mmlu_scores = []

for file in sorted(glob.glob("results/step-*.json")):
    with open(file) as f:
        data = json.load(f)
        step = int(file.split("-")[1].split(".")[0])
        steps.append(step)
        mmlu_scores.append(data["results"]["mmlu"]["acc"])

# 绘制
plt.plot(steps, mmlu_scores)
plt.xlabel("训练步骤")
plt.ylabel("MMLU准确率")
plt.title("训练进度")
plt.savefig("training_curve.png")
```

### 工作流程3：比较多个模型

用于模型比较的基准套件。

```
模型比较：
- [ ] 步骤1：定义模型列表
- [ ] 步骤2：运行评估
- [ ] 步骤3：生成比较表
```

**步骤1：定义模型列表**

```bash
# models.txt
meta-llama/Llama-2-7b-hf
meta-llama/Llama-2-13b-hf
mistralai/Mistral-7B-v0.1
microsoft/phi-2
```

**步骤2：运行评估**

```bash
#!/bin/bash
# eval_all_models.sh

TASKS="mmlu,gsm8k,hellaswag,truthfulqa"

while read model; do
    echo "正在评估 $model"

    # 提取模型名称用于输出文件
    model_name=$(echo $model | sed 's/\//-/g')

    lm_eval --model hf \
      --model_args pretrained=$model,dtype=bfloat16 \
      --tasks $TASKS \
      --num_fewshot 5 \
      --batch_size auto \
      --output_path results/$model_name.json

done &lt; models.txt
```

**步骤3：生成比较表**

```python
import json
import pandas as pd

models = [
    "meta-llama-Llama-2-7b-hf",
    "meta-llama-Llama-2-13b-hf",
    "mistralai-Mistral-7B-v0.1",
    "microsoft-phi-2"
]

tasks = ["mmlu", "gsm8k", "hellaswag", "truthfulqa"]

results = []
for model in models:
    with open(f"results/{model}.json") as f:
        data = json.load(f)
        row = {"Model": model.replace("-", "/")}
        for task in tasks:
            # 获取每个任务的主要指标
            metrics = data["results"][task]
            if "acc" in metrics:
                row[task.upper()] = f"{metrics['acc']:.3f}"
            elif "exact_match" in metrics:
                row[task.upper()] = f"{metrics['exact_match']:.3f}"
        results.append(row)

df = pd.DataFrame(results)
print(df.to_markdown(index=False))
```

输出：
```
| Model                  | MMLU  | GSM8K | HELLASWAG | TRUTHFULQA |
|------------------------|-------|-------|-----------|------------|
| meta-llama/Llama-2-7b  | 0.459 | 0.142 | 0.765     | 0.391      |
| meta-llama/Llama-2-13b | 0.549 | 0.287 | 0.801     | 0.430      |
| mistralai/Mistral-7B   | 0.626 | 0.395 | 0.812     | 0.428      |
| microsoft/phi-2        | 0.560 | 0.613 | 0.682     | 0.447      |
```

### 工作流程4：使用vLLM评估（更快的推理）

使用vLLM后端实现5-10倍更快的评估。

```
vLLM评估：
- [ ] 步骤1：安装vLLM
- [ ] 步骤2：配置vLLM后端
- [ ] 步骤3：运行评估
```

**步骤1：安装vLLM**

```bash
pip install vllm
```

**步骤2：配置vLLM后端**

```bash
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=1,dtype=auto,gpu_memory_utilization=0.8 \
  --tasks mmlu \
  --batch_size auto
```

**步骤3：运行评估**

vLLM比标准HuggingFace快5-10倍：

```bash
# 标准HF：7B模型上MMLU约2小时
lm_eval --model hf \
  --model_args pretrained=meta-llama/Llama-2-7b-hf \
  --tasks mmlu \
  --batch_size 8

# vLLM：7B模型上MMLU约15-20分钟
lm_eval --model vllm \
  --model_args pretrained=meta-llama/Llama-2-7b-hf,tensor_parallel_size=2 \
  --tasks mmlu \
  --batch_size auto
```

## 何时使用vs替代方案

**使用lm-evaluation-harness当：**
- 为学术论文基准测试模型
- 在标准任务上比较模型质量
- 跟踪训练进度
- 报告标准化指标（每个人都使用相同的提示）
- 需要可复现的评估

**使用替代方案：**
- **HELM**（斯坦福）：更广泛的评估（公平性、效率、校准）
- **AlpacaEval**：使用LLM评判器的指令遵循评估
- **MT-Bench**：对话式多轮评估
- **自定义脚本**：特定领域评估

## 常见问题

**问题：评估太慢**

使用vLLM后端：
```bash
lm_eval --model vllm \
  --model_args pretrained=model-name,tensor_parallel_size=2
```

或者减少少样本示例：
```bash
--num_fewshot 0  # 而不是5
```

或者评估MMLU的子集：
```bash
--tasks mmlu_stem  # 仅STEM主题
```

**问题：内存不足**

减少批大小：
```bash
--batch_size 1  # 或者 --batch_size auto
```

使用量化：
```bash
--model_args pretrained=model-name,load_in_8bit=True
```

启用CPU卸载：
```bash
--model_args pretrained=model-name,device_map=auto,offload_folder=offload
```

**问题：与报告的结果不同**

检查少样本计数：
```bash
--num_fewshot 5  # 大多数论文使用5-shot
```

检查确切的任务名称：
```bash
--tasks mmlu  # 不是mmlu_direct或mmlu_fewshot
```

验证模型和分词器匹配：
```bash
--model_args pretrained=model-name,tokenizer=same-model-name
```

**问题：HumanEval不执行代码**

安装执行依赖：
```bash
pip install human-eval
```

启用代码执行：
```bash
lm_eval --model hf \
  --model_args pretrained=model-name \
  --tasks humaneval \
  --allow_code_execution  # HumanEval必需
```

## 高级主题

**基准描述**：有关所有60多个任务的详细描述、它们测量的内容以及解释，请参阅 [references/benchmark-guide.md](references/benchmark-guide.md)。

**自定义任务**：有关创建特定领域评估任务，请参阅 [references/custom-tasks.md](references/custom-tasks.md)。

**API评估**：有关评估OpenAI、Anthropic和其他API模型，请参阅 [references/api-evaluation.md](references/api-evaluation.md)。

**多GPU策略**：有关数据并行和张量并行评估，请参阅 [references/distributed-eval.md](references/distributed-eval.md)。

## 硬件要求

- **GPU**：NVIDIA（CUDA 11.8+），可在CPU上工作（非常慢）
- **VRAM**：
  - 7B模型：16GB（bf16）或8GB（8位）
  - 13B模型：28GB（bf16）或14GB（8位）
  - 70B模型：需要多GPU或量化
- **时间**（7B模型，单个A100）：
  - HellaSwag：10分钟
  - GSM8K：5分钟
  - MMLU（完整）：2小时
  - HumanEval：20分钟

## 资源

- GitHub：https://github.com/EleutherAI/lm-evaluation-harness
- 文档：https://github.com/EleutherAI/lm-evaluation-harness/tree/main/docs
- 任务库：60多个任务，包括MMLU、GSM8K、HumanEval、TruthfulQA、HellaSwag、ARC、WinoGrande等
- 排行榜：https://huggingface.co/spaces/HuggingFaceH4/open_llm_leaderboard（使用此框架）

