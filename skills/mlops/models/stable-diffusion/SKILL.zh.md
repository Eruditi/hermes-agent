
---
name: stable-diffusion-image-generation
description: 通过HuggingFace Diffusers使用Stable Diffusion模型进行最先进的文本到图像生成。用于从文本提示生成图像、执行图像到图像转换、修复或构建自定义扩散管道。
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [diffusers&gt;=0.30.0, transformers&gt;=4.41.0, accelerate&gt;=0.31.0, torch&gt;=2.0.0]
metadata:
  hermes:
    tags: [图像生成, Stable Diffusion, Diffusers, 文本到图像, 多模态, 计算机视觉]

---

# Stable Diffusion 图像生成

使用HuggingFace Diffusers库通过Stable Diffusion生成图像的综合指南。

## 何时使用Stable Diffusion

**使用Stable Diffusion的情况：**
- 从文本描述生成图像
- 执行图像到图像转换（风格迁移、增强）
- 修复（填充遮罩区域）
- 扩展（将图像扩展到边界之外）
- 创建现有图像的变体
- 构建自定义图像生成工作流

**关键特性：**
- **文本到图像**：从自然语言提示生成图像
- **图像到图像**：使用文本指导转换现有图像
- **修复**：用上下文感知内容填充遮罩区域
- **ControlNet**：添加空间条件（边缘、姿势、深度）
- **LoRA支持**：高效的微调和风格适配
- **多种模型**：支持SD 1.5、SDXL、SD 3.0、Flux

**使用替代方案：**
- **DALL-E 3**：用于基于API的生成，无需GPU
- **Midjourney**：用于艺术风格化输出
- **Imagen**：用于Google Cloud集成
- **Leonardo.ai**：用于基于Web的创意工作流

## 快速开始

### 安装

```bash
pip install diffusers transformers accelerate torch
pip install xformers  # 可选：内存高效的注意力
```

### 基本文本到图像

```python
from diffusers import DiffusionPipeline
import torch

# 加载管道（自动检测模型类型）
pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
)
pipe.to("cuda")

# 生成图像
image = pipe(
    "日落时宁静的山脉景观，高度详细",
    num_inference_steps=50,
    guidance_scale=7.5
).images[0]

image.save("output.png")
```

### 使用SDXL（更高质量）

```python
from diffusers import AutoPipelineForText2Image
import torch

pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")

# 启用内存优化
pipe.enable_model_cpu_offload()

image = pipe(
    prompt="未来城市有飞行汽车，电影级灯光",
    height=1024,
    width=1024,
    num_inference_steps=30
).images[0]
```

## 架构概述

### 三大支柱设计

Diffusers围绕三个核心组件构建：

```
管道（编排）
├── 模型（神经网络）
│   ├── UNet / Transformer（噪声预测）
│   ├── VAE（潜在编码/解码）
│   └── 文本编码器（CLIP/T5）
└── 调度器（去噪算法）
```

### 管道推理流程

```
文本提示 → 文本编码器 → 文本嵌入
                                    ↓
随机噪声 → [去噪循环] ← 调度器
                      ↓
               预测噪声
                      ↓
              VAE解码器 → 最终图像
```

## 核心概念

### 管道

管道编排完整的工作流：

| 管道 | 用途 |
|----------|---------|
| `StableDiffusionPipeline` | 文本到图像（SD 1.x/2.x） |
| `StableDiffusionXLPipeline` | 文本到图像（SDXL） |
| `StableDiffusion3Pipeline` | 文本到图像（SD 3.0） |
| `FluxPipeline` | 文本到图像（Flux模型） |
| `StableDiffusionImg2ImgPipeline` | 图像到图像 |
| `StableDiffusionInpaintPipeline` | 修复 |

### 调度器

调度器控制去噪过程：

| 调度器 | 步骤 | 质量 | 用例 |
|-----------|-------|---------|----------|
| `EulerDiscreteScheduler` | 20-50 | 好 | 默认选择 |
| `EulerAncestralDiscreteScheduler` | 20-50 | 好 | 更多变化 |
| `DPMSolverMultistepScheduler` | 15-25 | 优秀 | 快速，高质量 |
| `DDIMScheduler` | 50-100 | 好 | 确定性 |
| `LCMScheduler` | 4-8 | 好 | 非常快 |
| `UniPCMultistepScheduler` | 15-25 | 优秀 | 快速收敛 |

### 交换调度器

```python
from diffusers import DPMSolverMultistepScheduler

# 交换以获得更快的生成
pipe.scheduler = DPMSolverMultistepScheduler.from_config(
    pipe.scheduler.config
)

# 现在用更少的步骤生成
image = pipe(prompt, num_inference_steps=20).images[0]
```

## 生成参数

### 关键参数

| 参数 | 默认值 | 描述 |
|-----------|---------|-------------|
| `prompt` | 必需 | 所需图像的文本描述 |
| `negative_prompt` | 无 | 图像中要避免的内容 |
| `num_inference_steps` | 50 | 去噪步骤（更多=更好质量） |
| `guidance_scale` | 7.5 | 提示遵循度（通常7-12） |
| `height`, `width` | 512/1024 | 输出尺寸（8的倍数） |
| `generator` | 无 | 用于可重复性的Torch生成器 |
| `num_images_per_prompt` | 1 | 批量大小 |

### 可重复生成

```python
import torch

generator = torch.Generator(device="cuda").manual_seed(42)

image = pipe(
    prompt="戴高顶礼帽的猫",
    generator=generator,
    num_inference_steps=50
).images[0]
```

### 负面提示

```python
image = pipe(
    prompt="花园里狗的专业照片",
    negative_prompt="模糊，低质量，扭曲，丑陋，解剖学错误",
    guidance_scale=7.5
).images[0]
```

## 图像到图像

使用文本指导转换现有图像：

```python
from diffusers import AutoPipelineForImage2Image
from PIL import Image

pipe = AutoPipelineForImage2Image.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

init_image = Image.open("input.jpg").resize((512, 512))

image = pipe(
    prompt="场景的水彩画",
    image=init_image,
    strength=0.75,  # 转换程度（0-1）
    num_inference_steps=50
).images[0]
```

## 修复

填充遮罩区域：

```python
from diffusers import AutoPipelineForInpainting
from PIL import Image

pipe = AutoPipelineForInpainting.from_pretrained(
    "runwayml/stable-diffusion-inpainting",
    torch_dtype=torch.float16
).to("cuda")

image = Image.open("photo.jpg")
mask = Image.open("mask.png")  # 白色=修复区域

result = pipe(
    prompt="一辆红色汽车停在街上",
    image=image,
    mask_image=mask,
    num_inference_steps=50
).images[0]
```

## ControlNet

添加空间条件以获得精确控制：

```python
from diffusers import StableDiffusionControlNetPipeline, ControlNetModel
import torch

# 加载用于边缘条件的ControlNet
controlnet = ControlNetModel.from_pretrained(
    "lllyasviel/control_v11p_sd15_canny",
    torch_dtype=torch.float16
)

pipe = StableDiffusionControlNetPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    controlnet=controlnet,
    torch_dtype=torch.float16
).to("cuda")

# 使用Canny边缘图像作为控制
control_image = get_canny_image(input_image)

image = pipe(
    prompt="梵高风格的漂亮房子",
    image=control_image,
    num_inference_steps=30
).images[0]
```

### 可用的ControlNets

| ControlNet | 输入类型 | 用例 |
|------------|------------|----------|
| `canny` | 边缘图 | 保留结构 |
| `openpose` | 姿势骨架 | 人体姿势 |
| `depth` | 深度图 | 3D感知生成 |
| `normal` | 法线图 | 表面细节 |
| `mlsd` | 线段 | 建筑线条 |
| `scribble` | 粗略草图 | 草图到图像 |

## LoRA适配器

加载微调的风格适配器：

```python
from diffusers import DiffusionPipeline

pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    torch_dtype=torch.float16
).to("cuda")

# 加载LoRA权重
pipe.load_lora_weights("path/to/lora", weight_name="style.safetensors")

# 使用LoRA风格生成
image = pipe("训练风格的肖像").images[0]

# 调整LoRA强度
pipe.fuse_lora(lora_scale=0.8)

# 卸载LoRA
pipe.unload_lora_weights()
```

### 多个LoRA

```python
# 加载多个LoRA
pipe.load_lora_weights("lora1", adapter_name="style")
pipe.load_lora_weights("lora2", adapter_name="character")

# 为每个设置权重
pipe.set_adapters(["style", "character"], adapter_weights=[0.7, 0.5])

image = pipe("一幅肖像").images[0]
```

## 内存优化

### 启用CPU卸载

```python
# 模型CPU卸载 - 在不使用时将模型移动到CPU
pipe.enable_model_cpu_offload()

# 顺序CPU卸载 - 更激进，更慢
pipe.enable_sequential_cpu_offload()
```

### 注意力切片

```python
# 通过分块计算注意力来减少内存
pipe.enable_attention_slicing()

# 或特定块大小
pipe.enable_attention_slicing("max")
```

### xFormers内存高效注意力

```python
# 需要xformers包
pipe.enable_xformers_memory_efficient_attention()
```

### 大图像的VAE切片

```python
# 为大图像分块解码潜在表示
pipe.enable_vae_slicing()
pipe.enable_vae_tiling()
```

## 模型变体

### 加载不同精度

```python
# FP16（推荐用于GPU）
pipe = DiffusionPipeline.from_pretrained(
    "model-id",
    torch_dtype=torch.float16,
    variant="fp16"
)

# BF16（更好的精度，需要Ampere+ GPU）
pipe = DiffusionPipeline.from_pretrained(
    "model-id",
    torch_dtype=torch.bfloat16
)
```

### 加载特定组件

```python
from diffusers import UNet2DConditionModel, AutoencoderKL

# 加载自定义VAE
vae = AutoencoderKL.from_pretrained("stabilityai/sd-vae-ft-mse")

# 与管道一起使用
pipe = DiffusionPipeline.from_pretrained(
    "stable-diffusion-v1-5/stable-diffusion-v1-5",
    vae=vae,
    torch_dtype=torch.float16
)
```

## 批量生成

高效生成多个图像：

```python
# 多个提示
prompts = [
    "弹钢琴的猫",
    "读书的狗",
    "画画的鸟"
]

images = pipe(prompts, num_inference_steps=30).images

# 每个提示多个图像
images = pipe(
    "美丽的日落",
    num_images_per_prompt=4,
    num_inference_steps=30
).images
```

## 常见工作流

### 工作流1：高质量生成

```python
from diffusers import StableDiffusionXLPipeline, DPMSolverMultistepScheduler
import torch

# 1. 加载带有优化的SDXL
pipe = StableDiffusionXLPipeline.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16,
    variant="fp16"
)
pipe.to("cuda")
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)
pipe.enable_model_cpu_offload()

# 2. 使用质量设置生成
image = pipe(
    prompt="大草原上雄伟的狮子，黄金时段灯光，8k，详细的毛皮",
    negative_prompt="模糊，低质量，卡通，动漫，草图",
    num_inference_steps=30,
    guidance_scale=7.5,
    height=1024,
    width=1024
).images[0]
```

### 工作流2：快速原型设计

```python
from diffusers import AutoPipelineForText2Image, LCMScheduler
import torch

# 使用LCM进行4-8步生成
pipe = AutoPipelineForText2Image.from_pretrained(
    "stabilityai/stable-diffusion-xl-base-1.0",
    torch_dtype=torch.float16
).to("cuda")

# 加载LCM LoRA以快速生成
pipe.load_lora_weights("latent-consistency/lcm-lora-sdxl")
pipe.scheduler = LCMScheduler.from_config(pipe.scheduler.config)
pipe.fuse_lora()

# 在~1秒内生成
image = pipe(
    "美丽的风景",
    num_inference_steps=4,
    guidance_scale=1.0
).images[0]
```

## 常见问题

**CUDA内存不足：**
```python
# 启用内存优化
pipe.enable_model_cpu_offload()
pipe.enable_attention_slicing()
pipe.enable_vae_slicing()

# 或使用更低精度
pipe = DiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16)
```

**黑色/噪声图像：**
```python
# 检查VAE配置
# 如果需要，使用安全检查器绕过
pipe.safety_checker = None

# 确保适当的dtype一致性
pipe = pipe.to(dtype=torch.float16)
```

**生成缓慢：**
```python
# 使用更快的调度器
from diffusers import DPMSolverMultistepScheduler
pipe.scheduler = DPMSolverMultistepScheduler.from_config(pipe.scheduler.config)

# 减少步骤
image = pipe(prompt, num_inference_steps=20).images[0]
```

## 参考

- **[高级用法](references/advanced-usage.md)** - 自定义管道、微调、部署
- **[故障排除](references/troubleshooting.md)** - 常见问题和解决方案

## 资源

- **文档**：https://huggingface.co/docs/diffusers
- **仓库**：https://github.com/huggingface/diffusers
- **模型中心**：https://huggingface.co/models?library=diffusers
- **Discord**：https://discord.gg/diffusers
