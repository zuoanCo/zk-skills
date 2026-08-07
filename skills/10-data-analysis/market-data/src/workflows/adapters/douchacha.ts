// ============================================================
// 抖查查 (Douchacha) Adapter — 抖音电商数据
// ============================================================
// 抖查查是抖音电商数据分析平台，专注达人带货和商品销量
//
// Auth: API Key
// Key endpoints:
//   /api/product/search    — 商品搜索
//   /api/author/detail     — 达人详情
//   /api/live/detail       — 直播详情
//   /api/product/sales     — 商品销量查询

import * as https from 'https';
import {
  MarketDataAdapter, PlatformCredentials, CompetitorResult, CompetitorItem,
  KeywordResult, registerAdapter
} from '../market-data-adapters';

class DouchachaAdapter implements MarketDataAdapter {
  readonly platformId = 'douchacha';
  readonly platformName = '抖查查';
  readonly supportedCapabilities = ['competitors', 'keywords'];

  private apiKey = '';

  configure(credentials: PlatformCredentials): void {
    this.apiKey = credentials.api_key || '';
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
      url: item.productUrl || '',
      image_url: item.cover || item.image || '',
      shop_name: item.shopName || '',
      extra: {
        live_sales: item.liveSales,
        video_sales: item.videoSales,
        category: item.category
      }
    }));

    return { platform: this.platformName, items };
  }

  async getKeywords(keyword: string, options: { related?: boolean }): Promise<KeywordResult> {
    this.requireAuth();

    const data = await this.apiCall('/api/keyword/search', { keyword });

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
        '抖查查需要 API Key。\n' +
        '请在 https://www.douchacha.com 申请 API 权限，然后配置：\n' +
        '  market-data config set --platform douchacha --api-key "your_key"'
      );
    }
  }

  private async apiCall(path: string, params: Record<string, string>): Promise<any> {
    const qs = Object.entries({ ...params, app_key: this.apiKey })
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
      .join('&');

    return this.httpGet(`https://api.douchacha.com${path}?${qs}`);
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
              reject(new Error(`抖查查 API 错误 [${parsed.code}]: ${parsed.message || parsed.msg || '未知错误'}`));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`抖查查返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('抖查查请求超时')); });
      req.end();
    });
  }
}

registerAdapter('douchacha', () => new DouchachaAdapter());
