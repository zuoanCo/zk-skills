---
name: market-research
description: 市场调研 Skill。搜索并分析 Google Trends、Amazon Best Seller、TikTok Trend、Reddit、YouTube 等数据源，输出市场规模、增长趋势、消费者画像、机会点和风险。
---

# market-research · 市场调研

用多源数据扫描市场机会，回答"这个品类值不值得进入"。

## 用途

- 扫描品类市场规模和增长趋势
- 识别消费者画像和核心需求
- 发现市场机会点和进入窗口
- 评估市场风险和合规门槛
- 为选品和定位提供数据基础

## 触发场景

- 进入新市场或新品类前
- 老板要求"看看美国宠物市场"
- 选品需要市场数据支撑
- 季度战略复盘

## 输入

- 目标市场（国家 / 地区）
- 目标品类或关键词
- 时间范围（默认 12 个月）
- 数据源偏好（可选）

## 输出

```markdown
## {市场} {品类} 市场调研报告

### 市场规模
- 整体市场规模
- 线上渗透率
- 年增长率

### 增长趋势
- Google Trends 趋势
- Amazon Best Seller 走势
- TikTok / YouTube 热度

### 消费者画像
- 人群特征
- 购买动机
- 价格敏感度

### 机会点
- 未被满足的需求
- 新兴细分赛道
- 季节性 / 事件性机会

### 风险
- 合规风险
- 竞争加剧
- 供应链风险
```

## 工作流

1. **确定研究范围**：市场、品类、关键词、时间窗口。
2. **多源数据采集**：
   - Google Trends：搜索热度、区域分布、相关查询
   - Amazon Best Seller：品类销量排名、价格带
   - TikTok Creative Center / 热门标签：内容热度
   - Reddit / 社媒：用户讨论、痛点
   - YouTube：测评视频、观看量
3. **数据清洗与交叉验证**：去噪、对齐时间、识别异常。
4. **洞察提炼**：市场规模估算、趋势判断、机会点。
5. **风险识别**：合规、竞争、供应链、平台政策。
6. **输出报告**：结构化 Markdown。

## 调用关系

**被调用**：task-planning、product-selection、decision-analysis

**调用**：competitor-analysis、customer-insight、compliance-check

## 依赖工具 / Memory

- Tool: 浏览器、Google Trends API（如有）、Amazon 数据爬虫、TikTok / Reddit / YouTube 搜索
- Memory: 历史市场数据、品类基准

## 边界与限制

- 不承诺绝对精确的市场规模，需标注数据来源和置信度
- 对需要登录或反爬的数据源，需使用合规方式
- 市场变化快，建议定期更新

## 示例

输入：美国市场宠物智能饮水机
输出：市场规模 $X 亿、年增长 15%、消费者关注静音 / 过滤 / App 连接、机会点在小型犬 / 多猫家庭、风险为 FCC / FDA 食品接触材料合规
