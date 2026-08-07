// ============================================================
// 飞瓜数据 (Feigua) Adapter — 抖音/快手电商数据
// ============================================================
// 飞瓜数据是短视频电商数据分析平台，覆盖抖音和快手
// 提供直播数据、达人分析、商品追踪、选品推荐
//
// Auth: API Key + API Secret
// Key endpoints:
//   /api/product/search      — 商品搜索
//   /api/product/ranking     — 商品排行
//   /api/live/ranking        — 直播排行
//   /api/author/ranking      — 达人排行

import * as https from 'https';
import * as crypto from 'crypto';
import {
  MarketDataAdapter, PlatformCredentials, TrendResult, CompetitorResult,
  CompetitorItem, KeywordResult, registerAdapter
} from '../market-data-adapters';

class FeiguaAdapter implements MarketDataAdapter {
  readonly platformId = 'feigua';
  readonly platformName = '飞瓜数据';
  readonly supportedCapabilities = ['trends', 'competitors', 'keywords'];

  private apiKey = '';
  private apiSecret = '';

  configure(credentials: PlatformCredentials): void {
    this.apiKey = credentials.api_key || '';
    this.apiSecret = credentials.api_secret || '';
  }

  async getTrends(keyword: string, period: string): Promise<TrendResult> {
    this.requireAuth();

    const data = await this.apiCall('/api/product/ranking', {
      keyword,
      period: period.replace('d', ''),
      sort: 'sales'
    });

    const items = data.data?.list || data.data || [];

    // 飞瓜的排行数据本身就是趋势的一个快照
    const totalSales = items.reduce((sum: number, item: any) => sum + (item.sales || 0), 0);
    const avgSales = items.length > 0 ? Math.round(totalSales / items.length) : 0;

    const dataPoints = items.slice(0, 30).map((item: any, i: number) => ({
      date: item.date || `rank_${i + 1}`,
      value: item.sales || item.salesVolume || 0
    }));

    return {
      keyword,
      platform: this.platformName,
      period,
      search_index: totalSales,
      trend: 'stable',
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
      price: parseFloat(item.price || '0'),
      currency: 'CNY',
      sales: item.sales || item.salesVolume || 0,
      rating: parseFloat(item.score || '0'),
      review_count: item.commentCount || 0,
      url: item.productUrl || '',
      image_url: item.cover || item.image || '',
      shop_name: item.shopName || '',
      extra: {
        platform: item.platform || 'douyin',
        live_sales: item.liveSales,
        video_sales: item.videoSales,
        commission_rate: item.commissionRate,
        category: item.category
      }
    }));

    return { platform: this.platformName, items };
  }

  async getKeywords(keyword: string, options: { related?: boolean }): Promise<KeywordResult> {
    this.requireAuth();

    const data = await this.apiCall('/api/keyword/hot', {
      keyword,
      platform: 'douyin'
    });

    const result: KeywordResult = {
      keyword,
      platform: this.platformName,
      search_volume: data.data?.searchVolume || 0
    };

    if (options.related && data.data?.related) {
      result.related_keywords = data.data.related.map((item: any) => ({
        keyword: item.keyword || '',
        volume: item.volume || 0
      }));
    }

    return result;
  }

  private requireAuth(): void {
    if (!this.apiKey) {
      throw new Error(
        '飞瓜数据需要 API Key。\n' +
        '请在 https://dy.feigua.cn/api 申请 API 权限，然后配置：\n' +
        '  market-data config set --platform feigua --api-key "your_key" --api-secret "your_secret"'
      );
    }
  }

  private async apiCall(path: string, params: Record<string, string>): Promise<any> {
    const timestamp = String(Math.floor(Date.now() / 1000));
    const allParams: Record<string, string> = { ...params, app_key: this.apiKey, timestamp };

    if (this.apiSecret) {
      const sortedKeys = Object.keys(allParams).sort();
      const signStr = sortedKeys.map(k => `${k}=${allParams[k]}`).join('&');
      const signature = crypto.createHmac('sha256', this.apiSecret).update(signStr).digest('hex');
      allParams['sign'] = signature;
    }

    const qs = Object.entries(allParams)
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
      .join('&');

    return this.httpGet(`https://api.feigua.cn${path}?${qs}`);
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
              reject(new Error(`飞瓜 API 错误 [${parsed.code}]: ${parsed.message || parsed.msg || '未知错误'}`));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`飞瓜返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('飞瓜请求超时')); });
      req.end();
    });
  }
}

registerAdapter('feigua', () => new FeiguaAdapter());
