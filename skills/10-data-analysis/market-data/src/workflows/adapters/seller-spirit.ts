// ============================================================
// 卖家精灵 (SellerSpirit) Adapter — 亚马逊选品/关键词/竞品
// ============================================================
// 卖家精灵是中国最大的亚马逊卖家数据工具
// API 文档: https://www.sellersprite.com/v3/api-doc
//
// Auth: API Key + API Secret (HMAC签名)
// Key endpoints:
//   /api/v3/keyword/reverse         — ASIN反查关键词
//   /api/v3/keyword/trend           — 关键词趋势
//   /api/v3/product/search          — 产品搜索
//   /api/v3/product/detail          — 产品详情
//   /api/v3/competitor/analysis     — 竞品分析
//   /api/v3/market/trend            — 品类趋势

import * as https from 'https';
import * as crypto from 'crypto';
import {
  MarketDataAdapter, PlatformCredentials, TrendResult, CompetitorResult,
  CompetitorItem, KeywordResult, PriceResult, PriceItem, registerAdapter
} from '../market-data-adapters';

class SellerSpiritAdapter implements MarketDataAdapter {
  readonly platformId = 'seller_spirit';
  readonly platformName = '卖家精灵';
  readonly supportedCapabilities = ['trends', 'competitors', 'keywords', 'prices'];

  private apiKey = '';
  private apiSecret = '';

  // 站点映射
  private static readonly SITE_MAP: Record<string, number> = {
    'us': 1, 'uk': 2, 'de': 3, 'fr': 4, 'jp': 5, 'ca': 6, 'it': 7, 'es': 8, 'au': 9, 'mx': 10
  };

  configure(credentials: PlatformCredentials): void {
    this.apiKey = credentials.api_key || '';
    this.apiSecret = credentials.api_secret || '';
  }

  async getTrends(keyword: string, period: string): Promise<TrendResult> {
    this.requireAuth();

    const daysMap: Record<string, number> = { '7d': 7, '30d': 30, '90d': 90, '180d': 180, '1y': 365 };
    const days = daysMap[period] || 30;

    const data = await this.apiCall('/api/v3/keyword/trend', {
      keyword,
      marketplace: 'us',
      days: String(days)
    });

    const trendData = data.data || [];
    const dataPoints = trendData.map((item: any) => ({
      date: item.date || item.searchDate || '',
      value: item.searchVolume || item.search_volume || 0
    }));

    // Calculate trend
    let trend: 'rising' | 'stable' | 'declining' = 'stable';
    if (dataPoints.length >= 14) {
      const firstHalf = dataPoints.slice(0, Math.floor(dataPoints.length / 2));
      const secondHalf = dataPoints.slice(Math.floor(dataPoints.length / 2));
      const avgFirst = firstHalf.reduce((s: number, d: any) => s + d.value, 0) / firstHalf.length;
      const avgSecond = secondHalf.reduce((s: number, d: any) => s + d.value, 0) / secondHalf.length;
      if (avgSecond > avgFirst * 1.15) trend = 'rising';
      else if (avgSecond < avgFirst * 0.85) trend = 'declining';
    }

    const avgVolume = dataPoints.length > 0
      ? Math.round(dataPoints.reduce((s: number, d: any) => s + d.value, 0) / dataPoints.length)
      : 0;

    return {
      keyword,
      platform: this.platformName,
      period,
      search_index: avgVolume,
      trend,
      data_points: dataPoints
    };
  }

  async getCompetitors(keyword: string, top: number): Promise<CompetitorResult> {
    this.requireAuth();

    const data = await this.apiCall('/api/v3/product/search', {
      keyword,
      marketplace: 'us',
      page: '1',
      page_size: String(Math.min(top, 50)),
      sort_by: 'sales'
    });

    const items: CompetitorItem[] = (data.data?.products || data.data || []).map((item: any) => ({
      title: item.title || '',
      price: parseFloat(item.price || '0'),
      currency: 'USD',
      sales: item.monthlySales || item.estimated_sales || 0,
      rating: parseFloat(item.rating || '0'),
      review_count: item.reviewCount || item.review_count || 0,
      url: item.asin ? `https://www.amazon.com/dp/${item.asin}` : '',
      image_url: item.imageUrl || item.image || '',
      shop_name: item.brand || '',
      extra: {
        asin: item.asin,
        bsr: item.bsr || item.rank || 0,
        fba_fee: item.fbaFee,
        category: item.category,
        seller_count: item.sellerCount
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

    // Get keyword details
    const data = await this.apiCall('/api/v3/keyword/trend', {
      keyword,
      marketplace: 'us',
      days: '30'
    });

    if (data.data) {
      const latest = Array.isArray(data.data) ? data.data[data.data.length - 1] : data.data;
      result.search_volume = latest.searchVolume || latest.search_volume || 0;
      result.competition = latest.competition || undefined;
      result.cpc = latest.cpc || undefined;

      if (options.history && Array.isArray(data.data)) {
        result.history = data.data.map((item: any) => ({
          date: item.date || '',
          value: item.searchVolume || 0
        }));
      }
    }

    // Get related keywords
    if (options.related) {
      try {
        const relData = await this.apiCall('/api/v3/keyword/related', {
          keyword,
          marketplace: 'us'
        });
        result.related_keywords = (relData.data || []).map((item: any) => ({
          keyword: item.keyword || item.word || '',
          volume: item.searchVolume || item.volume || 0
        }));
      } catch {
        // Related keywords are optional
      }
    }

    return result;
  }

  async getPrices(keyword: string, options: { history?: number }): Promise<PriceResult> {
    this.requireAuth();

    const data = await this.apiCall('/api/v3/product/search', {
      keyword,
      marketplace: 'us',
      page: '1',
      page_size: '20',
      sort_by: 'price'
    });

    const items: PriceItem[] = (data.data?.products || data.data || []).map((item: any) => ({
      title: item.title || '',
      current_price: parseFloat(item.price || '0'),
      currency: 'USD',
      url: item.asin ? `https://www.amazon.com/dp/${item.asin}` : '',
      shop_name: item.brand || ''
    }));

    return { platform: this.platformName, items };
  }

  // ---- API call ----

  private requireAuth(): void {
    if (!this.apiKey || !this.apiSecret) {
      throw new Error(
        '卖家精灵需要 API Key 和 API Secret。\n' +
        '请在 https://www.sellersprite.com/v3/api 申请 API 权限，然后配置：\n' +
        '  market-data config set --platform seller_spirit --api-key "your_key" --api-secret "your_secret"'
      );
    }
  }

  private async apiCall(path: string, params: Record<string, string>): Promise<any> {
    const timestamp = String(Math.floor(Date.now() / 1000));

    // HMAC-SHA256 signature
    const signStr = Object.keys(params).sort().map(k => `${k}=${params[k]}`).join('&') + `&timestamp=${timestamp}`;
    const signature = crypto
      .createHmac('sha256', this.apiSecret)
      .update(signStr)
      .digest('hex');

    const qs = Object.entries({ ...params, timestamp, sign: signature })
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
      .join('&');

    return this.httpGet(`https://api.sellersprite.com${path}?${qs}`);
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
          'Accept': 'application/json',
          'X-Api-Key': this.apiKey
        }
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            if (parsed.code && parsed.code !== 200 && parsed.code !== 0) {
              reject(new Error(`卖家精灵 API 错误 [${parsed.code}]: ${parsed.message || parsed.msg || '未知错误'}`));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`卖家精灵返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('卖家精灵请求超时')); });
      req.end();
    });
  }
}

registerAdapter('seller_spirit', () => new SellerSpiritAdapter());
