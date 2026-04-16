
---
name: fine-tuning-with-trl
description: 使用TRL通过强化学习微调LLM - SFT用于指令微调，DPO用于偏好对齐，PPO/GRPO用于奖励优化，以及奖励模型训练。当需要RLHF、将模型与偏好对齐或从人类反馈中训练时使用。与HuggingFace Transformers一起使用。
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [trl, transformers, datasets, peft, accelerate, torch]
metadata:
  hermes:
    tags: [后训练, TRL, 强化学习, 微调, SFT, DPO, PPO, GRPO, RLHF, 偏好对齐, HuggingFace]

---

# TRL - Transformer强化学习

## 快速开始

TRL提供用于将语言模型与人类偏好对齐的后训练方法。

**安装**：
```bash
pip install trl transformers datasets peft accelerate
```

**监督微调**（指令微调）：
```python
from trl import SFTTrainer

trainer = SFTTrainer(
    model="Qwen/Qwen2.5-0.5B",
    train_dataset=dataset,  # 提示-完成对
)
trainer.train()
```

**DPO**（与偏好对齐）：
```python
from trl import DPOTrainer, DPOConfig

config = DPOConfig(output_dir="model-dpo", beta=0.1)
trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=preference_dataset,  # 选择/拒绝对
    processing_class=tokenizer
)
trainer.train()
```

## 常见工作流

### 工作流1：完整RLHF管道（SFT → 奖励模型 → PPO）

从基础模型到人类对齐模型的完整管道。

复制此检查清单：

```
RLHF训练：
- [ ] 步骤1：监督微调（SFT）
- [ ] 步骤2：训练奖励模型
- [ ] 步骤3：PPO强化学习
- [ ] 步骤4：评估对齐模型
```

**步骤1：监督微调**

在指令遵循数据上训练基础模型：

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import SFTTrainer, SFTConfig
from datasets import load_dataset

# 加载模型
model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B")

# 加载指令数据集
dataset = load_dataset("trl-lib/Capybara", split="train")

# 配置训练
training_args = SFTConfig(
    output_dir="Qwen2.5-0.5B-SFT",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=2e-5,
    logging_steps=10,
    save_strategy="epoch"
)

# 训练
trainer = SFTTrainer(
    model=model,
    args=training_args,
    train_dataset=dataset,
    tokenizer=tokenizer
)
trainer.train()
trainer.save_model()
```

**步骤2：训练奖励模型**

训练模型以预测人类偏好：

```python
from transformers import AutoModelForSequenceClassification
from trl import RewardTrainer, RewardConfig

# 加载SFT模型作为基础
model = AutoModelForSequenceClassification.from_pretrained(
    "Qwen2.5-0.5B-SFT",
    num_labels=1  # 单个奖励分数
)
tokenizer = AutoTokenizer.from_pretrained("Qwen2.5-0.5B-SFT")

# 加载偏好数据（选择/拒绝对）
dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")

# 配置训练
training_args = RewardConfig(
    output_dir="Qwen2.5-0.5B-Reward",
    per_device_train_batch_size=2,
    num_train_epochs=1,
    learning_rate=1e-5
)

# 训练奖励模型
trainer = RewardTrainer(
    model=model,
    args=training_args,
    processing_class=tokenizer,
    train_dataset=dataset
)
trainer.train()
trainer.save_model()
```

**步骤3：PPO强化学习**

使用奖励模型优化策略：

```bash
python -m trl.scripts.ppo \
    --model_name_or_path Qwen2.5-0.5B-SFT \
    --reward_model_path Qwen2.5-0.5B-Reward \
    --dataset_name trl-internal-testing/descriptiveness-sentiment-trl-style \
    --output_dir Qwen2.5-0.5B-PPO \
    --learning_rate 3e-6 \
    --per_device_train_batch_size 64 \
    --total_episodes 10000
```

**步骤4：评估**

```python
from transformers import pipeline

# 加载对齐模型
generator = pipeline("text-generation", model="Qwen2.5-0.5B-PPO")

# 测试
prompt = "向10岁孩子解释量子计算"
output = generator(prompt, max_length=200)[0]["generated_text"]
print(output)
```

### 工作流2：使用DPO的简单偏好对齐

无需奖励模型即可将模型与偏好对齐。

复制此检查清单：

```
DPO训练：
- [ ] 步骤1：准备偏好数据集
- [ ] 步骤2：配置DPO
- [ ] 步骤3：使用DPOTrainer训练
- [ ] 步骤4：评估对齐
```

**步骤1：准备偏好数据集**

数据集格式：
```json
{
  "prompt": "法国的首都是什么？",
  "chosen": "法国的首都是巴黎。",
  "rejected": "我不知道。"
}
```

加载数据集：
```python
from datasets import load_dataset

dataset = load_dataset("trl-lib/ultrafeedback_binarized", split="train")
# 或加载您自己的
# dataset = load_dataset("json", data_files="preferences.json")
```

**步骤2：配置DPO**

```python
from trl import DPOConfig

config = DPOConfig(
    output_dir="Qwen2.5-0.5B-DPO",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=5e-7,
    beta=0.1,  # KL惩罚强度
    max_prompt_length=512,
    max_length=1024,
    logging_steps=10
)
```

**步骤3：使用DPOTrainer训练**

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
from trl import DPOTrainer

model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
tokenizer = AutoTokenizer.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")

trainer = DPOTrainer(
    model=model,
    args=config,
    train_dataset=dataset,
    processing_class=tokenizer
)

trainer.train()
trainer.save_model()
```

**CLI替代方案**：
```bash
trl dpo \
    --model_name_or_path Qwen/Qwen2.5-0.5B-Instruct \
    --dataset_name argilla/Capybara-Preferences \
    --output_dir Qwen2.5-0.5B-DPO \
    --per_device_train_batch_size 4 \
    --learning_rate 5e-7 \
    --beta 0.1
```

### 工作流3：使用GRPO的内存高效在线RL

使用最小内存进行强化学习训练。

复制此检查清单：

```
GRPO训练：
- [ ] 步骤1：定义奖励函数
- [ ] 步骤2：配置GRPO
- [ ] 步骤3：使用GRPOTrainer训练
```

**步骤1：定义奖励函数**

```python
def reward_function(completions, **kwargs):
    """
    计算完成的奖励。

    Args：
        completions：生成的文本列表

    Returns：
        奖励分数列表（浮点数）
    """
    rewards = []
    for completion in completions:
        # 示例：基于长度和唯一词的奖励
        score = len(completion.split())  # 更喜欢更长的响应
        score += len(set(completion.lower().split()))  # 奖励唯一词
        rewards.append(score)
    return rewards
```

或使用奖励模型：
```python
from transformers import pipeline

reward_model = pipeline("text-classification", model="reward-model-path")

def reward_from_model(completions, prompts, **kwargs):
    # 组合提示+完成
    full_texts = [p + c for p, c in zip(prompts, completions)]
    # 获取奖励分数
    results = reward_model(full_texts)
    return [r["score"] for r in results]
```

**步骤2：配置GRPO**

```python
from trl import GRPOConfig

config = GRPOConfig(
    output_dir="Qwen2-GRPO",
    per_device_train_batch_size=4,
    num_train_epochs=1,
    learning_rate=1e-5,
    num_generations=4,  # 每个提示生成4个完成
    max_new_tokens=128
)
```

**步骤3：使用GRPOTrainer训练**

```python
from datasets import load_dataset
from trl import GRPOTrainer

# 加载仅提示的数据集
dataset = load_dataset("trl-lib/tldr", split="train")

trainer = GRPOTrainer(
    model="Qwen/Qwen2-0.5B-Instruct",
    reward_funcs=reward_function,  # 您的奖励函数
    args=config,
    train_dataset=dataset
)

trainer.train()
```

**CLI**：
```bash
trl grpo \
    --model_name_or_path Qwen/Qwen2-0.5B-Instruct \
    --dataset_name trl-lib/tldr \
    --output_dir Qwen2-GRPO \
    --num_generations 4
```

## 何时使用vs替代方案

**使用TRL的情况：**
- 需要将模型与人类偏好对齐
- 有偏好数据（选择/拒绝对）
- 想要使用强化学习（PPO、GRPO）
- 需要奖励模型训练
- 正在进行RLHF（完整管道）

**方法选择**：
- **SFT**：有提示-完成对，想要基本指令遵循
- **DPO**：有偏好，想要简单对齐（无需奖励模型）
- **PPO**：有奖励模型，需要最大程度控制RL
- **GRPO**：内存受限，想要在线RL
- **奖励模型**：构建RLHF管道，需要为生成评分

**使用替代方案：**
- **HuggingFace Trainer**：无RL的基本微调
- **Axolotl**：基于YAML的训练配置
- **LitGPT**：教育性，最小化微调
- **Unsloth**：快速LoRA训练

## 常见问题

**问题：DPO训练期间OOM**

减少批大小和序列长度：
```python
config = DPOConfig(
    per_device_train_batch_size=1,  # 从4减少
    max_length=512,  # 从1024减少
    gradient_accumulation_steps=8  # 保持有效批次
)
```

或使用梯度检查点：
```python
model.gradient_checkpointing_enable()
```

**问题：对齐质量差**

调整beta参数：
```python
# 更高的beta = 更保守（更接近参考）
config = DPOConfig(beta=0.5)  # 默认0.1

# 更低的beta = 更激进的对齐
config = DPOConfig(beta=0.01)
```

**问题：奖励模型不学习**

检查损失类型和学习率：
```python
config = RewardConfig(
    learning_rate=1e-5,  # 尝试不同的LR
    num_train_epochs=3  # 训练更长
)
```

确保偏好数据集有明确的赢家：
```python
# 验证数据集
print(dataset[0])
# 应该有明确的选择 &gt; 拒绝
```

**问题：PPO训练不稳定**

调整KL系数：
```python
config = PPOConfig(
    kl_coef=0.1,  # 从0.05增加
    cliprange=0.1  # 从0.2减少
)
```

## 高级主题

**SFT训练指南**：有关数据集格式、聊天模板、打包策略和多GPU训练，请参阅[references/sft-training.md](references/sft-training.md)。

**DPO变体**：有关IPO、cDPO、RPO和其他DPO损失函数及推荐超参数，请参阅[references/dpo-variants.md](references/dpo-variants.md)。

**奖励建模**：有关结果与过程奖励、Bradley-Terry损失和奖励模型评估，请参阅[references/reward-modeling.md](references/reward-modeling.md)。

**在线RL方法**：有关PPO、GRPO、RLOO和OnlineDPO及详细配置，请参阅[references/online-rl.md](references/online-rl.md)。

## 硬件要求

- **GPU**：NVIDIA（需要CUDA）
- **VRAM**：取决于模型和方法
  - SFT 7B：16GB（使用LoRA）
  - DPO 7B：24GB（存储参考模型）
  - PPO 7B：40GB（策略+奖励模型）
  - GRPO 7B：24GB（更内存高效）
- **多GPU**：通过`accelerate`支持
- **混合精度**：推荐BF16（A100/H100）

**内存优化**：
- 对所有方法使用LoRA/QLoRA
- 启用梯度检查点
- 使用更小的批大小和梯度累积

## 资源

- 文档：https://huggingface.co/docs/trl/
- GitHub：https://github.com/huggingface/trl
- 论文：
  - "Training language models to follow instructions with human feedback" (InstructGPT, 2022)
  - "Direct Preference Optimization: Your Language Model is Secretly a Reward Model" (DPO, 2023)
  - "Group Relative Policy Optimization" (GRPO, 2024)
- 示例：https://github.com/huggingface/trl/tree/main/examples/scripts

