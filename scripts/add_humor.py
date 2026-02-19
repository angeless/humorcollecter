#!/usr/bin/env python3
"""
添加幽默内容到Notion数据库
Usage: python3 add_humor.py "内容" [--tags "标签1,标签2"] [--source "来源"] [--url "链接"] [--notes "备注"]
"""

import os
import sys
import argparse
import json
from datetime import datetime
from urllib import request, error

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "YOUR_NOTION_TOKEN_HERE")
DATABASE_ID = os.environ.get("HUMOR_DATABASE_ID", "YOUR_DATABASE_ID_HERE")
NOTION_VERSION = "2025-09-03"


def add_humor(content: str, tags: list = None, source: str = None, 
              url: str = None, notes: str = None):
    """添加幽默内容到Notion数据库"""
    
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    
    # 构建属性
    properties = {
        "内容": {"title": [{"text": {"content": content}}]},
        "创建时间": {"date": {"start": datetime.now().isoformat()[:10]}}
    }
    
    if source:
        properties["来源"] = {"select": {"name": source}}
    
    if tags:
        properties["标签"] = {"multi_select": [{"name": tag.strip()} for tag in tags]}
    
    if url:
        properties["链接"] = {"url": url}
    
    if notes:
        properties["备注"] = {"rich_text": [{"text": {"content": notes}}]}
    
    # 默认状态为"待处理"
    properties["状态"] = {"select": {"name": "待处理"}}
    
    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": properties
    }
    
    req = request.Request(
        "https://api.notion.com/v1/pages",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )
    
    try:
        with request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✅ 已添加到Notion: {content[:50]}...")
            return result
    except error.HTTPError as e:
        print(f"❌ 添加失败: {e.read().decode()}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="添加幽默内容到Notion")
    parser.add_argument("content", help="幽默内容文本")
    parser.add_argument("--tags", help="标签，逗号分隔")
    parser.add_argument("--source", help="来源平台")
    parser.add_argument("--url", help="原始链接")
    parser.add_argument("--notes", help="备注说明")
    
    args = parser.parse_args()
    
    tags = args.tags.split(",") if args.tags else []
    
    add_humor(
        content=args.content,
        tags=tags,
        source=args.source,
        url=args.url,
        notes=args.notes
    )


if __name__ == "__main__":
    main()
