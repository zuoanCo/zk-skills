#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
keyword_research.py

关键词研究辅助脚本：基于种子词扩展长尾词，计算简单相关性和竞争度评分。

用法:
    python scripts/keyword_research.py "pet water fountain" --market us --output keywords.csv
"""

import argparse
import csv
import sys
from pathlib import Path


# 长尾扩展模板（实际生产环境应接入关键词工具 API）
EXPANSIONS = [
    "{seed} for cats",
    "{seed} for dogs",
    "automatic {seed}",
    "quiet {seed}",
    "stainless steel {seed}",
    "large capacity {seed}",
    "{seed} with filter",
    "{seed} for small pets",
    "{seed} for multi cat",
    "best {seed}",
]

NEGATIVE_PATTERNS = [
    "cheap",
    "free",
    "diy",
    "homemade",
    "used",
]


def expand(seed: str) -> list[str]:
    keywords = [seed]
    for template in EXPANSIONS:
        keywords.append(template.format(seed=seed))
    return keywords


def estimate_metrics(keyword: str) -> dict:
    """
    模拟搜索量和竞争度估算。
    实际应接入 Helium 10 / Jungle Scout / 卖家精灵等工具 API。
    """
    words = keyword.split()
    # 越长尾通常搜索量越低但竞争度越低
    search_volume = max(1000, 50000 - len(words) * 8000 + hash(keyword) % 5000)
    competition = max(10, 80 - len(words) * 15)
    relevance = 100 if seed in keyword else 80
    return {
        "keyword": keyword,
        "search_volume": abs(search_volume),
        "competition": abs(competition),
        "relevance": relevance,
    }


def classify(keyword: str) -> str:
    lower = keyword.lower()
    for neg in NEGATIVE_PATTERNS:
        if neg in lower:
            return "否定词"
    words = keyword.split()
    if len(words) <= 2:
        return "核心词"
    if len(words) >= 4:
        return "长尾词"
    return "中尾词"


def main() -> int:
    parser = argparse.ArgumentParser(description="关键词扩展研究")
    parser.add_argument("seed", help="种子关键词")
    parser.add_argument("--market", default="us", help="目标市场")
    parser.add_argument("--output", type=Path, help="输出 CSV 文件")
    args = parser.parse_args()

    global seed
    seed = args.seed.lower()

    keywords = expand(args.seed)
    results = [estimate_metrics(kw) for kw in keywords]
    for r in results:
        r["type"] = classify(r["keyword"])

    # 按搜索量排序
    results = sorted(results, key=lambda x: x["search_volume"], reverse=True)

    if args.output:
        with open(args.output, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(
                f,
                fieldnames=["keyword", "type", "search_volume", "competition", "relevance"],
            )
            writer.writeheader()
            writer.writerows(results)
        print(f"已保存到 {args.output}")
    else:
        print(f"{'关键词':<45} {'类型':<10} {'搜索量':>10} {'竞争度':>10} {'相关性':>10}")
        print("-" * 90)
        for r in results:
            print(
                f"{r['keyword']:<45} {r['type']:<10} {r['search_volume']:>10} "
                f"{r['competition']:>10} {r['relevance']:>10}"
            )

    return 0


if __name__ == "__main__":
    sys.exit(main())
