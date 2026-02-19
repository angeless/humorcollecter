#!/usr/bin/env python3
"""
整理并预览幽默内容，确认后添加到Notion
Usage: 
  python3 humor_cli.py preview "原始内容" [--tags "标签"]    # 预览整理结果
  python3 humor_cli.py add "内容" [--tags "标签"]           # 直接添加
  python3 humor_cli.py draft                                    # 进入交互模式
"""

import os
import sys
import argparse
import json
import re
from datetime import datetime
from urllib import request, error

NOTION_TOKEN = os.environ.get("NOTION_TOKEN", "YOUR_NOTION_TOKEN_HERE")
DATABASE_ID = os.environ.get("HUMOR_DATABASE_ID", "YOUR_DATABASE_ID_HERE")
NOTION_VERSION = "2025-09-03"


class HumorEntry:
    """幽默内容条目"""
    
    def __init__(self, raw_content: str, source: str = None, url: str = None):
        self.raw = raw_content
        self.source = source or self._detect_source(raw_content)
        self.url = url
        self.tags = []
        self.notes = ""
        self.structured = self._structure_content(raw_content)
        
    def _detect_source(self, content: str) -> str:
        """自动检测来源"""
        if "reddit" in content.lower() or "u/" in content:
            return "Reddit"
        elif "twitter" in content.lower() or "x.com" in content:
            return "Twitter"
        elif "小红书" in content:
            return "小红书"
        elif "抖音" in content:
            return "抖音"
        return "其他"
    
    def _structure_content(self, content: str) -> dict:
        """结构化解析内容"""
        structured = {
            "original": content,
            "title": "",
            "setup": "",      # 铺垫
            "punchline": "",  # 笑点
            "context": "",    # 背景
            "dialogue": []    # 对话形式
        }
        
        # 检测是否为对话形式
        if "•" in content or "网友说" in content or "回复" in content:
            lines = self._parse_thread(content)
            structured["dialogue"] = lines
            structured["title"] = lines[0]["content"][:50] if lines else content[:50]
        else:
            # 单条内容
            structured["title"] = content[:50]
            structured["punchline"] = content
            
        return structured
    
    def _parse_thread(self, content: str) -> list:
        """解析Reddit/论坛串 - 按用户名分割"""
        lines = []
        
        # Reddit格式: 用户名 • Xd ago 内容... u/下一个用户名
        # 分割模式: 匹配 (u/)用户名 + 时间标记
        import re
        
        # 清理多余的avatar文本
        content = re.sub(r'\s+avatar\s+', ' ', content)
        
        # 找到所有发言位置
        # 模式: 可选的u/ + 用户名 + 可选的avatar + • + 时间 + ago
        pattern = r'(?:u/)?([\w\-_]+)(?:\s+avatar)?\s*•\s*(\d+d?\s*ago)'
        matches = list(re.finditer(pattern, content))
        
        for i, match in enumerate(matches):
            author = match.group(1)
            start_pos = match.end()
            end_pos = matches[i + 1].start() if i + 1 < len(matches) else len(content)
            text = content[start_pos:end_pos].strip()
            
            # 清理投票标记和下一个用户名前缀
            text = re.sub(r'\s*Upvote\s*\d+\s*Downvote\s*Reply\s*', ' ', text)
            text = re.sub(r'\s*More replies\s*', ' ', text)
            text = re.sub(r'\s*u/\w+\s*avatar\s*', ' ', text)  # 移除下一个用户的avatar标记
            text = text.strip()
            
            if text:
                lines.append({
                    "author": author,
                    "content": text,
                    "type": "reply"
                })
        
        # 如果没匹配到，按原始方式处理
        if not lines:
            # 简单按行分割
            for line in content.split('\n'):
                line = line.strip()
                if line and len(line) > 10:
                    lines.append({"author": "", "content": line, "type": "content"})
        
        return lines
    
    def suggest_tags(self) -> list:
        """智能推荐标签"""
        content_lower = self.raw.lower()
        suggestions = []
        
        tag_map = {
            "polymarket": "Polymarket",
            "crypto": "加密货币",
            "bitcoin": "比特币",
            "交易": "交易",
            "程序员": "程序员",
            "ai": "AI",
            "gpt": "AI",
            "投资": "投资",
            "tax": "税务",
            "fee": "手续费",
            "产品经理": "产品经理",
            "老板": "职场",
            " dating": " dating",
            "约会": " dating",
            "父母": "家庭"
        }
        
        for keyword, tag in tag_map.items():
            if keyword in content_lower and tag not in suggestions:
                suggestions.append(tag)
        
        # 根据来源添加标签
        if self.source == "Reddit":
            suggestions.append("Reddit神回复")
        elif self.source == "Twitter":
            suggestions.append("推特")
            
        return suggestions
    
    def suggest_topics(self) -> list:
        """推荐适配的开放麦主题"""
        content_lower = self.raw.lower()
        topics = []
        
        # 主题映射
        topic_keywords = {
            "投资预期": ["polymarket", "crypto", "bitcoin", "交易", "fee", "tax", "投资"],
            "职场吐槽": ["程序员", "产品经理", "老板", "加班", "需求"],
            "AI时代": ["ai", "gpt", "chatgpt", "人工智能"],
            " dating困境": [" dating", "约会", "单身", "tinder"],
            "生活观察": ["通胀", "物价", "消费"]
        }
        
        for topic, keywords in topic_keywords.items():
            if any(kw in content_lower for kw in keywords):
                topics.append(topic)
        
        return topics if topics else ["通用话题"]
    
    def analyze_structure(self) -> dict:
        """分析笑点结构"""
        structure = {
            "形式": "",
            "铺垫": "",
            "笑点": "",
            "节奏": ""
        }
        
        if self.structured["dialogue"] and len(self.structured["dialogue"]) >= 2:
            structure["形式"] = "对话递进"
            structure["铺垫"] = self.structured["dialogue"][0]["content"][:50] if self.structured["dialogue"] else ""
            structure["笑点"] = "层层叠加的成本吐槽"
            structure["节奏"] = f"{len(self.structured['dialogue'])}轮递进"
        else:
            structure["形式"] = "单句"
            structure["笑点"] = self.raw[:50]
            
        return structure
    
    def suggest_adaptation(self) -> str:
        """改编建议"""
        suggestions = []
        
        if self.structured["dialogue"]:
            suggestions.append("保留对话形式，可删减为3-4轮保留节奏")
            
        topics = self.suggest_topics()
        if "投资预期" in topics:
            suggestions.append("可类比到：炒股/买房/创业等任何'看起来赚了实际亏了'的场景")
            suggestions.append("开场：你们有没有觉得自己赚了钱...")
            
        elif "职场吐槽" in topics:
            suggestions.append("可代入自身经历增强真实感")
            
        return " | ".join(suggestions) if suggestions else "可直接使用"
    
    def suggest_notes(self) -> str:
        """智能推荐备注"""
        notes = []
        
        if self.structured["dialogue"]:
            notes.append("对话形式，层层递进")
        
        if "fee" in self.raw.lower() or "税" in self.raw:
            notes.append("预期管理/成本意识")
            
        return "；".join(notes) if notes else ""
    
    def format_preview(self) -> str:
        """格式化预览 - 开放麦优化版"""
        structure = self.analyze_structure()
        topics = self.suggest_topics()
        
        lines = [
            "=" * 50,
            "🎤 开放麦素材整理",
            "=" * 50,
            "",
            f"📝 来源: {self.source}",
            f"🏷️ 标签: {', '.join(self.suggest_tags())}",
            f"🎯 适配主题: {', '.join(topics)}",
            "",
            "📊 笑点结构:",
            f"  形式: {structure['形式']}",
            f"  节奏: {structure['节奏']}",
            "",
            "📄 内容:",
            "-" * 40,
        ]
        
        if self.structured["dialogue"]:
            for i, item in enumerate(self.structured["dialogue"], 1):
                author = f"[{item['author']}] " if item['author'] else ""
                content = item['content']
                lines.append(f"  {i}. {author}{content}")
        else:
            lines.append(f"  {self.structured['punchline']}")
        
        lines.extend([
            "",
            "🎭 改编建议:",
            f"  {self.suggest_adaptation()}",
            "",
            "💡 备注:",
            f"  {self.suggest_notes() or '可直接使用'}",
            "",
            "=" * 50,
        ])
        
        return "\n".join(lines)
    
    def to_notion_payload(self, tags: list = None, notes: str = None) -> dict:
        """生成Notion API payload"""
        # 使用推荐标签 + 用户指定标签
        final_tags = list(set((tags or []) + self.suggest_tags()))
        final_notes = notes or self.suggest_notes()
        
        # 构建结构化内容 - 保留完整原文
        content_text = self.raw
        
        properties = {
            "内容": {"title": [{"text": {"content": content_text[:100]}}]},
            "来源": {"select": {"name": self.source}},
            "标签": {"multi_select": [{"name": t} for t in final_tags]},
            "状态": {"select": {"name": "待处理"}},
            "创建时间": {"date": {"start": datetime.now().isoformat()[:10]}},
            "备注": {"rich_text": [{"text": {"content": final_notes}}]}
        }
        
        if self.url:
            properties["链接"] = {"url": self.url}
            
        return {
            "parent": {"database_id": DATABASE_ID},
            "properties": properties
        }
    
    def _format_dialogue_for_notion(self) -> str:
        """格式化对话为Notion内容"""
        parts = []
        for item in self.structured["dialogue"][:3]:  # 前3条
            author = item['author'][:15] if item['author'] else ""
            content = item['content'][:60] + "..." if len(item['content']) > 60 else item['content']
            if author:
                parts.append(f"{author}: {content}")
            else:
                parts.append(content)
        return " | ".join(parts)


def preview_content(raw_content: str, source: str = None, url: str = None):
    """预览整理结果"""
    entry = HumorEntry(raw_content, source, url)
    print(entry.format_preview())
    return entry


def add_to_notion(entry: HumorEntry, tags: list = None, notes: str = None):
    """添加到Notion"""
    headers = {
        "Authorization": f"Bearer {NOTION_TOKEN}",
        "Notion-Version": NOTION_VERSION,
        "Content-Type": "application/json"
    }
    
    payload = entry.to_notion_payload(tags, notes)
    
    req = request.Request(
        "https://api.notion.com/v1/pages",
        data=json.dumps(payload).encode(),
        headers=headers,
        method="POST"
    )
    
    try:
        with request.urlopen(req) as response:
            result = json.loads(response.read().decode())
            print(f"✅ 已添加到Notion!")
            return result
    except error.HTTPError as e:
        error_msg = e.read().decode()
        print(f"❌ 添加失败: {error_msg}")
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="幽默内容整理工具")
    parser.add_argument("action", choices=["preview", "add", "draft"], help="操作: preview预览, add直接添加, draft交互模式")
    parser.add_argument("content", nargs="?", help="原始内容")
    parser.add_argument("--tags", help="额外标签，逗号分隔")
    parser.add_argument("--source", help="来源")
    parser.add_argument("--url", help="原始链接")
    parser.add_argument("--notes", help="自定义备注")
    
    args = parser.parse_args()
    
    if args.action == "preview" and args.content:
        entry = preview_content(args.content, args.source, args.url)
        print("\n💡 使用以下命令添加到Notion:")
        safe_content = args.content.replace('"', '\\"')
        print(f'python3 humor_cli.py add "{safe_content[:100]}..." --tags "{args.tags or ""}"')
        
    elif args.action == "add" and args.content:
        entry = HumorEntry(args.content, args.source, args.url)
        tags = args.tags.split(",") if args.tags else []
        add_to_notion(entry, tags, args.notes)
        
    elif args.action == "draft":
        print("📝 交互模式 - 粘贴内容 (Ctrl+D结束):")
        content = sys.stdin.read().strip()
        if content:
            entry = preview_content(content)
            confirm = input("\n确认添加到Notion? (y/n): ")
            if confirm.lower() == 'y':
                add_to_notion(entry)
        else:
            print("❌ 没有输入内容")
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
