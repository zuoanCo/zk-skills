#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
inventory_analyzer.py

库存分析脚本：读取库存和销售 CSV，计算周转天数、缺货风险、呆滞库存。

输入文件格式（inventory.csv）:
    sku,warehouse,quantity,inbound,sales_7d,sales_30d,age_days
    WP-001,US-West,320,500,45,180,45

用法:
    python scripts/inventory_analyzer.py inventory.csv --safety-days 14
"""

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class SKUInventory:
    sku: str
    warehouse: str
    quantity: int
    inbound: int
    sales_7d: int
    sales_30d: int
    age_days: int

    @property
    def available(self) -> int:
        return self.quantity + self.inbound

    @property
    def daily_sales(self) -> float:
        return self.sales_30d / 30.0

    @property
    def turnover_days(self) -> float:
        if self.daily_sales <= 0:
            return float("inf")
        return self.available / self.daily_sales

    def safety_stock(self, days: int = 14) -> float:
        return self.daily_sales * days

    def status(self, safety_days: int = 14) -> str:
        if self.quantity < self.safety_stock(safety_days) and self.turnover_days < safety_days * 2:
            return "缺货风险"
        if self.turnover_days > 180 or self.age_days > 180:
            return "呆滞"
        if self.turnover_days > 90:
            return "滞销"
        return "健康"


def load_inventory(path: Path) -> list[SKUInventory]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                SKUInventory(
                    sku=row["sku"].strip(),
                    warehouse=row["warehouse"].strip(),
                    quantity=int(row["quantity"]),
                    inbound=int(row["inbound"]),
                    sales_7d=int(row["sales_7d"]),
                    sales_30d=int(row["sales_30d"]),
                    age_days=int(row["age_days"]),
                )
            )
    return rows


def analyze(items: list[SKUInventory], safety_days: int) -> None:
    print(f"{'SKU':<10} {'仓库':<10} {'库存':>8} {'在途':>8} {'30天销量':>10} {'周转天数':>10} {'状态':<10} {'建议'}")
    print("-" * 90)

    for item in items:
        status = item.status(safety_days)
        if status == "缺货风险":
            needed = int(item.safety_stock(safety_days) * 2 - item.available)
            advice = f"紧急补货 {max(needed, 0)}"
        elif status == "呆滞":
            advice = "清仓/降价"
        elif status == "滞销":
            advice = "促销/优化 Listing"
        else:
            advice = "维持"

        print(
            f"{item.sku:<10} {item.warehouse:<10} {item.quantity:>8} "
            f"{item.inbound:>8} {item.sales_30d:>10} {item.turnover_days:>10.1f} "
            f"{status:<10} {advice}"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="库存健康度分析")
    parser.add_argument("csv", type=Path, help="库存 CSV 文件路径")
    parser.add_argument("--safety-days", type=int, default=14, help="安全库存天数")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"文件不存在: {args.csv}", file=sys.stderr)
        return 1

    items = load_inventory(args.csv)
    analyze(items, args.safety_days)
    return 0


if __name__ == "__main__":
    sys.exit(main())
