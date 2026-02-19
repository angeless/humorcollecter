#!/usr/bin/env python3
"""
搜索幽默内容
Usage: python3 search_humor.py [--tag "程序员"] [--keyword "AI"]
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
    return DATABASE_ID.replace("-", "")


def search_by_tag(tag: str):
    """按标签搜索"""
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    
    data_source_id = get_data_source_id()
    
    payload = {
        "filter": {
            "property": "标签",
            "multi_select": {"contains": tag}
        },
        "sorts": [{"property": "创建时间", "direction": "descending"}]
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
        print(f"❌ 搜索失败: {e.read().decode()}")
        return []


def format_entry(entry):
    """格式化显示条目"""
    props = entry.get("properties", {})
    
    title_prop = props.get("内容", {}).get("title", [])
    content = title_prop[0].get("text", {}).get("content", "") if title_prop else ""
    
    tags_prop = props.get("标签", {}).get("multi_select", [])
    tags = ", ".join([t.get("name", "") for t in tags_prop]) if tags_prop else "无"
    
    status = props.get("状态", {}).get("select", {}).get("name", "未知")
    
    return f"""
━━━━━━━━━━━━━━━━━━━━
📄 {content}
🏷️ 标签: {tags} | 状态: {status}
"""


def main():
    parser = argparse.ArgumentParser(description="搜索幽默内容")
    parser.add_argument("--tag", help="按标签搜索")
    parser.add_argument("--keyword", help="按关键词搜索（本地过滤）")
    parser.add_argument("--status", help="按状态筛选")
    
    args = parser.parse_args()
    
    if args.tag:
        print(f"🔍 搜索标签: {args.tag}\n")
        results = search_by_tag(args.tag)
        print(f"找到 {len(results)} 条结果:\n")
        for entry in results:
            print(format_entry(entry))
    elif args.keyword:
        print("⚠️ 关键词搜索需要获取所有内容后本地过滤，暂不支持")
        print("💡 建议使用Notion的搜索功能或按标签分类")
    else:
        print("请指定搜索条件: --tag 或 --keyword")


if __name__ == "__main__":
    main()
