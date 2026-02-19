#!/usr/bin/env python3
"""
列出最近的幽默条目
Usage: python3 list_humor.py [--limit 10] [--status 待处理]
"""

import os
import sys
import json
import argparse
from urllib import request, error

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "YOUR_NOTION_TOKEN_HERE")
DATABASE_ID = os.environ.get("HUMOR_DATABASE_ID", "YOUR_DATABASE_ID_HERE")
NOTION_VERSION = "2025-09-03"


def get_data_source_id():
    """获取data_source_id用于查询"""
    # 从数据库ID提取
    return DATABASE_ID.replace("-", "")


def list_humor(limit: int = 10, status: str = None):
    """列出幽默条目"""
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    
    # 获取data_source_id
    data_source_id = get_data_source_id()
    
    # 构建查询
    payload = {
        "page_size": limit,
        "sorts": [{"property": "创建时间", "direction": "descending"}]
    }
    
    if status:
        payload["filter"] = {
            "property": "状态",
            "select": {"equals": status}
        }
    
    req = request.Request(
        f"https://api.notion.com/v1/data_sources/{data_source_id}/query",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )
    
    try:
        with request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            return result.get("results", [])
    except error.HTTPError as e:
        print(f"❌ 查询失败: {e.read().decode()}")
        sys.exit(1)


def format_entry(entry):
    """格式化显示条目"""
    props = entry.get("properties", {})
    
    # 获取内容
    title_prop = props.get("内容", {}).get("title", [])
    content = title_prop[0].get("text", {}).get("content", "") if title_prop else ""
    
    # 获取标签
    tags_prop = props.get("标签", {}).get("multi_select", [])
    tags = ", ".join([t.get("name", "") for t in tags_prop]) if tags_prop else "无"
    
    # 获取状态
    status = props.get("状态", {}).get("select", {}).get("name", "未知")
    
    # 获取来源
    source = props.get("来源", {}).get("select", {}).get("name", "未标注")
    
    return f"""
━━━━━━━━━━━━━━━━━━━━
📄 {content[:80]}{'...' if len(content) > 80 else ''}
🏷️ 标签: {tags}
📍 来源: {source} | 状态: {status}
"""


def main():
    parser = argparse.ArgumentParser(description="列出幽默条目")
    parser.add_argument("--limit", type=int, default=10, help="返回数量")
    parser.add_argument("--status", help="按状态筛选")
    
    args = parser.parse_args()
    
    results = list_humor(limit=args.limit, status=args.status)
    
    print(f"📋 找到 {len(results)} 条记录:\n")
    for entry in results:
        print(format_entry(entry))


if __name__ == "__main__":
    main()
