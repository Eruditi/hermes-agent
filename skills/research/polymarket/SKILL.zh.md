---
name: polymarket
description: 查询Polymarket预测市场数据 — 搜索市场、获取价格、订单簿和价格历史。通过公共REST API只读，无需API密钥。
version: 1.0.0
author: Hermes Agent + Teknium
tags: [polymarket, 预测市场, 市场数据, 交易]
---

# Polymarket — 预测市场数据

使用Polymarket的公共REST API查询预测市场数据。所有端点都是只读的，不需要身份验证。

有关完整的端点参考和curl示例，请参阅`references/api-endpoints.md`。

## 何时使用

- 用户询问预测市场、投注赔率或事件概率
- 用户想知道"X发生的几率是多少？"
- 用户特别询问Polymarket
- 用户想要市场价格、订单簿数据或价格历史
- 用户要求监控或跟踪预测市场变动

## 关键概念

- **事件**包含一个或多个**市场**（一对多关系）
- **市场**是二元结果，是/否价格在0.00和1.00之间
- 价格就是概率：价格0.65意味着市场认为有65%的可能性
- `outcomePrices`字段：JSON编码数组，如`["0.80", "0.20"]`
- `clobTokenIds`字段：两个令牌ID的JSON编码数组[是，否]，用于价格/订单簿查询
- `conditionId`字段：用于价格历史查询的十六进制字符串
- 交易量以USDC（美元）为单位

## 三个公共API

1. **Gamma API** 在`gamma-api.polymarket.com` — 发现、搜索、浏览
2. **CLOB API** 在`clob.polymarket.com` — 实时价格、订单簿、历史
3. **Data API** 在`data-api.polymarket.com` — 交易、未平仓合约

## 典型工作流程

当用户询问预测市场赔率时：

1. **搜索**使用Gamma API public-search端点与他们的查询
2. **解析**响应 — 提取事件及其嵌套市场
3. **呈现**市场问题、当前价格作为百分比以及交易量
4. **深入**如果被要求 — 使用clobTokenIds获取订单簿，conditionId获取历史

## 呈现结果

为了可读性，将价格格式化为百分比：
- outcomePrices `["0.652", "0.348"]`变为"是：65.2%，否：34.8%"
- 始终显示市场问题和概率
- 可用时包含交易量

示例：`"X会发生吗？" — 65.2% 是（120万美元交易量）`

## 解析双重编码字段

Gamma API将`outcomePrices`、`outcomes`和`clobTokenIds`作为JSON响应中的JSON字符串返回（双重编码）。使用Python处理时，用`json.loads(market['outcomePrices'])`解析它们以获取实际数组。

## 速率限制

宽松 — 正常使用不太可能命中：
- Gamma：每10秒4,000个请求（常规）
- CLOB：每10秒9,000个请求（常规）
- Data：每10秒1,000个请求（常规）

## 限制

- 此技能是只读的 — 它不支持下单交易
- 交易需要基于钱包的加密身份验证（EIP-712签名）
- 一些新市场可能有空的价格历史
- 地理限制适用于交易，但只读数据可全球访问
