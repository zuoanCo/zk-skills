// ============================================================
// 多多参谋 (PDD Duoduo) Adapter — 拼多多电商数据
// ============================================================
// 多多参谋是拼多多卖家的数据分析工具
// 提供关键词分析、竞品监控、类目数据
//
// Auth: API Key + API Secret

import * as https from 'https';
import * as crypto from 'crypto';
import {
  MarketDataAdapter, PlatformCredentials, TrendResult, CompetitorResult,
  CompetitorItem, KeywordResult, registerAdapter
} from '../market-data-adapters';

class PddDuoduoAdapter implements MarketDataAdapter {
  readonly platformId = 'pdd_duoduo';
  readonly platformName = '多多参谋';
  readonly supportedCapabilities = ['trends', 'competitors', 'keywords'];

  private apiKey = '';
  private apiSecret = '';

  configure(credentials: PlatformCredentials): void {
    this.apiKey = credentials.api_key || '';
    this.apiSecret = credentials.api_secret || '';
  }

  async getTrends(keyword: string, period: string): Promise<TrendResult> {
    this.requireAuth();
    const data = await this.apiCall('/api/keyword/trend', {
      keyword,
      days: period.replace('d', '')
    });

    const trendData = data.data?.list || [];
    const dataPoints = trendData.map((item: any) => ({
      date: item.date || '',
      value: item.searchVolume || item.sales || 0
    }));

    let trend: 'rising' | 'stable' | 'declining' = 'stable';
    if (dataPoints.length >= 14) {
      const firstHalf = dataPoints.slice(0, Math.floor(dataPoints.length / 2));
      const secondHalf = dataPoints.slice(Math.floor(dataPoints.length / 2));
      const avgFirst = firstHalf.reduce((s: number, d: any) => s + d.value, 0) / firstHalf.length;
      const avgSecond = secondHalf.reduce((s: number, d: any) => s + d.value, 0) / secondHalf.length;
      if (avgSecond > avgFirst * 1.15) trend = 'rising';
      else if (avgSecond < avgFirst * 0.85) trend = 'declining';
    }

    const avgValue = dataPoints.length > 0
      ? Math.round(dataPoints.reduce((s: number, d: any) => s + d.value, 0) / dataPoints.length)
      : 0;

    return { keyword, platform: this.platformName, period, search_index: avgValue, trend, data_points: dataPoints };
  }

  async getCompetitors(keyword: string, top: number): Promise<CompetitorResult> {
    this.requireAuth();
    const data = await this.apiCall('/api/product/search', {
      keyword, page: '1', page_size: String(Math.min(top, 50)), sort: 'sales_desc'
    });

    const items: CompetitorItem[] = (data.data?.list || []).map((item: any) => ({
      title: item.goodsName || item.title || '',
      price: parseFloat(item.minGroupPrice || item.price || '0'),
      currency: 'CNY',
      sales: item.salesTip ? parseInt(item.salesTip.replace(/[^0-9]/g, '')) : (item.sales || 0),
      rating: parseFloat(item.avgScore || '0'),
      review_count: item.commentCount || 0,
      url: item.goodsId ? `https://mobile.yangkeduo.com/goods.html?goods_id=${item.goodsId}` : '',
      image_url: item.thumbUrl || '',
      shop_name: item.mallName || '',
      extra: {
        goods_id: item.goodsId,
        category: item.categoryName,
        promotion_rate: item.promotionRate
      }
    }));

    return { platform: this.platformName, items };
  }

  async getKeywords(keyword: string, options: { related?: boolean }): Promise<KeywordResult> {
    this.requireAuth();
    const data = await this.apiCall('/api/keyword/detail', { keyword });

    const result: KeywordResult = {
      keyword,
      platform: this.platformName,
      search_volume: data.data?.searchVolume || 0,
      competition: data.data?.competition || undefined
    };

    if (options.related && data.data?.related) {
      result.related_keywords = data.data.related.map((item: any) => ({
        keyword: item.keyword || '',
        volume: item.searchVolume || 0
      }));
    }

    return result;
  }

  private requireAuth(): void {
    if (!this.apiKey) {
      throw new Error(
        '多多参谋需要 API Key。\n' +
        '请在 https://www.duoduocm.com 申请 API 权限，然后配置：\n' +
        '  market-data config set --platform pdd_duoduo --api-key "your_key" --api-secret "your_secret"'
      );
    }
  }

  private async apiCall(path: string, params: Record<string, string>): Promise<any> {
    const timestamp = String(Math.floor(Date.now() / 1000));
    const allParams: Record<string, string> = { ...params, app_key: this.apiKey, timestamp };

    if (this.apiSecret) {
      const sortedKeys = Object.keys(allParams).sort();
      const signStr = sortedKeys.map(k => `${k}=${allParams[k]}`).join('&');
      allParams['sign'] = crypto.createHmac('sha256', this.apiSecret).update(signStr).digest('hex');
    }

    const qs = Object.entries(allParams).map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join('&');
    return this.httpGet(`https://api.duoduocm.com${path}?${qs}`);
  }

  private httpGet(url: string): Promise<any> {
    return new Promise((resolve, reject) => {
      const parsed = new URL(url);
      const options = {
        hostname: parsed.hostname,
        path: parsed.pathname + parsed.search,
        method: 'GET',
        headers: { 'User-Agent': 'market-data-cli/1.0', 'Accept': 'application/json' }
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            if (parsed.code && parsed.code !== 0 && parsed.code !== 200) {
              reject(new Error(`多多参谋 API 错误 [${parsed.code}]: ${parsed.message || parsed.msg || '未知错误'}`));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`多多参谋返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });
      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('多多参谋请求超时')); });
      req.end();
    });
  }
}

registerAdapter('pdd_duoduo', () => new PddDuoduoAdapter());
