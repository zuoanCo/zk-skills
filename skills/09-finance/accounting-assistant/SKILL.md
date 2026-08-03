---
name: accounting-assistant
description: 连接 Odoo Accounting，创建凭证草稿、分析账目、辅助对账和报表生成。
---

# accounting-assistant · 财务辅助

## 用途
- 创建会计凭证草稿
- 分析账目异常
- 辅助对账
- 生成财务报表初稿

## 触发场景
- 需要创建凭证
- 月度对账
- 账目异常需要分析
- 需要快速报表

## 输入
- 交易数据
- 凭证信息
- 对账单
- Odoo Accounting 配置

## 输出
```markdown
## 财务辅助报告

### 凭证草稿
### 账目分析
### 对账差异
### 建议调整
### 报表初稿
```

## 工作流
1. **接收数据**：发票、银行流水、平台账单
2. **分类匹配**：收入、成本、费用
3. **创建草稿**：在 Odoo 生成凭证草稿
4. **异常识别**：对账差异、重复记录
5. **输出分析**：科目余额、趋势
6. **人工确认**：会计审核后过账

## 调用关系
**被调用**：profitability-analysis、cost-analysis

**调用**：odoo-integration、data-cleaning

## 依赖工具 / Memory
- Tool: Odoo Accounting API
- Memory: 会计科目映射、对账规则

## 边界与限制
- 只创建草稿，不过账
- 税务、审计问题需专业会计
- 不处理现金收支

## 示例
输出：根据 7 月 Amazon 结算单生成 12 张凭证草稿，涉及收入、佣金、FBA 费用等科目
