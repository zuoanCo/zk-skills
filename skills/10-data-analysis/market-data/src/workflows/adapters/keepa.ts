// ============================================================
// Keepa Adapter — Amazon 价格历史/排名追踪
// ============================================================
// Keepa API: https://api.keepa.com
// Docs: https://keepa.com/#!discuss/t/using-the-keepa-api/47
//
// Auth: API key (passed as query param)
// Key endpoints:
//   /product?key=...&domain=1&asin=...      — product data + price history
//   /product?key=...&domain=1&title=...     — search by title
//   /category?key=...&domain=1&category=... — category stats

import * as https from 'https';
import {
  MarketDataAdapter, PlatformCredentials, TrendResult, CompetitorResult,
  CompetitorItem, PriceResult, PriceItem, registerAdapter
} from '../market-data-adapters';

class KeepaAdapter implements MarketDataAdapter {
  readonly platformId = 'keepa';
  readonly platformName = 'Keepa';
  readonly supportedCapabilities = ['competitors', 'prices', 'trends'];

  private apiKey = '';

  // Keepa uses a proprietary time format: minutes since epoch, * 60000 offset
  // Plus an offset of 21564000 minutes (for historical data before 2012)
  private static readonly KEEPA_EPOCH_OFFSET = 21564000;

  configure(credentials: PlatformCredentials): void {
    this.apiKey = credentials.api_key || '';
  }

  async getCompetitors(keyword: string, top: number): Promise<CompetitorResult> {
    this.requireAuth();

    // Search products by keyword (domain 1 = US, 2 = UK, 3 = DE, etc.)
    const data = await this.apiCall('/product', {
      domain: '1',
      title: keyword,
      stats: '1'
    });

    const asins: string[] = data.asins || [];
    if (asins.length === 0) {
      return { platform: this.platformName, items: [] };
    }

    // Fetch detailed product data for top N
    const targetAsins = asins.slice(0, Math.min(top, 100));
    const productData = await this.apiCall('/product', {
      domain: '1',
      asin: targetAsins.join(','),
      stats: '1'
    });

    const products = productData.products || [];
    const items: CompetitorItem[] = products.map((p: any) => ({
      title: p.title || '',
      price: this.getLatestPrice(p, 1), // 1 = Amazon price
      currency: 'USD',
      sales: p.monthlySold ? parseInt(p.monthlySold) : undefined,
      rating: p.avgRating ? p.avgRating / 10 : undefined,
      review_count: p.reviewCount || 0,
      url: `https://www.amazon.com/dp/${p.asin}`,
      image_url: p.imagesCSV ? `https://images-na.ssl-images-amazon.com/images/I/${p.imagesCSV.split(',')[0]}` : '',
      shop_name: 'Amazon',
      extra: {
        asin: p.asin,
        bsr: p.stats?.current?.[3] || 0, // 3 = Sales rank
        brand: p.brand || '',
        fba_fees: p.fbaFees || {},
        monthly_sold: p.monthlySold
      }
    }));

    return { platform: this.platformName, items };
  }

  async getPrices(keyword: string, options: { history?: number }): Promise<PriceResult> {
    this.requireAuth();

    const data = await this.apiCall('/product', {
      domain: '1',
      title: keyword,
      stats: '1',
      history: '1'
    });

    const products = data.products || [];
    const items: PriceItem[] = products.slice(0, 20).map((p: any) => {
      const currentPrice = this.getLatestPrice(p, 1);
      const historyDays = options.history || 30;
      const history = this.parsePriceHistory(p, 1, historyDays);

      return {
        title: p.title || '',
        current_price: currentPrice,
        currency: 'USD',
        url: `https://www.amazon.com/dp/${p.asin}`,
        shop_name: 'Amazon',
        price_history: history
      };
    });

    return { platform: this.platformName, items };
  }

  async getTrends(keyword: string, period: string): Promise<TrendResult> {
    this.requireAuth();

    const data = await this.apiCall('/product', {
      domain: '1',
      title: keyword,
      stats: '1',
      history: '1'
    });

    const products = data.products || [];
    if (products.length === 0) {
      return { keyword, platform: this.platformName, period, search_index: 0, trend: 'stable', data_points: [] };
    }

    // Use BSR (Best Seller Rank) as a proxy for demand trend
    // Lower BSR = higher sales, so we invert for display
    const p = products[0];
    const bsrHistory = this.parseBsrHistory(p, period);

    let trend: 'rising' | 'stable' | 'declining' = 'stable';
    if (bsrHistory.length >= 14) {
      const firstHalf = bsrHistory.slice(0, Math.floor(bsrHistory.length / 2));
      const secondHalf = bsrHistory.slice(Math.floor(bsrHistory.length / 2));
      const avgFirst = firstHalf.reduce((s, d) => s + d.value, 0) / firstHalf.length;
      const avgSecond = secondHalf.reduce((s, d) => s + d.value, 0) / secondHalf.length;
      // For BSR, lower is better — so if avgSecond < avgFirst, demand is rising
      if (avgSecond < avgFirst * 0.85) trend = 'rising';
      else if (avgSecond > avgFirst * 1.15) trend = 'declining';
    }

    const avgBsr = bsrHistory.length > 0
      ? Math.round(bsrHistory.reduce((s, d) => s + d.value, 0) / bsrHistory.length)
      : 0;

    return {
      keyword,
      platform: this.platformName,
      period,
      search_index: avgBsr,
      trend,
      data_points: bsrHistory
    };
  }

  // ---- Keepa-specific helpers ----

  private getLatestPrice(product: any, csvIndex: number): number {
    const csv = product.csv?.[csvIndex];
    if (!csv || csv.length < 2) return 0;
    // Last two values are [timestamp, price]; Keepa prices are in cents
    return (csv[csv.length - 1] || 0) / 100;
  }

  private parsePriceHistory(product: any, csvIndex: number, days: number): Array<{ date: string; price: number }> {
    const csv = product.csv?.[csvIndex];
    if (!csv || csv.length < 2) return [];

    const result: Array<{ date: string; price: number }> = [];
    const cutoff = Date.now() - days * 86400000;

    // CSV format: [timestamp1, price1, timestamp2, price2, ...]
    for (let i = 0; i < csv.length - 1; i += 2) {
      const tsMs = (csv[i] + KeepaAdapter.KEEPA_EPOCH_OFFSET) * 60000;
      const price = csv[i + 1];
      if (tsMs >= cutoff && price >= 0 && price !== -1) {
        result.push({
          date: new Date(tsMs).toISOString().slice(0, 10),
          price: price / 100
        });
      }
    }
    return result;
  }

  private parseBsrHistory(product: any, period: string): Array<{ date: string; value: number }> {
    const csv = product.csv?.[3]; // 3 = Sales rank
    if (!csv || csv.length < 2) return [];

    const daysMap: Record<string, number> = { '7d': 7, '30d': 30, '90d': 90, '180d': 180, '1y': 365 };
    const days = daysMap[period] || 30;
    const cutoff = Date.now() - days * 86400000;

    const result: Array<{ date: string; value: number }> = [];
    for (let i = 0; i < csv.length - 1; i += 2) {
      const tsMs = (csv[i] + KeepaAdapter.KEEPA_EPOCH_OFFSET) * 60000;
      const value = csv[i + 1];
      if (tsMs >= cutoff && value > 0 && value !== -1) {
        result.push({
          date: new Date(tsMs).toISOString().slice(0, 10),
          value
        });
      }
    }
    return result;
  }

  // ---- API call ----

  private requireAuth(): void {
    if (!this.apiKey) {
      throw new Error(
        'Keepa 需要 API Key。\n' +
        '请在 https://keepa.com/#!api 购买 API 订阅，然后配置：\n' +
        '  market-data config set --platform keepa --api-key "your_key"'
      );
    }
  }

  private async apiCall(path: string, params: Record<string, string>): Promise<any> {
    const qs = Object.entries({ key: this.apiKey, ...params })
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
      .join('&');

    return this.httpGet(`https://api.keepa.com${path}?${qs}`);
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
            if (parsed.error) {
              reject(new Error(`Keepa API 错误: ${parsed.error.message || JSON.stringify(parsed.error)}`));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`Keepa 返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(30000, () => { req.destroy(); reject(new Error('Keepa 请求超时')); });
      req.end();
    });
  }
}

registerAdapter('keepa', () => new KeepaAdapter());
