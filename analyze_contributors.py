import json

# 读取贡献者数据
with open('contributors.json', 'r', encoding='utf-8') as f:
    contributors = json.load(f)

# 打印前10名贡献者
print("=" * 60)
print("NousResearch/hermes-agent 仓库前10名贡献者")
print("=" * 60)
for i, contributor in enumerate(contributors[:10], 1):
    print(f"{i:2d}. {contributor['login']:20s} - {contributor['contributions']:3d} 次贡献")

# 查找用户Eruditi
print("\n" + "=" * 60)
print("查找用户 Eruditi")
print("=" * 60)
found = False
for i, contributor in enumerate(contributors, 1):
    if contributor['login'] == 'Eruditi':
        print(f"✓ 找到用户 Eruditi！")
        print(f"  排名: 第 {i} 名")
        print(f"  贡献数: {contributor['contributions']} 次")
        print(f"  GitHub 主页: {contributor['html_url']}")
        found = True
        break

if not found:
    print(f"✗ 用户 Eruditi 不在贡献者列表中")
    print(f"  共查询到 {len(contributors)} 名贡献者")

# 打印完整统计
print("\n" + "=" * 60)
print("统计摘要")
print("=" * 60)
print(f"总贡献者数: {len(contributors)}")
print(f"前10名贡献者总贡献: {sum(c['contributions'] for c in contributors[:10])}")
print(f"所有贡献者总贡献: {sum(c['contributions'] for c in contributors)}")
