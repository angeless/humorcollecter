---
name: humor-collector
description: 收集幽默内容并自动整理到Notion数据库，用于写段子或开放麦。支持文本、链接、图片等多种形式的内容归档。
---

# 幽默感收集器 (Humor Collector)

把看到的搞笑内容一键归档到Notion，积累写作素材库。

## 快速开始

```bash
# 添加一条幽默内容
python3 scripts/add_humor.py "这里有只小龙虾，它的名字叫Q，因为它没有钳。"

# 添加带标签的内容
python3 scripts/add_humor.py "AI说：I'm here to help. 用户说：Can you make me coffee? AI说：..." --tags "AI,咖啡,期望管理"

# 添加带来源的内容
python3 scripts/add_humor.py "程序员鼓励师其实是程序员自己" --source "小红书" --tags "程序员,自嘲"
```

## 环境变量配置

```bash
export NOTION_TOKEN="secret_xxxxxxxx"  # Notion integration token
export HUMOR_DATABASE_ID="30c994709f0b8000a284c25e1e8540a3"  # 你的Notion数据库ID
```

## Notion数据库结构

确保你的Notion数据库有以下字段：

| 字段名 | 类型 | 说明 |
|--------|------|------|
| 内容 (Content) | Title | 幽默内容文本 |
| 来源 (Source) | Select | 来源平台 |
| 标签 (Tags) | Multi-select | 分类标签 |
| 状态 (Status) | Select | 待处理/已整理/已使用 |
| 备注 (Notes) | Rich Text | 补充说明 |
| 链接 (URL) | URL | 原始链接 |
| 创建时间 (Created) | Date | 自动记录 |

## 工作流

```
[发现好笑内容]
       ↓
[执行 add_humor.py]
       ↓
[自动同步到Notion数据库]
       ↓
[积累素材库 → 写段子/开放麦]
```

## 脚本说明

| 脚本 | 用途 |
|------|------|
| `add_humor.py` | 添加幽默内容到Notion |
| `list_humor.py` | 列出最近的幽默条目 |
| `search_humor.py` | 按标签/关键词搜索 |
| `batch_import.py` | 批量导入本地文件 |

## 使用示例

### 1. 添加简单段子
```bash
python3 scripts/add_humor.py "我问AI：你能帮我写代码吗？AI说：当然。我问：那你能帮我写bug吗？AI说：你已经在写了。"
```

### 2. 添加带完整元数据
```bash
python3 scripts/add_humor.py \
  "产品经理：这个需求很简单。程序员：你行你上。产品经理：我来就我来。程序员：请。产品经理：... 还是你来吧。" \
  --tags "产品经理,程序员,期望管理" \
  --source "Twitter" \
  --url "https://twitter.com/xxx/status/xxx" \
  --notes "适合开放麦开场"
```

### 3. 从文件批量导入
```bash
# humor.txt 格式：每行一条内容
python3 scripts/batch_import.py humor.txt --tags "待分类"
```

### 4. 搜索素材
```bash
# 按标签搜索
python3 scripts/search_humor.py --tag "程序员"

# 按关键词搜索
python3 scripts/search_humor.py --keyword "AI"

# 搜索未使用的素材
python3 scripts/search_humor.py --status "待处理"
```

## Notion集成设置

### 1. 创建Integration
1. 访问 https://www.notion.so/my-integrations
2. 点击 "New integration"
3. 填写名称（如"Humor Collector"）
4. 复制生成的 Token

### 2. 连接数据库
1. 打开你的Notion数据库页面
2. 点击右上角 "..." → "Connect to"
3. 选择你的 Integration

### 3. 获取数据库ID
从Notion页面URL中提取：
```
https://www.notion.so/xxx/DATABASE_ID?v=...
                              ^^^^^^^^^^^^
```

## 扩展功能

### Discord集成
配合OpenClaw使用，监听频道中的消息：

```bash
# 当在Discord看到好笑内容，@机器人或使用命令
!humor "内容" --tags "标签"
```

### 定时整理
设置cron任务，定期将"待处理"的内容整理成段子大纲：

```bash
# 每周日晚上整理本周素材
0 21 * * 0 python3 scripts/weekly_review.py
```

## 数据导出

```bash
# 导出为Markdown（方便写作）
python3 scripts/export.py --format markdown --output ./my_jokes.md

# 导出为JSON（数据分析）
python3 scripts/export.py --format json --output ./humor_data.json
```
