---
name: market-data
description: 市场数据平台统一接入，支持国内外电商数据查询、竞品分析、选品建议、趋势洞察。使用场景：查市场、看竞品、选品、趋势分析、关键词、行业数据。
when_to_use:
  - 用户需要查看市场趋势、行业数据
  - 用户需要竞品分析、竞品价格监控
  - 用户需要选品建议、选品分析
  - 用户需要关键词分析、搜索热度
  - 用户需要供应商查询、比价
  - 用户提到 市场数据、竞品、选品、趋势、关键词、行业、比价、供应商、销量预估
allowed-tools: Bash(market-data *) Bash(odoo model *) Bash(odoo skill *)
---

# Market Data Skill — 市场数据统一分析平台

本 skill 整合国内外主流电商数据平台，提供统一的市场数据查询和分析能力。

## 运行模式

系统支持三种模式，根据用户配置自动识别：

| 模式 | 说明 | 必须配置至少一个 |
|------|------|-----------------|
| `domestic` | 国内电商数据 | 生意参谋/1688/蝉妈妈/飞瓜/抖查查/多多参谋/京东商智/百度指数/企查查/天眼查 |
| `international` | 跨境电商数据 | 卖家精灵/Keepa/Helium10/JungleScout/亚马逊SP-API/速卖通/Shopee/店透视 |
| `both` | 国内外全覆盖 | 国内+国际各至少一个 |

`shared` 分类的平台（店小秘/马帮/通途/芒果/赛盒/亿数通）同时计入国内和国际。

## 配置管理

配置文件：`skills/market-data/config.json`

### 查看当前配置状态

```bash
market-data config status
```

输出示例：
```
模式: domestic（自动检测）
已启用平台: 蝉妈妈, 1688, 百度指数
未配置平台: 生意参谋, 飞瓜数据, 抖查查, ...
```

### 配置平台凭证

```bash
market-data config set --platform chanmama --api-key "xxx" --api-secret "yyy"
market-data config set --platform keepa --api-key "zzz"
market-data config set --platform alibaba1688 --app-key "xxx" --app-secret "yyy"
```

### 设置模式

```bash
market-data config mode domestic     # 仅国内
market-data config mode international # 仅国外
market-data config mode both          # 国内外
market-data config mode auto          # 根据已配置平台自动判断（默认）
```

### 启用/禁用平台

```bash
market-data config enable --platform chanmama
market-data config disable --platform keepa
```

## 核心查询能力

### 1. 市场趋势分析

```bash
market-data trends --keyword "笔记本支架" --market domestic --period 30d
market-data trends --keyword "laptop stand" --market international --period 90d
```

支持字段：
- `--keyword` 搜索关键词
- `--market` 国内(domestic)/国际(international)/全部(all)
- `--period` 时间范围：7d/30d/90d/180d/1y
- `--platform` 指定数据源（可选，默认用所有已配置平台）

### 2. 竞品分析

```bash
market-data competitor --keyword "笔记本支架" --market domestic --top 10
market-data competitor --asin "B0XXXXXXXX" --market international
market-data competitor --url "https://item.taobao.com/xxx"
```

支持字段：
- `--keyword` 按关键词搜索竞品
- `--asin` 亚马逊ASIN
- `--url` 商品链接
- `--market` 国内/国际/全部
- `--top` 返回前N个竞品
- `--fields` 指定返回字段：price,sales,rating,review_count,bsr

### 3. 选品分析

```bash
market-data product-select --category "办公家具" --market domestic --budget 50
market-data product-select --keyword "laptop accessories" --market international --min-margin 30%
```

支持字段：
- `--category` 品类
- `--keyword` 关键词
- `--market` 国内/国际/全部
- `--budget` 预算上限（采购价）
- `--min-margin` 最低毛利率
- `--min-sales` 月销量最低门槛

### 4. 关键词分析

```bash
market-data keyword --word "笔记本支架" --market domestic
market-data keyword --word "laptop stand" --market international --related
```

支持字段：
- `--word` 目标关键词
- `--market` 国内/国际/全部
- `--related` 同时返回相关词
- `--history` 返回搜索趋势历史

### 5. 价格监控

```bash
market-data price --keyword "笔记本支架" --market domestic --alert-below 30
market-data price --asin "B0XXXXXXXX" --market international --history 90d
```

支持字段：
- `--keyword` 或 `--asin` 或 `--url` 指定目标
- `--alert-below` 价格低于此值时提醒
- `--alert-above` 价格高于此值时提醒
- `--history` 查看价格历史

### 6. 供应商查询

```bash
market-data supplier --keyword "笔记本支架" --platform alibaba1688
market-data supplier --company "深圳市xxx科技有限公司" --platform qichacha
```

### 7. 综合分析报告

```bash
market-data report --keyword "笔记本支架" --market both
market-data report --keyword "笔记本支架" --market domestic --format markdown
```

综合多个数据源，生成包含趋势、竞品、关键词、定价建议的完整报告。

## 数据源优先级

当多个平台都能提供同类数据时，按以下优先级选用：

### 国内数据
| 数据类型 | 首选 | 备选 |
|---------|------|------|
| 行业大盘 | 生意参谋 | 京东商智 |
| 搜索关键词 | 生意参谋 | 百度指数 |
| 竞品销量 | 生意参谋 | 蝉妈妈/飞瓜 |
| 直播电商 | 蝉妈妈 | 飞瓜/抖查查 |
| 供应商比价 | 1688 | 企查查/天眼查 |
| 消费趋势 | 百度指数 | 微信指数 |
| 利润计算 | 赛盒 | 亿数通 |

### 国际数据
| 数据类型 | 首选 | 备选 |
|---------|------|------|
| 选品分析 | 卖家精灵 | Jungle Scout |
| 关键词 | 卖家精灵 | Helium 10 |
| 价格历史 | Keepa | 店透视 |
| 竞品追踪 | 店透视 | 卖家精灵 |
| 销量预估 | 卖家精灵 | AMZScout |
| 广告数据 | 亚马逊SP-API | 亿数通 |
| 搜索趋势 | Google Trends | — |

### 多平台（国内外通用）
| 数据类型 | 首选 | 备选 |
|---------|------|------|
| 多平台订单 | 店小秘 | 马帮 |
| 利润精算 | 赛盒 | 马帮 |

## 错误处理

### 无平台配置

```
❌ 未检测到任何已配置的数据平台。
当前模式: domestic
请至少配置以下其中一个平台：
  - 生意参谋: market-data config set --platform shengyicanmou --app-key "xxx"
  - 蝉妈妈:   market-data config set --platform chanmama --api-key "xxx"
  - 1688:     market-data config set --platform alibaba1688 --app-key "xxx"
  - 百度指数:  market-data config set --platform baidu_index --cookie "xxx"
运行 market-data config status 查看完整平台列表。
```

### 平台凭证失效

```
⚠️ 蝉妈妈 API 返回认证失败（401）。
请检查凭证是否过期：
  market-data config set --platform chanmama --api-key "新key"
已切换到备选数据源：飞瓜数据
```

### 请求频率限制

```
⚠️ Keepa API 调用频率超限，等待 60 秒后重试...
已切换到备选数据源：店透视
```

## 与 ERP 联动

market-data 可以与 odoo 库存/销售数据联动分析：

```bash
# 对比市场数据和自有库存
market-data compare --keyword "笔记本支架" --erp-product "笔记本电脑支架"
```

此时会：
1. 从 market-data 获取市场均价、竞品价格、行业销量
2. 从 Odoo 获取自有库存、成本、售价
3. 生成对标分析：定价是否合理、库存是否充足、是否需要补货

## 使用示例

**用户说：** "帮我看看笔记本支架在国内市场的情况"

```bash
market-data trends --keyword "笔记本支架" --market domestic --period 90d
market-data competitor --keyword "笔记本支架" --market domestic --top 10
market-data keyword --word "笔记本支架" --market domestic --related
```

**用户说：** "laptop stand 在亚马逊上卖得怎么样"

```bash
market-data trends --keyword "laptop stand" --market international --period 30d
market-data competitor --keyword "laptop stand" --market international --top 10
market-data price --keyword "laptop stand" --market international --history 90d
```

**用户说：** "帮我做一个笔记本支架的全面市场分析"

```bash
market-data report --keyword "笔记本支架" --market both
```

**用户说：** "帮我在1688上找笔记本支架的供应商"

```bash
market-data supplier --keyword "笔记本支架" --platform alibaba1688
```

**用户说：** "我的笔记本支架定价50块，合理吗"

```bash
market-data compare --keyword "笔记本支架" --erp-product "笔记本电脑支架"
```
