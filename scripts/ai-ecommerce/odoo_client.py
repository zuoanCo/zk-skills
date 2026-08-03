#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
odoo_client.py

Odoo 连接示例脚本：使用 XML-RPC 读取和创建记录。

环境变量:
    ODOO_URL=https://your-odoo.odoo.com
    ODOO_DB=your_db
    ODOO_USERNAME=your_email
    ODOO_API_KEY=your_api_key

用法:
    python scripts/odoo_client.py sale.order --limit 10
    python scripts/odoo_client.py purchase.order --create --file po.json
"""

import argparse
import json
import os
import sys
from xmlrpc.client import ServerProxy


def get_env_or_raise(name: str) -> str:
    value = os.environ.get(name)
    if not value:
        raise EnvironmentError(f"缺少环境变量: {name}")
    return value


def authenticate() -> tuple[ServerProxy, int, str]:
    url = get_env_or_raise("ODOO_URL").rstrip("/")
    db = get_env_or_raise("ODOO_DB")
    username = get_env_or_raise("ODOO_USERNAME")
    api_key = get_env_or_raise("ODOO_API_KEY")

    common = ServerProxy(f"{url}/xmlrpc/2/common")
    uid = common.authenticate(db, username, api_key, {})
    if not uid:
        raise AuthenticationError("Odoo 认证失败")

    models = ServerProxy(f"{url}/xmlrpc/2/object")
    return models, uid, db


class AuthenticationError(Exception):
    pass


def read_records(models: ServerProxy, uid: int, db: str, model: str, limit: int) -> list:
    return models.execute_kw(
        db,
        uid,
        os.environ["ODOO_API_KEY"],
        model,
        "search_read",
        [[]],
        {"limit": limit, "fields": ["name", "create_date"]},
    )


def create_record(models: ServerProxy, uid: int, db: str, model: str, data: dict) -> int:
    return models.execute_kw(
        db,
        uid,
        os.environ["ODOO_API_KEY"],
        model,
        "create",
        [data],
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Odoo API 客户端")
    parser.add_argument("model", help="Odoo 模型名，如 sale.order")
    parser.add_argument("--limit", type=int, default=10, help="读取数量")
    parser.add_argument("--create", action="store_true", help="创建记录")
    parser.add_argument("--file", type=str, help="创建记录用的 JSON 文件")
    args = parser.parse_args()

    try:
        models, uid, db = authenticate()
    except EnvironmentError as e:
        print(e, file=sys.stderr)
        return 1
    except AuthenticationError as e:
        print(e, file=sys.stderr)
        return 1

    if args.create:
        if not args.file:
            print("--create 需要 --file 指定 JSON 数据", file=sys.stderr)
            return 1
        with open(args.file, "r", encoding="utf-8") as f:
            data = json.load(f)
        record_id = create_record(models, uid, db, args.model, data)
        print(f"已创建 {args.model} 记录，ID: {record_id}")
    else:
        records = read_records(models, uid, db, args.model, args.limit)
        print(json.dumps(records, indent=2, ensure_ascii=False, default=str))

    return 0


if __name__ == "__main__":
    sys.exit(main())
