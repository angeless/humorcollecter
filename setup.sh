#!/bin/bash
# setup.sh - 快速安装脚本

echo "🎭 安装 幽默感收集器..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 需要安装 Python3"
    exit 1
fi

# 创建.env文件
if [ ! -f .env ]; then
    cp .env.example .env
    echo "✅ 已创建 .env 文件，请编辑填入你的Notion信息"
else
    echo "⚠️ .env 文件已存在，跳过创建"
fi

# 设置脚本权限
chmod +x scripts/*.py

echo ""
echo "🎉 安装完成！"
echo ""
echo "下一步:"
echo "1. 编辑 .env 文件，填入 NOTION_TOKEN 和 HUMOR_DATABASE_ID"
echo "2. 运行: python3 scripts/add_humor.py '测试内容'"
