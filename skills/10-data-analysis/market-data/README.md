# Market Data Skill — 市场数据统一分析平台

AI Agent 市场数据能力，整合国内外电商数据平台。

## 支持的平台（29个）

### 国内（11个）
生意参谋、1688、蝉妈妈、飞瓜数据、抖查查、多多参谋、京东商智、百度指数、微信指数、企查查、天眼查

### 国际（12个）
卖家精灵、Keepa、Helium 10、Jungle Scout、AMZScout、数魔、亚马逊SP-API、速卖通、Shopee、Shopify、店透视、Google Trends

### 通用（6个）
店小秘、马帮、通途、芒果店长、赛盒、亿数通

### 免费数据（无需API Key）
百度搜索建议、淘宝搜索建议、B站搜索建议

## 使用方式

```bash
# 配置平台
market-data config set --platform chanmama --api-key "your_key"
market-data config status

# 查询（免费源默认可用）
market-data keyword --word "笔记本支架" --related
market-data trends --keyword "笔记本支架" --market domestic
market-data competitor --keyword "笔记本支架" --market domestic --top 10
market-data supplier --keyword "笔记本支架"
market-data report --keyword "笔记本支架" --market both
```

## 架构

```
market-data
├── config.json          # 平台凭证配置
├── SKILL.md             # Skill 定义文档
├── src/workflows/
│   ├── market-data.ts           # 配置管理
│   ├── market-data-adapters.ts  # 适配器框架
│   └── adapters/                # 12个平台适配器
│       ├── baidu-index.ts       # 百度指数
│       ├── alibaba1688.ts       # 1688
│       ├── chanmama.ts          # 蝉妈妈
│       ├── feigua.ts            # 飞瓜
│       ├── douchacha.ts         # 抖查查
│       ├── pdd-duoduo.ts        # 多多参谋
│       ├── jd-shangzhi.ts       # 京东商智
│       ├── qichacha.ts          # 企查查
│       ├── seller-spirit.ts     # 卖家精灵
│       ├── keepa.ts             # Keepa
│       ├── google-trends.ts     # Google Trends
│       └── free-sources.ts      # 免费数据聚合
└── src/cli/commands/
    └── market-data.ts           # CLI 命令
```

## 适配器开发

每个适配器实现 `MarketDataAdapter` 接口：

```typescript
interface MarketDataAdapter {
  readonly platformId: string;
  readonly platformName: string;
  readonly supportedCapabilities: string[];
  configure(credentials: PlatformCredentials): void;
  getTrends?(keyword: string, period: string): Promise<TrendResult>;
  getCompetitors?(keyword: string, top: number): Promise<CompetitorResult>;
  getKeywords?(keyword: string, options: any): Promise<KeywordResult>;
  getPrices?(keyword: string, options: any): Promise<PriceResult>;
  getSuppliers?(keyword: string): Promise<SupplierResult>;
}
```

新适配器只需：
1. 实现接口
2. 调用 `registerAdapter('platform_id', () => new MyAdapter())`
3. 在 `market-data-adapters.ts` 中 import
