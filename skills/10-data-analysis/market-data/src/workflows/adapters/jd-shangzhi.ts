// ============================================================
// 京东商智 (JD Shangzhi) Adapter — 京东电商数据
// ============================================================
// 京东商智是京东官方卖家数据工具
// 提供行业大盘、搜索分析、竞品数据
//
// Auth: App Key + App Secret + Access Token (京东开放平台OAuth)
// Key endpoints:
//   /api/keyword/trend       — 关键词趋势
//   /api/product/search      — 商品搜索
//   /api/category/hot        — 热门类目

import * as https from 'https';
import * as crypto from 'crypto';
import {
  MarketDataAdapter, PlatformCredentials, TrendResult, CompetitorResult,
  CompetitorItem, KeywordResult, registerAdapter
} from '../market-data-adapters';

class JdShangzhiAdapter implements MarketDataAdapter {
  readonly platformId = 'jd_shangzhi';
  readonly platformName = '京东商智';
  readonly supportedCapabilities = ['trends', 'competitors', 'keywords'];

  private appKey = '';
  private appSecret = '';
  private accessToken = '';

  configure(credentials: PlatformCredentials): void {
    this.appKey = credentials.app_key || '';
    this.appSecret = credentials.app_secret || '';
    this.accessToken = credentials.access_token || '';
  }

  async getTrends(keyword: string, period: string): Promise<TrendResult> {
    this.requireAuth();
    const data = await this.jdApiCall('jingdong.sz.read.data.query', {
      keyword,
      days: period.replace('d', ''),
      type: 'search_trend'
    });

    const trendData = data.data?.list || [];
    const dataPoints = trendData.map((item: any) => ({
      date: item.date || '',
      value: item.searchIndex || item.searchVolume || 0
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
      ? Math.round(dataPoints.reduce((s: number, d: any) => s + d.value, 0) / dataPoints.length) : 0;

    return { keyword, platform: this.platformName, period, search_index: avgValue, trend, data_points: dataPoints };
  }

  async getCompetitors(keyword: string, top: number): Promise<CompetitorResult> {
    this.requireAuth();
    const data = await this.jdApiCall('jingdong.sz.read.product.search', {
      keyword,
      page: '1',
      page_size: String(Math.min(top, 50)),
      sort: 'sales_desc'
    });

    const items: CompetitorItem[] = (data.data?.list || []).map((item: any) => ({
      title: item.wareName || item.title || '',
      price: parseFloat(item.price || '0'),
      currency: 'CNY',
      sales: item.monthlySales || item.sales || 0,
      rating: parseFloat(item.score || '0'),
      review_count: item.commentCount || 0,
      url: item.wareId ? `https://item.jd.com/${item.wareId}.html` : '',
      image_url: item.imageUrl || '',
      shop_name: item.shopName || '',
      extra: {
        ware_id: item.wareId,
        brand: item.brand,
        category: item.category
      }
    }));

    return { platform: this.platformName, items };
  }

  async getKeywords(keyword: string, options: { related?: boolean }): Promise<KeywordResult> {
    this.requireAuth();
    const data = await this.jdApiCall('jingdong.sz.read.keyword.query', { keyword });

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
    if (!this.appKey || !this.appSecret) {
      throw new Error(
        '京东商智需要 App Key 和 App Secret。\n' +
        '请在 https://open.jd.com 注册应用获取凭证，然后配置：\n' +
        '  market-data config set --platform jd_shangzhi --app-key "your_key" --app-secret "your_secret"'
      );
    }
  }

  private async jdApiCall(method: string, params: Record<string, string>): Promise<any> {
    const timestamp = new Date().toISOString().replace('T', ' ').slice(0, 19);

    const sysParams: Record<string, string> = {
      method,
      app_key: this.appKey,
      timestamp,
      format: 'json',
      v: '2.0',
      sign_method: 'md5'
    };

    if (this.accessToken) {
      sysParams.access_token = this.accessToken;
    }

    // MD5 sign
    const allParams = { ...sysParams, ...params };
    const sortedKeys = Object.keys(allParams).sort();
    const signStr = this.appSecret + sortedKeys.map(k => `${k}${allParams[k]}`).join('') + this.appSecret;
    const sign = crypto.createHash('md5').update(signStr, 'utf8').digest('hex').toUpperCase();
    sysParams.sign = sign;

    const qs = Object.entries({ ...sysParams, ...params })
      .map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`)
      .join('&');

    return this.httpGet(`https://api.jd.com/routerjson?${qs}`);
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
              reject(new Error(`京东商智 API 错误 [${parsed.code}]: ${parsed.message || parsed.msg || '未知错误'}`));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`京东商智返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });
      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('京东商智请求超时')); });
      req.end();
    });
  }
}

registerAdapter('jd_shangzhi', () => new JdShangzhiAdapter());
