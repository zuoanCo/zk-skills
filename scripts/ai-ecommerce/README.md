# AI 跨境电商 Skill 脚本集合

本目录包含 AI 跨境电商体系中可独立运行的辅助脚本。这些脚本与对应 Skill 配套使用，用于数据处理、计算和 API 连接。

## 脚本清单

| 脚本 | 用途 | 对应 Skill |
|------|------|-----------|
| [inventory_analyzer.py](inventory_analyzer.py) | 库存健康度分析：周转天数、缺货风险、呆滞库存 | inventory-analysis |
| [demand_forecast.py](demand_forecast.py) | 基于历史销量的简单时间序列预测 | demand-forecast |
| [ppc_analyzer.py](ppc_analyzer.py) | Amazon PPC Search Term Report 分析 | advertising-analysis |
| [profit_calculator.py](profit_calculator.py) | SKU 利润和利润率计算 | profitability-analysis |
| [odoo_client.py](odoo_client.py) | Odoo XML-RPC 连接示例 | odoo-integration |
| [quotation_compare.py](quotation_compare.py) | 多供应商报价到岸成本比较 | quotation-analysis |
| [product_scorer.py](product_scorer.py) | 选品四维度评分 | product-selection |
| [keyword_research.py](keyword_research.py) | 关键词扩展和基础评分 | seo-keyword |
| [generate_remaining_skills.py](generate_remaining_skills.py) | 生成 65 Skill 骨架的生成器（维护用） |

## 示例数据

`data/` 目录包含测试用的示例 CSV 文件：

- `sample_inventory.csv`：库存分析样本
- `sample_sales.csv`：销量预测样本
- `sample_ppc_report.csv`：PPC 报告样本
- `sample_quotations.csv`：供应商报价样本

## 快速测试

```bash
# 库存分析
python scripts/inventory_analyzer.py scripts/data/sample_inventory.csv --safety-days 14

# 利润计算
python scripts/profit_calculator.py --price 39.99 --cost 8.5 --logistics 1.2 --fba 4.52 --commission 15 --ads 20 --returns 8

# 选品评分
python scripts/product_scorer.py --demand 85 --competition 65 --profit 75 --supply 80

# PPC 分析
python scripts/ppc_analyzer.py scripts/data/sample_ppc_report.csv --acos-target 30

# 报价比较
python scripts/quotation_compare.py scripts/data/sample_quotations.csv --quantity 1000

# 销量预测
python scripts/demand_forecast.py scripts/data/sample_sales.csv --days 7

# 关键词扩展
python scripts/keyword_research.py "pet water fountain" --output /tmp/keywords.csv
```

## 安全说明

- `odoo_client.py` 需要环境变量配置，**不要将 API key 写入代码**
- 所有脚本只读取数据或生成建议，**不自动执行写操作**
- 生产环境使用前请先在测试数据上验证

## 扩展建议

- 将脚本封装为 MCP Tool 或 Claude Code 可调用的工具
- 对接真实数据源（Odoo API、Amazon SP API、广告平台 API）
- 增加单元测试和日志记录
- 对长周期任务增加异步执行能力
