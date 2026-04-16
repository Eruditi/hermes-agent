
---
name: guidance
description: 使用正则表达式和语法控制LLM输出，保证有效的JSON/XML/代码生成，强制执行结构化格式，并使用Guidance构建多步骤工作流程 - Microsoft Research的约束生成框架
version: 1.0.0
author: Orchestra Research
license: MIT
dependencies: [guidance, transformers]
metadata:
  hermes:
    tags: [提示工程, Guidance, 约束生成, 结构化输出, JSON验证, 语法, Microsoft Research, 格式强制执行, 多步骤工作流程]

---

# Guidance: 约束LLM生成

## 何时使用此技能

当你需要时使用Guidance：
- **使用正则表达式或语法控制LLM输出语法**
- **保证有效的JSON/XML/代码** 生成
- **减少延迟** 与传统提示方法相比
- **强制执行结构化格式**（日期、电子邮件、ID等）
- **构建多步骤工作流程** 带有Pythonic控制流
- **通过语法约束防止无效输出**

**GitHub Stars**：18,000+ | **来自**：Microsoft Research

## 安装

```bash
# 基本安装
pip install guidance

# 带特定后端
pip install guidance[transformers]  # Hugging Face模型
pip install guidance[llama_cpp]     # llama.cpp模型
```

## 快速开始

### 基本示例：结构化生成

```python
from guidance import models, gen

# 加载模型（支持OpenAI、Transformers、llama.cpp）
lm = models.OpenAI("gpt-4")

# 生成带约束
result = lm + "The capital of France is " + gen("capital", max_tokens=5)

print(result["capital"])  # "Paris"
```

### 使用Anthropic Claude

```python
from guidance import models, gen, system, user, assistant

# 配置Claude
lm = models.Anthropic("claude-sonnet-4-5-20250929")

# 使用上下文管理器进行聊天格式
with system():
    lm += "You are a helpful assistant."

with user():
    lm += "What is the capital of France?"

with assistant():
    lm += gen(max_tokens=20)
```

## 核心概念

### 1. 上下文管理器

Guidance使用Pythonic上下文管理器进行聊天式交互。

```python
from guidance import system, user, assistant, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# 系统消息
with system():
    lm += "You are a JSON generation expert."

# 用户消息
with user():
    lm += "Generate a person object with name and age."

# 助手响应
with assistant():
    lm += gen("response", max_tokens=100)

print(lm["response"])
```

**优势：**
- 自然聊天流
- 清晰的角色分离
- 易于阅读和维护

### 2. 约束生成

Guidance使用正则表达式或语法确保输出匹配指定的模式。

#### 正则表达式约束

```python
from guidance import models, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# 约束为有效的电子邮件格式
lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# 约束为日期格式（YYYY-MM-DD）
lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}")

# 约束为电话号码
lm += "Phone: " + gen("phone", regex=r"\d{3}-\d{3}-\d{4}")

print(lm["email"])  # 保证有效的电子邮件
print(lm["date"])   # 保证YYYY-MM-DD格式
```

**工作原理：**
- 正则表达式在令牌级别转换为语法
- 在生成期间过滤无效令牌
- 模型只能产生匹配的输出

#### 选择约束

```python
from guidance import models, gen, select

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# 约束为特定选择
lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")

# 多项选择
lm += "Best answer: " + select(
    ["A) Paris", "B) London", "C) Berlin", "D) Madrid"],
    name="answer"
)

print(lm["sentiment"])  # 之一：positive, negative, neutral
print(lm["answer"])     # 之一：A, B, C, 或 D
```

### 3. 令牌修复

Guidance自动"修复"提示和生成之间的令牌边界。

**问题：** 令牌化会创建不自然的边界。

```python
# 没有令牌修复
prompt = "The capital of France is "
# 最后一个令牌：" is "
# 第一个生成的令牌可能是 " Par"（带前导空格）
# 结果："The capital of France is  Paris"（双空格！）
```

**解决方案：** Guidance后退一个令牌并重新生成。

```python
from guidance import models, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# 默认启用令牌修复
lm += "The capital of France is " + gen("capital", max_tokens=5)
# 结果："The capital of France is Paris"（正确间距）
```

**优势：**
- 自然的文本边界
- 没有尴尬的间距问题
- 更好的模型性能（看到自然的令牌序列）

### 4. 基于语法的生成

使用上下文无关语法定义复杂结构。

```python
from guidance import models, gen

lm = models.Anthropic("claude-sonnet-4-5-20250929")

# JSON语法（简化）
json_grammar = """
{
    "name": &lt;gen name regex="[A-Za-z ]+" max_tokens=20&gt;,
    "age": &lt;gen age regex="[0-9]+" max_tokens=3&gt;,
    "email": &lt;gen email regex="[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\\.[a-zA-Z]{2,}" max_tokens=50&gt;
}
"""

# 生成有效的JSON
lm += gen("person", grammar=json_grammar)

print(lm["person"])  # 保证有效的JSON结构
```

**使用场景：**
- 复杂的结构化输出
- 嵌套数据结构
- 编程语言语法
- 特定领域语言

### 5. Guidance函数

使用 `@guidance` 装饰器创建可重用的生成模式。

```python
from guidance import guidance, gen, models

@guidance
def generate_person(lm):
    """生成一个带姓名和年龄的人。"""
    lm += "Name: " + gen("name", max_tokens=20, stop="\n")
    lm += "\nAge: " + gen("age", regex=r"[0-9]+", max_tokens=3)
    return lm

# 使用函数
lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = generate_person(lm)

print(lm["name"])
print(lm["age"])
```

**有状态函数：**

```python
@guidance(stateless=False)
def react_agent(lm, question, tools, max_rounds=5):
    """带工具使用的ReAct代理。"""
    lm += f"Question: {question}\n\n"

    for i in range(max_rounds):
        # 思考
        lm += f"Thought {i+1}: " + gen("thought", stop="\n")

        # 行动
        lm += "\nAction: " + select(list(tools.keys()), name="action")

        # 执行工具
        tool_result = tools[lm["action"]]()
        lm += f"\nObservation: {tool_result}\n\n"

        # 检查是否完成
        lm += "Done? " + select(["Yes", "No"], name="done")
        if lm["done"] == "Yes":
            break

    # 最终答案
    lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
    return lm
```

## 后端配置

### Anthropic Claude

```python
from guidance import models

lm = models.Anthropic(
    model="claude-sonnet-4-5-20250929",
    api_key="your-api-key"  # 或设置ANTHROPIC_API_KEY环境变量
)
```

### OpenAI

```python
lm = models.OpenAI(
    model="gpt-4o-mini",
    api_key="your-api-key"  # 或设置OPENAI_API_KEY环境变量
)
```

### 本地模型（Transformers）

```python
from guidance.models import Transformers

lm = Transformers(
    "microsoft/Phi-4-mini-instruct",
    device="cuda"  # 或 "cpu"
)
```

### 本地模型（llama.cpp）

```python
from guidance.models import LlamaCpp

lm = LlamaCpp(
    model_path="/path/to/model.gguf",
    n_ctx=4096,
    n_gpu_layers=35
)
```

## 常见模式

### 模式1：JSON生成

```python
from guidance import models, gen, system, user, assistant

lm = models.Anthropic("claude-sonnet-4-5-20250929")

with system():
    lm += "You generate valid JSON."

with user():
    lm += "Generate a user profile with name, age, and email."

with assistant():
    lm += """{
    "name": """ + gen("name", regex=r'"[A-Za-z ]+"', max_tokens=30) + """,
    "age": """ + gen("age", regex=r"[0-9]+", max_tokens=3) + """,
    "email": """ + gen("email", regex=r'"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}"', max_tokens=50) + """
}"""

print(lm)  # 保证有效的JSON
```

### 模式2：分类

```python
from guidance import models, gen, select

lm = models.Anthropic("claude-sonnet-4-5-20250929")

text = "This product is amazing! I love it."

lm += f"Text: {text}\n"
lm += "Sentiment: " + select(["positive", "negative", "neutral"], name="sentiment")
lm += "\nConfidence: " + gen("confidence", regex=r"[0-9]+", max_tokens=3) + "%"

print(f"Sentiment: {lm['sentiment']}")
print(f"Confidence: {lm['confidence']}%")
```

### 模式3：多步骤推理

```python
from guidance import models, gen, guidance

@guidance
def chain_of_thought(lm, question):
    """生成带逐步推理的答案。"""
    lm += f"Question: {question}\n\n"

    # 生成多个推理步骤
    for i in range(3):
        lm += f"Step {i+1}: " + gen(f"step_{i+1}", stop="\n", max_tokens=100) + "\n"

    # 最终答案
    lm += "\nTherefore, the answer is: " + gen("answer", max_tokens=50)

    return lm

lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = chain_of_thought(lm, "What is 15% of 200?")

print(lm["answer"])
```

### 模式4：ReAct代理

```python
from guidance import models, gen, select, guidance

@guidance(stateless=False)
def react_agent(lm, question):
    """带工具使用的ReAct代理。"""
    tools = {
        "calculator": lambda expr: eval(expr),
        "search": lambda query: f"Search results for: {query}",
    }

    lm += f"Question: {question}\n\n"

    for round in range(5):
        # 思考
        lm += f"Thought: " + gen("thought", stop="\n") + "\n"

        # 行动选择
        lm += "Action: " + select(["calculator", "search", "answer"], name="action")

        if lm["action"] == "answer":
            lm += "\nFinal Answer: " + gen("answer", max_tokens=100)
            break

        # 行动输入
        lm += "\nAction Input: " + gen("action_input", stop="\n") + "\n"

        # 执行工具
        if lm["action"] in tools:
            result = tools[lm["action"]](lm["action_input"])
            lm += f"Observation: {result}\n\n"

    return lm

lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = react_agent(lm, "What is 25 * 4 + 10?")
print(lm["answer"])
```

### 模式5：数据提取

```python
from guidance import models, gen, guidance

@guidance
def extract_entities(lm, text):
    """从文本中提取结构化实体。"""
    lm += f"Text: {text}\n\n"

    # 提取人物
    lm += "Person: " + gen("person", stop="\n", max_tokens=30) + "\n"

    # 提取组织
    lm += "Organization: " + gen("organization", stop="\n", max_tokens=30) + "\n"

    # 提取日期
    lm += "Date: " + gen("date", regex=r"\d{4}-\d{2}-\d{2}", max_tokens=10) + "\n"

    # 提取位置
    lm += "Location: " + gen("location", stop="\n", max_tokens=30) + "\n"

    return lm

text = "Tim Cook announced at Apple Park on 2024-09-15 in Cupertino."

lm = models.Anthropic("claude-sonnet-4-5-20250929")
lm = extract_entities(lm, text)

print(f"Person: {lm['person']}")
print(f"Organization: {lm['organization']}")
print(f"Date: {lm['date']}")
print(f"Location: {lm['location']}")
```

## 最佳实践

### 1. 对格式验证使用正则表达式

```python
# ✅ 好：正则表达式确保有效格式
lm += "Email: " + gen("email", regex=r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")

# ❌ 不好：自由生成可能产生无效电子邮件
lm += "Email: " + gen("email", max_tokens=50)
```

### 2. 对固定类别使用select()

```python
# ✅ 好：保证有效的类别
lm += "Status: " + select(["pending", "approved", "rejected"], name="status")

# ❌ 不好：可能生成拼写错误或无效值
lm += "Status: " + gen("status", max_tokens=20)
```

### 3. 利用令牌修复

```python
# 默认启用令牌修复
# 不需要特殊操作 - 只需自然拼接
lm += "The capital is " + gen("capital")  # 自动修复
```

### 4. 使用stop序列

```python
# ✅ 好：在换行处停止以用于单行输出
lm += "Name: " + gen("name", stop="\n")

# ❌ 不好：可能生成多行
lm += "Name: " + gen("name", max_tokens=50)
```

### 5. 创建可重用函数

```python
# ✅ 好：可重用模式
@guidance
def generate_person(lm):
    lm += "Name: " + gen("name", stop="\n")
    lm += "\nAge: " + gen("age", regex=r"[0-9]+")
    return lm

# 多次使用
lm = generate_person(lm)
lm += "\n\n"
lm = generate_person(lm)
```

### 6. 平衡约束

```python
# ✅ 好：合理的约束
lm += gen("name", regex=r"[A-Za-z ]+", max_tokens=30)

# ❌ 太严格：可能失败或非常慢
lm += gen("name", regex=r"^(John|Jane)$", max_tokens=10)
```

## 与替代方案的比较

| 功能 | Guidance | Instructor | Outlines | LMQL |
|---------|----------|------------|----------|------|
| 正则表达式约束 | ✅ 是 | ❌ 否 | ✅ 是 | ✅ 是 |
| 语法支持 | ✅ CFG | ❌ 否 | ✅ CFG | ✅ CFG |
| Pydantic验证 | ❌ 否 | ✅ 是 | ✅ 是 | ❌ 否 |
| 令牌修复 | ✅ 是 | ❌ 否 | ✅ 是 | ❌ 否 |
| 本地模型 | ✅ 是 | ⚠️ 有限 | ✅ 是 | ✅ 是 |
| API模型 | ✅ 是 | ✅ 是 | ⚠️ 有限 | ✅ 是 |
| Pythonic语法 | ✅ 是 | ✅ 是 | ✅ 是 | ❌ 类SQL |
| 学习曲线 | 低 | 低 | 中 | 高 |

**何时选择Guidance：**
- 需要正则表达式/语法约束
- 想要令牌修复
- 构建带控制流的复杂工作流程
- 使用本地模型（Transformers、llama.cpp）
- 更喜欢Pythonic语法

**何时选择替代方案：**
- Instructor：需要自动重试的Pydantic验证
- Outlines：需要JSON模式验证
- LMQL：更喜欢声明性查询语法

## 性能特性

**延迟减少：**
- 对于约束输出，比传统提示快30-50%
- 令牌修复减少不必要的重新生成
- 语法约束防止无效令牌生成

**内存使用：**
- 与无约束生成相比，最小开销
- 语法编译在首次使用后缓存
- 推理时高效的令牌过滤

**令牌效率：**
- 防止在无效输出上浪费令牌
- 不需要重试循环
- 直接路径到有效输出

## 资源

- **文档**：https://guidance.readthedocs.io
- **GitHub**：https://github.com/guidance-ai/guidance (18k+ stars)
- **笔记本**：https://github.com/guidance-ai/guidance/tree/main/notebooks
- **Discord**：社区支持可用

## 另请参阅

- `references/constraints.md` - 全面的正则表达式和语法模式
- `references/backends.md` - 后端特定配置
- `references/examples.md` - 生产就绪示例

