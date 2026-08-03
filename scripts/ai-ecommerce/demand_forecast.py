#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
demand_forecast.py

简单销量预测脚本：基于历史日销量，使用移动平均 + 趋势预测未来销量。

输入文件格式（sales.csv）:
    date,sales
    2026-06-01,12
    2026-06-02,15
    ...

用法:
    python scripts/demand_forecast.py sales.csv --days 30
"""

import argparse
import csv
import sys
from datetime import datetime, timedelta
from pathlib import Path


def load_sales(path: Path) -> list[tuple[datetime, int]]:
    data = []
    with open(path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            date = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            sales = int(row["sales"])
            data.append((date, sales))
    return sorted(data, key=lambda x: x[0])


def moving_average(values: list[int], window: int) -> float:
    if len(values) < window:
        window = len(values)
    return sum(values[-window:]) / window


def trend_slope(values: list[int], window: int = 14) -> float:
    """基于最近 window 天计算日均增长/下降趋势。"""
    if len(values) < window * 2:
        return 0.0
    recent = sum(values[-window:]) / window
    previous = sum(values[-(window * 2) : -window]) / window
    return (recent - previous) / window


def forecast(data: list[tuple[datetime, int]], days: int) -> list[tuple[datetime, float]]:
    sales_values = [s for _, s in data]
    base = moving_average(sales_values, 30)
    slope = trend_slope(sales_values, 14)

    last_date = data[-1][0]
    results = []
    for i in range(1, days + 1):
        predicted = max(base + slope * i, 0)
        date = last_date + timedelta(days=i)
        results.append((date, predicted))
    return results


def main() -> int:
    parser = argparse.ArgumentParser(description="销量预测")
    parser.add_argument("csv", type=Path, help="历史销量 CSV 文件路径")
    parser.add_argument("--days", type=int, default=30, help="预测未来天数")
    args = parser.parse_args()

    if not args.csv.exists():
        print(f"文件不存在: {args.csv}", file=sys.stderr)
        return 1

    data = load_sales(args.csv)
    if len(data) < 30:
        print("警告：历史数据不足 30 天，预测结果可能不准确", file=sys.stderr)

    results = forecast(data, args.days)
    total = sum(v for _, v in results)

    print(f"{'日期':<12} {'预测销量':>10}")
    print("-" * 25)
    for date, value in results:
        print(f"{date.strftime('%Y-%m-%d'):<12} {value:>10.1f}")

    print(f"\n未来 {args.days} 天总预测销量: {total:.0f}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
