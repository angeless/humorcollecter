#!/usr/bin/env python3
"""
批量导入本地文件中的幽默内容
Usage: python3 batch_import.py humor.txt [--tags "待分类"]

文件格式（每行一条）:
---
这里有只小龙虾，它的名字叫Q，因为它没有钳。
AI说：I'm here to help. 用户说：Can you make me coffee?
---
"""

import os
import sys
import argparse
from add_humor import add_humor


def batch_import(file_path: str, tags: list = None, source: str = None):
    """批量导入文件中的内容"""
    
    if not os.path.exists(file_path):
        print(f"❌ 文件不存在: {file_path}")
        sys.exit(1)
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = [line.strip() for line in f if line.strip()]
    
    print(f"📁 读取到 {len(lines)} 条内容\n")
    
    success_count = 0
    for i, content in enumerate(lines, 1):
        print(f"[{i}/{len(lines)}] ", end="")
        try:
            add_humor(content=content, tags=tags, source=source)
            success_count += 1
        except Exception as e:
            print(f"❌ 失败: {e}")
    
    print(f"\n✅ 导入完成: {success_count}/{len(lines)} 条成功")


def main():
    parser = argparse.ArgumentParser(description="批量导入幽默内容")
    parser.add_argument("file", help="文件路径")
    parser.add_argument("--tags", help="标签，逗号分隔")
    parser.add_argument("--source", help="来源平台")
    
    args = parser.parse_args()
    
    tags = args.tags.split(",") if args.tags else []
    
    batch_import(file_path=args.file, tags=tags, source=args.source)


if __name__ == "__main__":
    main()
