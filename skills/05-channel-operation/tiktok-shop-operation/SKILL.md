---
name: tiktok-shop-operation
description: 负责 TikTok Shop 的达人合作、短视频内容、直播运营和店铺增长。
---

# tiktok-shop-operation · TikTok Shop 运营

## 用途
- 策划 TikTok 短视频内容
- 管理达人合作
- 优化直播运营
- 分析 TikTok Shop 销售数据

## 触发场景
- TikTok Shop 新品上架
- 寻找合作达人
- 短视频数据下滑
- 直播策划

## 输入
- 产品信息
- TikTok Shop 数据
- 达人数据
- 短视频表现
- 竞品内容

## 输出
```markdown
## TikTok Shop 运营方案

### 内容策略
### 达人合作计划
### 直播计划
### 投放策略
### 数据复盘
```

## 工作流
1. **店铺诊断**：GMV、转化率、内容表现
2. **内容策划**：选题、脚本、拍摄计划
3. **达人筛选**：粉丝画像、互动率、报价
4. **直播运营**：排期、脚本、选品
5. **广告投放**：Spark Ads、直播加热
6. **数据复盘**：GMV、ROAS、内容 ROI

## 调用关系
**被调用**：channel-operation-agent

**调用**：video-script、creative-testing、advertising-analysis

## 依赖工具 / Memory
- Tool: TikTok Shop Seller Center、达人平台
- Memory: 爆款内容模板、达人库

## 边界与限制
- 不直接发布内容或联系达人
- 达人合作合同需人工确认
- 内容需符合平台社区规范

## 示例
输出：推荐 10 位宠物类达人，平均互动率 5%+，建议寄样 3 位做短视频测评
