# zk-skills

ZK 个人维护的 Claude Code / OpenClaw skill 集合。

按 Claude Code 标准组织：每个 skill 是仓库根下 `skills/<skill-name>/` 下的独立目录，含 `SKILL.md` 入口与 `references/` 等引用文件。

## 已收录的 skills

| Skill | 描述 | 来源 |
|---|---|---|
| [elegant-ancient-narrative-style](./skills/elegant-ancient-narrative-style) | 古雅叙事风格引擎：将现代文本转化为具有古雅气韵的现代表达，强调东方含蓄叙事而非古词替换 | 原创 |
| [super-creazy-html-ppt-in-work](./skills/super-creazy-html-ppt-in-work) | 高端 HTML 幻灯片生成器：智能主题匹配、SVG 图标系统、玻璃态/新拟态/极简多风格、8 种布局 × 12 主题 × 30 动画、16:9 演示优化 | upstream |
| [manga-studio](./skills/manga-studio) | AI 漫画工作流：从剧情/角色素材出发,自动产出世界观、角色参考表、分镜脚本、布局草图、成稿画面。覆盖单页与多页连续剧情,8 种画风预设。与 image-gen 配合使用。 | 原创(参考 morsoli/aimangastudio) |
| [dzu-zhumeng-business-gzh](./skills/dzu-zhumeng-business-gzh) | 德州学院逐梦商学院公众号文章创作：固定头尾、编辑署名、审校流程、往期推荐等元素稳定不变，覆盖安全提醒/节日思政/活动报道/招新报名等题材，图片视频逐项确认。 | 原创 |

## AI 跨境电商 Skill 体系（新增）

按 **AI 原生跨境电商公司** 组织架构设计，共 65 个专业 Skill：

- **00-core**：任务规划、决策分析、报告生成、知识管理
- **01-market-intelligence**：市场调研、竞品分析、用户洞察、趋势监控
- **02-product**：选品、产品定位、SKU 管理、定价策略
- **03-sourcing**：供应商搜索/评估、报价分析、谈判、采购管理
- **04-supply-chain**：库存分析、销量预测、补货、物流优化、履约管理
- **05-channel-operation**：Amazon / Shopify / TikTok / eBay / Walmart / 多平台同步
- **06-listing-content**：Listing 文案、关键词、图片提示词、视频脚本、本地化
- **07-growth-advertising**：广告分析、广告计划、关键词优化、素材测试、转化分析
- **08-customer-service**：客服、投诉分析、退款、评价管理
- **09-finance**：成本分析、利润分析、现金流、财务辅助、税务分析
- **10-data-analysis**：经营看板、数据清洗、数据分析、异常检测
- **11-compliance**：产品合规、商标检查、平台规则监控
- **12-management**：会议总结、任务跟踪、SOP 生成、绩效分析
- **13-automation**：Odoo 集成、电商 API、自动流程、飞书自动化
- **14-learning-memory**：经验管理、知识整理、自我优化

详见 [AI_ECOMMERCE_SKILLS.md](./AI_ECOMMERCE_SKILLS.md)。

配套脚本见 [scripts/ai-ecommerce](./scripts/ai-ecommerce)。

## 安装

### Claude Code

```bash
git clone https://github.com/zuoanCo/zk-skills ~/.claude/skills/zk-skills
# 或单独软链一个
ln -s "$(pwd)/skills/super-creazy-html-ppt-in-work" ~/.claude/skills/super-creazy-html-ppt-in-work
```

### OpenClaw

```bash
cp -r skills/super-creazy-html-ppt-in-work ~/.openclaw/workspace/skills/
```

## 维护约定

- 新增 skill：放在 `skills/<skill-name>/`，自包含
- 引用文件统一放 `references/`
- frontmatter 至少含 `name` + `description`
- 大文件不进入 git
