#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
quotation_compare.py

供应商报价比较脚本：读取多家供应商报价 CSV，统一到岸成本并输出采购建议。

输入文件格式（quotations.csv）:
    supplier,unit_price,moq,packaging,certification,mold,shipping,duty,insurance,lead_time
    工厂A,8.50,500,0.30,0,0,1.20,0.85,0.05,25

用法:
    python scripts/quotation_compare.py quotations.csv --quantity 1000
"""

import argparse
import csv
import sys
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Quotation:
    supplier: str
    unit_price: float
    moq: int
    packaging: float
    certification: float
    mold: float
    shipping: float
    duty: float
    insurance: float
    lead_time: int

    def landed_cost(self, quantity: int) -> tuple[float, float]:
        if quantity < self.moq:
            return float("inf"), float("inf")
        product_total = self.unit_price * quantity
        packaging_total = self.packaging * quantity
        certification_total = self.certification * quantity
        mold_total = self.mold
        shipping_total = self.shipping * quantity
        duty_total = self.duty * quantity
        insurance_total = self.insurance * quantity

        total = (
            product_total
            + packaging_total
            + certification_total
            + mold_total
            + shipping_total
            + duty_total
            + insurance_total
        )
        per_unit = total / quantity
        return total, per_unit


def load_quotations(path: Path) -> list[Quotation]:
    rows = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            rows.append(
                Quotation(
                    supplier=row["supplier"].strip(),
                    unit_price=float(row["unit_price"]),
                    moq=int(row["moq"]),
                    packaging=float(row["packaging"]),
                    certification=float(row["certification"]),
                    mold=float(row["mold"]),
                    shipping=float(row["shipping"]),
                    duty=float(row["duty"]),
                    insurance=float(row["insurance"]),
                    lead_time=int(row["lead_time"]),
                )
            )
    return rows


def analyze(quotations: list[Quotation], quantity: int) -> None:
    results = []
    for q in quotations:
        total, per_unit = q.landed_cost(quantity)
        results.append((q, total, per_unit))

    results = sorted(results, key=lambda x: x[2])

    print(f"采购数量: {quantity}")
    print()
    print(f"{'供应商':<10} {'到岸总价':>12} {'到岸单价':>12} {'MOQ':>8} {'交期':>8} {'状态'}")
    print("-" * 65)
    for q, total, per_unit in results:
        status = "不满足 MOQ" if quantity < q.moq else "可行"
        print(
            f"{q.supplier:<10} ${total:>11.2f} ${per_unit:>11.2f} {q.moq:>8} {q.lead_time:>8}天 {status}"
        )

    feasible = [r for r in results if quantity >= r[0].moq]
    if feasible:
        best = feasible[0]
        print(f"\n推荐供应商: {best[0].supplier}，到岸单价 ${best[2]:.2f}")


def main() -> int:
    parser = argparse.ArgumentParser(description="供应商报价比较")
    parser.add_argument("csv", type=Path, help="报价 CSV 文件")
    parser.add_argument("--quantity", type=int, required=True, help="采购数量")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"文件不存在: {args.csv}", file=sys.stderr)
        return 1

    quotations = load_quotations(args.csv)
    analyze(quotations, args.quantity)
    return 0


if __name__ == "__main__":
    sys.exit(main())
