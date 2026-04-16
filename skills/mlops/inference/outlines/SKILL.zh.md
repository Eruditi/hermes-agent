
---
name: outlines
description: 在生成期间保证有效的JSON/XML/代码结构，使用Pydantic模型获得类型安全的输出，支持本地模型（Transformers、vLLM），并使用Outlines最大化推理速度 - dottxt.ai的结构化生成库
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [outlines, transformers, vllm, pydantic]
metadata:
  hermes:
    tags: [提示工程, Outlines, 结构化生成, JSON Schema, Pydantic, 本地模型, 基于语法的生成, vLLM, Transformers, 类型安全]

---

# Outlines: 结构化文本生成

## 何时使用此技能

当你需要时使用Outlines：
- **在生成期间保证有效的JSON/XML/代码** 结构
- **使用Pydantic模型** 获得类型安全的输出
- **支持本地模型**（Transformers、llama.cpp、vLLM）
- **最大化推理速度** 零开销的结构化生成
- **自动生成符合JSON模式** 的内容
- **在语法级别控制令牌采样**

**GitHub Stars**：8,000+ | **来自**：dottxt.ai（以前是.txt）

## 安装

```bash
# 基本安装
pip install outlines

# 带特定后端
pip install outlines transformers  # Hugging Face模型
pip install outlines llama-cpp-python  # llama.cpp
pip install outlines vllm  # 高吞吐量的vLLM
```

## 快速开始

### 基本示例：分类

```python
import outlines
from typing import Literal

# 加载模型
model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# 使用类型约束生成
prompt = "Sentiment of 'This product is amazing!': "
generator = outlines.generate.choice(model, ["positive", "negative", "neutral"])
sentiment = generator(prompt)

print(sentiment)  # "positive"（保证是这些之一）
```

### 使用Pydantic模型

```python
from pydantic import BaseModel
import outlines

class User(BaseModel):
    name: str
    age: int
    email: str

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# 生成结构化输出
prompt = "Extract user: John Doe, 30 years old, john@example.com"
generator = outlines.generate.json(model, User)
user = generator(prompt)

print(user.name)   # "John Doe"
print(user.age)    # 30
print(user.email)  # "john@example.com"
```

## 核心概念

### 1. 约束令牌采样

Outlines使用有限状态机（FSM）在logit级别约束令牌生成。

**工作原理：**
1. 将模式（JSON/Pydantic/regex）转换为上下文无关语法（CFG）
2. 将CFG转换为有限状态机（FSM）
3. 在生成期间的每个步骤过滤无效令牌
4. 当只有一个有效令牌时快速前进

**优势：**
- **零开销**：过滤发生在令牌级别
- **速度提升**：通过确定性路径快速前进
- **保证有效性**：无效输出不可能

```python
import outlines

# Pydantic模型 -&gt; JSON模式 -&gt; CFG -&gt; FSM
class Person(BaseModel):
    name: str
    age: int

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# 幕后：
# 1. Person -&gt; JSON模式
# 2. JSON模式 -&gt; CFG
# 3. CFG -&gt; FSM
# 4. FSM在生成期间过滤令牌

generator = outlines.generate.json(model, Person)
result = generator("Generate person: Alice, 25")
```

### 2. 结构化生成器

Outlines为不同的输出类型提供专门的生成器。

#### 选择生成器

```python
# 多项选择
generator = outlines.generate.choice(
    model,
    ["positive", "negative", "neutral"]
)

sentiment = generator("Review: This is great!")
# 结果：三个选择之一
```

#### JSON生成器

```python
from pydantic import BaseModel

class Product(BaseModel):
    name: str
    price: float
    in_stock: bool

# 生成匹配模式的有效JSON
generator = outlines.generate.json(model, Product)
product = generator("Extract: iPhone 15, $999, available")

# 保证有效的Product实例
print(type(product))  # &lt;class '__main__.Product'&gt;
```

#### 正则表达式生成器

```python
# 生成匹配正则表达式的文本
generator = outlines.generate.regex(
    model,
    r"[0-9]{3}-[0-9]{3}-[0-9]{4}"  # 电话号码模式
)

phone = generator("Generate phone number:")
# 结果："555-123-4567"（保证匹配模式）
```

#### 整数/浮点数生成器

```python
# 生成特定的数值类型
int_generator = outlines.generate.integer(model)
age = int_generator("Person's age:")  # 保证整数

float_generator = outlines.generate.float(model)
price = float_generator("Product price:")  # 保证浮点数
```

### 3. 模型后端

Outlines支持多个本地和基于API的后端。

#### Transformers (Hugging Face)

```python
import outlines

# 从Hugging Face加载
model = outlines.models.transformers(
    "microsoft/Phi-3-mini-4k-instruct",
    device="cuda"  # 或 "cpu"
)

# 与任何生成器一起使用
generator = outlines.generate.json(model, YourModel)
```

#### llama.cpp

```python
# 加载GGUF模型
model = outlines.models.llamacpp(
    "./models/llama-3.1-8b-instruct.Q4_K_M.gguf",
    n_gpu_layers=35
)

generator = outlines.generate.json(model, YourModel)
```

#### vLLM (高吞吐量)

```python
# 用于生产部署
model = outlines.models.vllm(
    "meta-llama/Llama-3.1-8B-Instruct",
    tensor_parallel_size=2  # 多GPU
)

generator = outlines.generate.json(model, YourModel)
```

#### OpenAI (有限支持)

```python
# 基本OpenAI支持
model = outlines.models.openai(
    "gpt-4o-mini",
    api_key="your-api-key"
)

# 注意：API模型的某些功能有限
generator = outlines.generate.json(model, YourModel)
```

### 4. Pydantic集成

Outlines具有一流的Pydantic支持和自动模式转换。

#### 基本模型

```python
from pydantic import BaseModel, Field

class Article(BaseModel):
    title: str = Field(description="Article title")
    author: str = Field(description="Author name")
    word_count: int = Field(description="Number of words", gt=0)
    tags: list[str] = Field(description="List of tags")

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, Article)

article = generator("Generate article about AI")
print(article.title)
print(article.word_count)  # 保证 &gt; 0
```

#### 嵌套模型

```python
class Address(BaseModel):
    street: str
    city: str
    country: str

class Person(BaseModel):
    name: str
    age: int
    address: Address  # 嵌套模型

generator = outlines.generate.json(model, Person)
person = generator("Generate person in New York")

print(person.address.city)  # "New York"
```

#### 枚举和字面量

```python
from enum import Enum
from typing import Literal

class Status(str, Enum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class Application(BaseModel):
    applicant: str
    status: Status  # 必须是枚举值之一
    priority: Literal["low", "medium", "high"]  # 必须是字面量之一

generator = outlines.generate.json(model, Application)
app = generator("Generate application")

print(app.status)  # Status.PENDING（或APPROVED/REJECTED）
```

## 常见模式

### 模式1：数据提取

```python
from pydantic import BaseModel
import outlines

class CompanyInfo(BaseModel):
    name: str
    founded_year: int
    industry: str
    employees: int

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, CompanyInfo)

text = """
Apple Inc. was founded in 1976 in the technology industry.
The company employs approximately 164,000 people worldwide.
"""

prompt = f"Extract company information:\n{text}\n\nCompany:"
company = generator(prompt)

print(f"Name: {company.name}")
print(f"Founded: {company.founded_year}")
print(f"Industry: {company.industry}")
print(f"Employees: {company.employees}")
```

### 模式2：分类

```python
from typing import Literal
import outlines

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# 二分类
generator = outlines.generate.choice(model, ["spam", "not_spam"])
result = generator("Email: Buy now! 50% off!")

# 多分类
categories = ["technology", "business", "sports", "entertainment"]
category_gen = outlines.generate.choice(model, categories)
category = category_gen("Article: Apple announces new iPhone...")

# 带置信度
class Classification(BaseModel):
    label: Literal["positive", "negative", "neutral"]
    confidence: float

classifier = outlines.generate.json(model, Classification)
result = classifier("Review: This product is okay, nothing special")
```

### 模式3：结构化表单

```python
class UserProfile(BaseModel):
    full_name: str
    age: int
    email: str
    phone: str
    country: str
    interests: list[str]

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, UserProfile)

prompt = """
Extract user profile from:
Name: Alice Johnson
Age: 28
Email: alice@example.com
Phone: 555-0123
Country: USA
Interests: hiking, photography, cooking
"""

profile = generator(prompt)
print(profile.full_name)
print(profile.interests)  # ["hiking", "photography", "cooking"]
```

### 模式4：多实体提取

```python
class Entity(BaseModel):
    name: str
    type: Literal["PERSON", "ORGANIZATION", "LOCATION"]

class DocumentEntities(BaseModel):
    entities: list[Entity]

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, DocumentEntities)

text = "Tim Cook met with Satya Nadella at Microsoft headquarters in Redmond."
prompt = f"Extract entities from: {text}"

result = generator(prompt)
for entity in result.entities:
    print(f"{entity.name} ({entity.type})")
```

### 模式5：代码生成

```python
class PythonFunction(BaseModel):
    function_name: str
    parameters: list[str]
    docstring: str
    body: str

model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
generator = outlines.generate.json(model, PythonFunction)

prompt = "Generate a Python function to calculate factorial"
func = generator(prompt)

print(f"def {func.function_name}({', '.join(func.parameters)}):")
print(f'    """{func.docstring}"""')
print(f"    {func.body}")
```

### 模式6：批处理

```python
def batch_extract(texts: list[str], schema: type[BaseModel]):
    """从多个文本中提取结构化数据。"""
    model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")
    generator = outlines.generate.json(model, schema)

    results = []
    for text in texts:
        result = generator(f"Extract from: {text}")
        results.append(result)

    return results

class Person(BaseModel):
    name: str
    age: int

texts = [
    "John is 30 years old",
    "Alice is 25 years old",
    "Bob is 40 years old"
]

people = batch_extract(texts, Person)
for person in people:
    print(f"{person.name}: {person.age}")
```

## 后端配置

### Transformers

```python
import outlines

# 基本使用
model = outlines.models.transformers("microsoft/Phi-3-mini-4k-instruct")

# GPU配置
model = outlines.models.transformers(
    "microsoft/Phi-3-mini-4k-instruct",
    device="cuda",
    model_kwargs={"torch_dtype": "float16"}
)

# 流行模型
model = outlines.models.transformers("meta-llama/Llama-3.1-8B-Instruct")
model = outlines.models.transformers("mistralai/Mistral-7B-Instruct-v0.3")
model = outlines.models.transformers("Qwen/Qwen2.5-7B-Instruct")
```

### llama.cpp

```python
# 加载GGUF模型
model = outlines.models.llamacpp(
    "./models/llama-3.1-8b.Q4_K_M.gguf",
    n_ctx=4096,         # 上下文窗口
    n_gpu_layers=35,    # GPU层
    n_threads=8         # CPU线程
)

# 完全GPU卸载
model = outlines.models.llamacpp(
    "./models/model.gguf",
    n_gpu_layers=-1  # 所有层在GPU上
)
```

### vLLM (生产)

```python
# 单GPU
model = outlines.models.vllm("meta-llama/Llama-3.1-8B-Instruct")

# 多GPU
model = outlines.models.vllm(
    "meta-llama/Llama-3.1-70B-Instruct",
    tensor_parallel_size=4  # 4个GPU
)

# 带量化
model = outlines.models.vllm(
    "meta-llama/Llama-3.1-8B-Instruct",
    quantization="awq"  # 或 "gptq"
)
```

## 最佳实践

### 1. 使用特定类型

```python
# ✅ 好：特定类型
class Product(BaseModel):
    name: str
    price: float  # 不是str
    quantity: int  # 不是str
    in_stock: bool  # 不是str

# ❌ 不好：所有东西都是字符串
class Product(BaseModel):
    name: str
    price: str  # 应该是float
    quantity: str  # 应该是int
```

### 2. 添加约束

```python
from pydantic import Field

# ✅ 好：带约束
class User(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    age: int = Field(ge=0, le=120)
    email: str = Field(pattern=r"^[\w\.-]+@[\w\.-]+\.\w+$")

# ❌ 不好：无约束
class User(BaseModel):
    name: str
    age: int
    email: str
```

### 3. 对类别使用枚举

```python
# ✅ 好：固定集合的枚举
class Priority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class Task(BaseModel):
    title: str
    priority: Priority

# ❌ 不好：自由形式字符串
class Task(BaseModel):
    title: str
    priority: str  # 可以是任何东西
```

### 4. 在提示中提供上下文

```python
# ✅ 好：清晰的上下文
prompt = """
Extract product information from the following text.
Text: iPhone 15 Pro costs $999 and is currently in stock.
Product:
"""

# ❌ 不好：最小上下文
prompt = "iPhone 15 Pro costs $999 and is currently in stock."
```

### 5. 处理可选字段

```python
from typing import Optional

# ✅ 好：不完整数据的可选字段
class Article(BaseModel):
    title: str  # 必需
    author: Optional[str] = None  # 可选
    date: Optional[str] = None  # 可选
    tags: list[str] = []  # 默认空列表

# 即使author/date缺失也能成功
```

## 与替代方案的比较

| 功能 | Outlines | Instructor | Guidance | LMQL |
|---------|----------|------------|----------|------|
| Pydantic支持 | ✅ 原生 | ✅ 原生 | ❌ 否 | ❌ 否 |
| JSON模式 | ✅ 是 | ✅ 是 | ⚠️ 有限 | ✅ 是 |
| 正则表达式约束 | ✅ 是 | ❌ 否 | ✅ 是 | ✅ 是 |
| 本地模型 | ✅ 完整 | ⚠️ 有限 | ✅ 完整 | ✅ 完整 |
| API模型 | ⚠️ 有限 | ✅ 完整 | ✅ 完整 | ✅ 完整 |
| 零开销 | ✅ 是 | ❌ 否 | ⚠️ 部分 | ✅ 是 |
| 自动重试 | ❌ 否 | ✅ 是 | ❌ 否 | ❌ 否 |
| 学习曲线 | 低 | 低 | 低 | 高 |

**何时选择Outlines：**
- 使用本地模型（Transformers、llama.cpp、vLLM）
- 需要最大推理速度
- 想要Pydantic模型支持
- 要求零开销的结构化生成
- 控制令牌采样过程

**何时选择替代方案：**
- Instructor：需要带自动重试的API模型
- Guidance：需要令牌修复和复杂工作流程
- LMQL：更喜欢声明性查询语法

## 性能特性

**速度：**
- **零开销**：结构化生成与无约束一样快
- **快速前进优化**：跳过确定性令牌
- **比生成后验证方法快1.2-2倍**

**内存：**
- 每个模式编译一次FSM（缓存）
- 最小运行时开销
- 与vLLM一起高效以获得高吞吐量

**准确性：**
- **100%有效输出**（由FSM保证）
- 不需要重试循环
- 确定性令牌过滤

## 资源

- **文档**：https://outlines-dev.github.io/outlines
- **GitHub**：https://github.com/outlines-dev/outlines（8k+ stars）
- **Discord**：https://discord.gg/R9DSu34mGd
- **博客**：https://blog.dottxt.co

## 另请参阅

- `references/json_generation.md` - 全面的JSON和Pydantic模式
- `references/backends.md` - 后端特定配置
- `references/examples.md` - 生产就绪示例

