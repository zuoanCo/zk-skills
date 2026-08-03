#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
profit_calculator.py

SKU 利润计算脚本：输入售价和各项成本，计算净利润和利润率。

用法:
    python scripts/profit_calculator.py --price 39.99 --cost 8.5 --logistics 1.2 --fba 4.52 --commission 15 --ads 20 --returns 8
"""

import argparse
import sys


def calculate(
    price: float,
    cost: float,
    logistics: float,
    fba: float,
    commission_pct: float,
    ads_pct: float,
    returns_pct: float,
    storage: float = 0.35,
    packaging: float = 0.5,
    other: float = 0.8,
) -> dict:
    commission = price * commission_pct / 100
    ads = price * ads_pct / 100
    returns = price * returns_pct / 100

    total_cost = cost + logistics + fba + commission + ads + returns + storage + packaging + other
    profit = price - total_cost
    margin = profit / price * 100 if price else 0.0

    return {
        "price": price,
        "cost": total_cost,
        "profit": profit,
        "margin": margin,
        "breakdown": {
            "采购成本": cost,
            "头程物流": logistics,
            "FBA 费用": fba,
            "平台佣金": commission,
            "广告费": ads,
            "退货损失": returns,
            "仓储费": storage,
            "包装费": packaging,
            "其他费用": other,
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="SKU 利润计算器")
    parser.add_argument("--price", type=float, required=True, help="售价")
    parser.add_argument("--cost", type=float, required=True, help="采购成本")
    parser.add_argument("--logistics", type=float, default=0.0, help="头程物流")
    parser.add_argument("--fba", type=float, default=0.0, help="FBA/尾程配送费")
    parser.add_argument("--commission", type=float, default=15.0, help="平台佣金百分比")
    parser.add_argument("--ads", type=float, default=20.0, help="广告费占售价百分比")
    parser.add_argument("--returns", type=float, default=8.0, help="退货损失占售价百分比")
    parser.add_argument("--storage", type=float, default=0.35, help="仓储费")
    parser.add_argument("--packaging", type=float, default=0.5, help="包装费")
    parser.add_argument("--other", type=float, default=0.8, help="其他费用")
    args = parser.parse_args()

    result = calculate(
        price=args.price,
        cost=args.cost,
        logistics=args.logistics,
        fba=args.fba,
        commission_pct=args.commission,
        ads_pct=args.ads,
        returns_pct=args.returns,
        storage=args.storage,
        packaging=args.packaging,
        other=args.other,
    )

    print(f"售价: ${result['price']:.2f}")
    print(f"总成本: ${result['cost']:.2f}")
    print(f"净利润: ${result['profit']:.2f}")
    print(f"利润率: {result['margin']:.2f}%")
    print()
    print("成本明细:")
    for name, value in result["breakdown"].items():
        pct = value / result["price"] * 100 if result["price"] else 0
        print(f"  {name}: ${value:.2f} ({pct:.1f}%)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
