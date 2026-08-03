---
name: trend-monitoring
description: 每天扫描 TikTok、Google、YouTube、Pinterest 等平台，发现爆品趋势和新兴需求，抢占市场先机。
---

# trend-monitoring · 趋势监控

## 用途
- 持续监控多平台热点
- 发现潜在爆品和新兴需求
- 预警趋势变化
- 为选品和内容创作提供灵感

## 触发场景
- 每日趋势扫描
- 季度选品规划
- 内容团队寻找选题
- 发现异常销量波动时

## 输入
- 监控关键词列表
- 目标平台
- 时间窗口
- 历史趋势基线

## 输出
```markdown
## 趋势监控日报

### 今日热点
### 增长最快关键词
### 新兴品类
### 相关视频 / 内容
### 机会评估
### 风险提示
```

## 工作流
1. **设置监控词**：品类词、场景词、竞品词
2. **多平台扫描**：TikTok、Google Trends、YouTube、Pinterest
3. **热度计算**：播放量、搜索量、互动增长率
4. **趋势分类**：爆品、潜力、衰退、异常
5. **输出预警**：高优先级趋势推送相关人员

## 调用关系
**被调用**：market-research、product-selection

**调用**：market-research、data-analysis

## 依赖工具 / Memory
- Tool: 社媒 API、Google Trends、爬虫
- Memory: 历史趋势库、爆款案例

## 边界与限制
- 趋势不等于销量，需结合市场数据验证
- 不追昙花一现的伪需求
- 监控频率和范围受工具限制

## 示例
输出：TikTok #quietcatfountain 标签近 7 天播放量增长 340%，建议关注静音饮水机趋势
