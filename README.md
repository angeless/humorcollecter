# 幽默感收集器 (Humor Collector) 🎭

把看到的搞笑内容一键归档到Notion，积累写作素材库。

## 功能

- 📝 快速添加幽默内容到Notion数据库
- 🏷️ 自动分类标签管理
- 🔍 按标签/来源搜索素材
- 📦 批量导入本地文件
- 🎤 为开放麦和段子写作积累素材

## 快速开始

### 1. 安装

```bash
git clone https://github.com/YOUR_USERNAME/humor-collector.git
cd humor-collector
cp .env.example .env
# 编辑 .env 填入你的Notion信息
```

### 2. 配置Notion

1. 访问 https://www.notion.so/my-integrations 创建Integration
2. 复制 Token 到 `.env` 文件
3. 在Notion中分享数据库给你的Integration

### 3. 使用

```bash
# 添加一条幽默内容
python3 scripts/add_humor.py "这里有只小龙虾，它的名字叫Q，因为它没有钳。"

# 添加带标签的内容
python3 scripts/add_humor.py "段子内容" --tags "AI,程序员"

# 查看最近的素材
python3 scripts/list_humor.py --limit 5

# 按标签搜索
python3 scripts/search_humor.py --tag "程序员"
```

## 数据库结构

在Notion中创建数据库，包含以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 内容 | Title | 幽默内容文本 |
| 来源 | Select | 来源平台 |
| 标签 | Multi-select | 分类标签 |
| 状态 | Select | 待处理/已整理/已使用 |
| 备注 | Rich text | 补充说明 |
| 链接 | URL | 原始链接 |
| 创建时间 | Date | 自动记录 |

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `add_humor.py` | 添加单条幽默内容 |
| `list_humor.py` | 列出最近的条目 |
| `search_humor.py` | 按标签搜索 |
| `batch_import.py` | 批量导入文件 |

## License

MIT
