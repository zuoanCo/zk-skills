# Odoo 集成示例

## 示例 1：读取销售订单

### 输入

- 模型：`sale.order`
- 操作：读取
- 条件：过去 30 天，状态为 sale

### 输出

```python
# 调用示例
orders = odoo_read(
    model='sale.order',
    domain=[
        ('date_order', '>=', '2026-07-01'),
        ('state', '=', 'sale')
    ],
    fields=['name', 'date_order', 'partner_id', 'amount_total', 'order_line']
)

# 返回结果
{
    "count": 156,
    "records": [
        {
            "name": "S00045",
            "date_order": "2026-07-15",
            "partner_id": [12, "Amazon Customer"],
            "amount_total": 159.96,
            "order_line": [101, 102, 103]
        },
        ...
    ]
}
```

## 示例 2：创建采购草稿

### 输入

- 供应商：工厂 B
- 产品：WP-001 宠物智能饮水机
- 数量：500
- 单价：$8.50

### 输出

```python
# 调用示例
po = odoo_create(
    model='purchase.order',
    values={
        'partner_id': 25,  # 工厂 B
        'order_line': [
            (0, 0, {
                'product_id': 101,
                'name': 'WP-001 宠物智能饮水机',
                'product_qty': 500,
                'price_unit': 8.50,
                'date_planned': '2026-09-10'
            })
        ]
    }
)

# 返回结果
{
    "status": "draft",
    "po_id": 128,
    "po_name": "P00128",
    "message": "采购草稿已创建，等待人工确认"
}
```

## 示例 3：读取库存

### 输入

- 模型：`stock.quant`
- 产品：WP-001
- 仓库：美西仓

### 输出

```python
inventory = odoo_read(
    model='stock.quant',
    domain=[
        ('product_id', '=', 101),
        ('location_id', 'ilike', 'US-West')
    ],
    fields=['product_id', 'location_id', 'quantity', 'reserved_quantity']
)

# 返回结果
{
    "product_id": 101,
    "location_id": "WH/US-West/Stock",
    "quantity": 320,
    "reserved_quantity": 45,
    "available_quantity": 275
}
```

## 示例 4：创建会计凭证草稿

### 输入

- 类型：供应商账单
- 金额：$4,250
- 供应商：工厂 B

### 输出

```python
bill = odoo_create(
    model='account.move',
    values={
        'move_type': 'in_invoice',
        'partner_id': 25,
        'invoice_line_ids': [
            (0, 0, {
                'product_id': 101,
                'quantity': 500,
                'price_unit': 8.50,
                'tax_ids': [(6, 0, [])]
            })
        ]
    }
)

# 返回结果
{
    "status": "draft",
    "move_id": 456,
    "move_name": "BILL/2026/00045",
    "message": "凭证草稿已创建，等待财务确认"
}
```
