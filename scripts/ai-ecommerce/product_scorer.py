#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
product_scorer.py

选品评分脚本：根据市场需求、竞争程度、利润空间、供应稳定四个维度计算综合得分。

用法:
    python scripts/product_scorer.py --demand 85 --competition 65 --profit 75 --supply 80
"""

import argparse
import sys


WEIGHTS = {
    "demand": 0.30,
    "competition": 0.20,
    "profit": 0.30,
    "supply": 0.20,
}


def score(demand: int, competition: int, profit: int, supply: int) -> dict:
    # 竞争程度得分越高表示竞争越小（越容易进入）
    competition_score = 100 - competition

    total = (
        demand * WEIGHTS["demand"]
        + competition_score * WEIGHTS["competition"]
        + profit * WEIGHTS["profit"]
        + supply * WEIGHTS["supply"]
    )

    if total >= 80:
        grade = "A"
    elif total >= 70:
        grade = "B+"
    elif total >= 60:
        grade = "B"
    elif total >= 50:
        grade = "C"
    else:
        grade = "D"

    return {
        "total": total,
        "grade": grade,
        "breakdown": {
            "市场需求 (30%)": demand * WEIGHTS["demand"],
            "竞争程度 (20%)": competition_score * WEIGHTS["competition"],
            "利润空间 (30%)": profit * WEIGHTS["profit"],
            "供应稳定 (20%)": supply * WEIGHTS["supply"],
        },
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="选品评分器")
    parser.add_argument("--demand", type=int, required=True, help="市场需求得分 0-100")
    parser.add_argument("--competition", type=int, required=True, help="竞争激烈程度 0-100（越高越激烈）")
    parser.add_argument("--profit", type=int, required=True, help="利润空间得分 0-100")
    parser.add_argument("--supply", type=int, required=True, help="供应稳定性得分 0-100")
    args = parser.parse_args()

    result = score(args.demand, args.competition, args.profit, args.supply)

    print(f"综合得分: {result['total']:.1f}")
    print(f"评级: {result['grade']}")
    print()
    print("分项得分:")
    for name, value in result["breakdown"].items():
        print(f"  {name}: {value:.1f}")

    if result["grade"] in ("A", "B+"):
        print("\n建议: 推荐进入")
    elif result["grade"] == "B":
        print("\n建议: 谨慎进入，需优化弱项")
    else:
        print("\n建议: 不建议进入")

    return 0


if __name__ == "__main__":
    sys.exit(main())
