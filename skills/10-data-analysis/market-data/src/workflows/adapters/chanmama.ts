// ============================================================
// 蝉妈妈 (Chanmama) Adapter — 抖音电商数据
// ============================================================
// 蝉妈妈是国内最大的抖音电商数据分析平台
// 提供直播带货、达人排行、商品销量、爆款追踪等数据
//
// Auth: API Key + API Secret
// Key endpoints:
//   /api/product/search     — 商品搜索/销量
//   /api/author/ranking     — 达人排行
//   /api/live/search        — 直播搜索
//   /api/product/trend      — 商品趋势
//   /api/keyword/hot        — 热门关键词

import * as https from 'https';
import * as crypto from 'crypto';
import {
  MarketDataAdapter, PlatformCredentials, TrendResult, CompetitorResult,
  CompetitorItem, KeywordResult, registerAdapter
} from '../market-data-adapters';

class ChanmamaAdapter implements MarketDataAdapter {
  readonly platformId = 'chanmama';
  readonly platformName = '蝉妈妈';
  readonly supportedCapabilities = ['trends', 'competitors', 'keywords'];

  private apiKey = '';
  private apiSecret = '';

  configure(credentials: PlatformCredentials): void {
    this.apiKey = credentials.api_key || '';
    this.apiSecret = credentials.api_secret || '';
  }

  async getTrends(keyword: string, period: string): Promise<TrendResult> {
    this.requireAuth();

    const data = await this.apiCall('/api/product/trend', {
      keyword,
      days: period.replace('d', '')
    });

    const trendData = data.data?.list || data.data || [];
    const dataPoints = trendData.map((item: any) => ({
      date: item.date || '',
      value: item.sales || item.salesVolume || item.searchVolume || 0
    }));

    let trend: 'rising' | 'stable' | 'declining' = 'stable';
    if (dataPoints.length >= 7) {
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

    return {
      keyword,
      platform: this.platformName,
      period,
      search_index: avgValue,
      trend,
      data_points: dataPoints
    };
  }

  async getCompetitors(keyword: string, top: number): Promise<CompetitorResult> {
    this.requireAuth();

    const data = await this.apiCall('/api/product/search', {
      keyword,
      page: '1',
      page_size: String(Math.min(top, 50)),
      sort: 'sales_desc'
    });

    const items: CompetitorItem[] = (data.data?.list || data.data || []).map((item: any) => ({
      title: item.title || item.productName || '',
      price: parseFloat(item.price || item.minPrice || '0'),
      currency: 'CNY',
      sales: item.sales || item.salesVolume || item.monthlySales || 0,
      rating: parseFloat(item.score || item.rating || '0'),
      review_count: item.commentCount || 0,
      url: item.productUrl || item.url || '',
      image_url: item.cover || item.image || '',
      shop_name: item.shopName || item.shop || '',
      extra: {
        douyin_price: item.price,
        commission_rate: item.commissionRate,
        live_sales: item.liveSales,
        video_sales: item.videoSales,
        category: item.category,
        sales_trend: item.salesTrend
      }
    }));

    return { platform: this.platformName, items };
  }

  async getKeywords(keyword: string, options: { related?: boolean; history?: boolean }): Promise<KeywordResult> {
    this.requireAuth();

    const result: KeywordResult = {
      keyword,
      platform: this.platformName
    };

    // 热门关键词
    const data = await this.apiCall('/api/keyword/hot', {
      keyword,
      type: 'product'
    });

    if (data.data) {
      result.search_volume = data.data.searchVolume || data.data.volume || 0;
      result.competition = data.data.competition || undefined;

      if (options.related) {
        result.related_keywords = (data.data.related || data.data.list || []).map((item: any) => ({
          keyword: item.keyword || item.word || '',
          volume: item.searchVolume || item.volume || 0
        }));
      }
    }

    return result;
  }

  // ---- API call ----

  private requireAuth(): void {
    if (!this.apiKey) {
      throw new Error(
        '蝉妈妈需要 API Key。\n' +
        '请在 https://www.chanmama.com/api 申请 API 权限，然后配置：\n' +
        '  market-data config set --platform chanmama --api-key "your_key" --api-secret "your_secret"'
      );
    }
  }

  private async apiCall(path: string, params: Record<string, string>): Promise<any> {
    const timestamp = String(Math.floor(Date.now() / 1000));

    const allParams: Record<string, string> = { ...params, app_key: this.apiKey, timestamp };
    const sortedKeys = Object.keys(allParams).sort();
    const signStr = sortedKeys.map(k => `${k}=${allParams[k]}`).join('&');

    let signature = '';
    if (this.apiSecret) {
      signature = crypto.createHmac('sha256', this.apiSecret).update(signStr).digest('hex');
    }

    const qs = sortedKeys.map(k => `${encodeURIComponent(k)}=${encodeURIComponent(allParams[k])}`).join('&');
    const url = `https://api.chanmama.com${path}?${qs}${signature ? '&sign=' + signature : ''}`;

    return this.httpGet(url);
  }

  private httpGet(url: string): Promise<any> {
    return new Promise((resolve, reject) => {
      const parsed = new URL(url);
      const options = {
        hostname: parsed.hostname,
        path: parsed.pathname + parsed.search,
        method: 'GET',
        headers: {
          'User-Agent': 'market-data-cli/1.0',
          'Accept': 'application/json'
        }
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            if (parsed.code && parsed.code !== 0 && parsed.code !== 200) {
              reject(new Error(`蝉妈妈 API 错误 [${parsed.code}]: ${parsed.message || parsed.msg || '未知错误'}`));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`蝉妈妈返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('蝉妈妈请求超时')); });
      req.end();
    });
  }
}

registerAdapter('chanmama', () => new ChanmamaAdapter());
