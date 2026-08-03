#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
ppc_analyzer.py

Amazon PPC 报告分析脚本：读取 Search Term Report CSV，识别高 spend 低转化词、高转化词，输出优化建议。

输入文件格式（ppc_report.csv）:
    campaign_name,ad_group_name,customer_search_term,impressions,clicks,spend,sales,orders
    Auto-1,Ad-1,pet water fountain,1000,50,25.0,80.0,2

用法:
    python scripts/ppc_analyzer.py ppc_report.csv --acos-target 30
"""

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class KeywordMetrics:
    keyword: str
    campaign: str
    impressions: int
    clicks: int
    spend: float
    sales: float
    orders: int

    @property
    def ctr(self) -> float:
        return self.clicks / self.impressions if self.impressions else 0.0

    @property
    def cvr(self) -> float:
        return self.orders / self.clicks if self.clicks else 0.0

    @property
    def acos(self) -> float:
        return self.spend / self.sales * 100 if self.sales else float("inf")


def load_report(path: Path) -> list[KeywordMetrics]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                KeywordMetrics(
                    keyword=row["customer_search_term"].strip(),
                    campaign=row["campaign_name"].strip(),
                    impressions=int(row["impressions"]),
                    clicks=int(row["clicks"]),
                    spend=float(row["spend"]),
                    sales=float(row["sales"]),
                    orders=int(row["orders"]),
                )
            )
    return rows


def analyze(metrics: list[KeywordMetrics], acos_target: float) -> None:
    total_spend = sum(m.spend for m in metrics)
    total_sales = sum(m.sales for m in metrics)
    overall_acos = total_spend / total_sales * 100 if total_sales else 0.0

    print(f"总 Spend: ${total_spend:.2f}")
    print(f"总 Sales: ${total_sales:.2f}")
    print(f"整体 ACOS: {overall_acos:.1f}% (目标: {acos_target}%)")
    print()

    # 高 spend 低转化（ACOS 超标 2 倍或 0 销售）
    waste = [m for m in metrics if m.spend > 10 and (m.acos > acos_target * 2 or m.sales == 0)]
    waste = sorted(waste, key=lambda x: x.spend, reverse=True)

    print("=== 建议否定 / 降价的关键词 ===")
    print(f"{'关键词':<30} {'Campaign':<20} {'Spend':>10} {'Sales':>10} {'ACOS':>10}")
    for m in waste[:15]:
        acos_str = f"{m.acos:.1f}%" if m.sales != 0 else "无销售"
        print(f"{m.keyword:<30} {m.campaign:<20} ${m.spend:>9.2f} ${m.sales:>9.2f} {acos_str:>10}")
    print()

    # 高转化词
    good = [m for m in metrics if m.sales > 0 and m.acos <= acos_target and m.spend > 10]
    good = sorted(good, key=lambda x: x.sales, reverse=True)

    print("=== 建议加预算的关键词 ===")
    print(f"{'关键词':<30} {'Campaign':<20} {'Spend':>10} {'Sales':>10} {'ACOS':>10}")
    for m in good[:15]:
        print(f"{m.keyword:<30} {m.campaign:<20} ${m.spend:>9.2f} ${m.sales:>9.2f} {m.acos:>9.1f}%")


def main() -> int:
    parser = argparse.ArgumentParser(description="Amazon PPC 报告分析")
    parser.add_argument("csv", type=Path, help="PPC Search Term Report CSV")
    parser.add_argument("--acos-target", type=float, default=30.0, help="目标 ACOS")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"文件不存在: {args.csv}", file=sys.stderr)
        return 1

    metrics = load_report(args.csv)
    analyze(metrics, args.acos_target)
    return 0


if __name__ == "__main__":
    sys.exit(main())
