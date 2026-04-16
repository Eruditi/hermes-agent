---
name: find-nearby
description: 使用OpenStreetMap查找附近的地方（餐厅、咖啡馆、酒吧、药店等）。支持坐标、地址、城市、邮编或Telegram位置引脚。无需API密钥。
version: 1.0.0
metadata:
  hermes:
    tags: [location, maps, nearby, places, restaurants, local, 位置, 地图, 附近, 地方, 餐厅, 本地]
    related_skills: []
---

# Find Nearby — 本地地点发现

查找任何位置附近的餐厅、咖啡馆、酒吧、药店和其他地方。使用OpenStreetMap（免费，无需API密钥）。支持：

- **坐标**来自Telegram位置引脚（对话中的纬度/经度）
- **地址**（"靠近123 Main St, Springfield"）
- **城市**（"奥斯汀市中心的餐厅"）
- **邮编**（"90210附近的药店"）
- **地标**（"时代广场附近的咖啡馆"）

## 快速参考

```bash
# 通过坐标（来自Telegram位置引脚或用户提供）
python3 SKILL_DIR/scripts/find_nearby.py --lat <LAT> --lon <LON> --type restaurant --radius 1500

# 通过地址、城市或地标（自动地理编码）
python3 SKILL_DIR/scripts/find_nearby.py --near "Times Square, New York" --type cafe

# 多种地点类型
python3 SKILL_DIR/scripts/find_nearby.py --near "downtown austin" --type restaurant --type bar --limit 10

# JSON输出
python3 SKILL_DIR/scripts/find_nearby.py --near "90210" --type pharmacy --json
```

### 参数

| 标志 | 描述 | 默认值 |
|------|------|--------|
| `--lat`, `--lon` | 精确坐标 | — |
| `--near` | 地址、城市、邮编或地标（地理编码） | — |
| `--type` | 地点类型（可重复多次） | restaurant |
| `--radius` | 搜索半径（米） | 1500 |
| `--limit` | 最大结果数 | 15 |
| `--json` | 机器可读的JSON输出 | 关闭 |

### 常见地点类型

`restaurant`, `cafe`, `bar`, `pub`, `fast_food`, `pharmacy`, `hospital`, `bank`, `atm`, `fuel`, `parking`, `supermarket`, `convenience`, `hotel`

## 工作流程

1. **获取位置**。查找Telegram引脚的坐标（`latitude: ... / longitude: ...`），或向用户询问地址/城市/邮编。

2. **询问偏好**（仅在未说明时）：地点类型，愿意走多远，任何具体要求（菜系，"现在营业"等）。

3. **运行脚本**，使用适当的标志。如果需要以编程方式处理结果，使用`--json`。

4. **呈现结果**，包括名称、距离和Google Maps链接。如果用户询问营业时间或"现在营业"，检查结果中的`hours`字段 — 如果缺失或不清楚，使用`web_search`验证。

5. **获取路线**，使用结果中的`directions_url`，或构造：`https://www.google.com/maps/dir/?api=1&origin=<LAT>,<LON>&destination=<LAT>,<LON>`

## 提示

- 如果结果稀疏，扩大半径（1500 → 3000米）
- 对于"现在营业"请求：检查结果中的`hours`字段，使用`web_search`交叉引用以确保准确性，因为OSM营业时间并不总是完整的
- 仅邮编在全球范围内可能有歧义 — 如果结果看起来错误，提示用户提供国家/州
- 该脚本使用社区维护的OpenStreetMap数据；覆盖范围因地区而异