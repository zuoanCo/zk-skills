// ============================================================
// 1688 (Alibaba) Adapter — 国内供应链/批发数据
// ============================================================
// 1688 Open Platform API: https://open.1688.com
// Supports: product search, supplier search, price comparison
//
// Auth: App Key + App Secret + Access Token (OAuth2)
// Key endpoints:
//   /openapi/param2/1/com.alibaba.product/alibaba.product.search
//   /openapi/param2/1/com.alibaba.product/alibaba.product.get
//   /openapi/param2/1/com.alibaba.supplier/supplier.search

import * as https from 'https';
import * as crypto from 'crypto';
import {
  MarketDataAdapter, PlatformCredentials, CompetitorResult, CompetitorItem,
  PriceResult, SupplierResult, SupplierItem, registerAdapter
} from '../market-data-adapters';

class Alibaba1688Adapter implements MarketDataAdapter {
  readonly platformId = 'alibaba1688';
  readonly platformName = '1688';
  readonly supportedCapabilities = ['competitors', 'prices', 'suppliers'];

  private appKey = '';
  private appSecret = '';
  private accessToken = '';

  configure(credentials: PlatformCredentials): void {
    this.appKey = credentials.app_key || '';
    this.appSecret = credentials.app_secret || '';
    this.accessToken = credentials.access_token || '';
  }

  async getCompetitors(keyword: string, top: number): Promise<CompetitorResult> {
    this.requireAuth();

    const params = {
      keyword,
      page: '1',
      pageSize: String(Math.min(top, 50)),
      sortType: 'va' // by sales volume
    };

    const data = await this.apiCall('alibaba.product.search', params);
    const items: CompetitorItem[] = (data.result?.toReturn || []).map((item: any) => ({
      title: item.subject || '',
      price: parseFloat(item.priceInfo?.[0]?.price || '0'),
      currency: 'CNY',
      sales: undefined, // 1688 doesn't expose exact sales in search
      url: item.productUrl || `https://detail.1688.com/offer/${item.offerId}.html`,
      image_url: item.image?.images?.[0] || '',
      shop_name: item.companyName || '',
      location: item.address || '',
      extra: {
        offer_id: item.offerId,
        company_type: item.companyType,
        trade_quantity: item.tradeQuantity
      }
    }));

    return { platform: this.platformName, items };
  }

  async getPrices(keyword: string, options: { history?: number }): Promise<PriceResult> {
    this.requireAuth();

    const params = {
      keyword,
      page: '1',
      pageSize: '20',
      sortType: 'p' // sort by price
    };

    const data = await this.apiCall('alibaba.product.search', params);
    const items = (data.result?.toReturn || []).map((item: any) => ({
      title: item.subject || '',
      current_price: parseFloat(item.priceInfo?.[0]?.price || '0'),
      currency: 'CNY',
      url: `https://detail.1688.com/offer/${item.offerId}.html`,
      shop_name: item.companyName || ''
    }));

    return { platform: this.platformName, items };
  }

  async getSuppliers(keyword: string): Promise<SupplierResult> {
    this.requireAuth();

    const params = {
      keyword,
      page: '1',
      pageSize: '20'
    };

    const data = await this.apiCall('alibaba.supplier.search', params);
    const items: SupplierItem[] = (data.result?.toReturn || []).map((item: any) => ({
      company_name: item.companyName || item.name || '',
      product_name: keyword,
      price: parseFloat(item.priceInfo?.price || '0'),
      currency: 'CNY',
      moq: item.minOrderQuantity ? parseInt(item.minOrderQuantity) : undefined,
      location: item.address || item.location || '',
      url: item.companyUrl || '',
      verified: item.creditLevel > 0 || false,
      years: item.years ? parseInt(item.years) : undefined,
      response_rate: item.responseRate || undefined,
      extra: {
        company_id: item.companyId,
        credit_level: item.creditLevel,
        trade_count: item.tradeCount
      }
    }));

    return { platform: this.platformName, items };
  }

  // ---- 1688 API call with signature ----

  private requireAuth(): void {
    if (!this.appKey || !this.appSecret) {
      throw new Error(
        '1688 需要 App Key 和 App Secret。\n' +
        '请在 https://open.1688.com 注册应用获取凭证，然后配置：\n' +
        '  market-data config set --platform alibaba1688 --app-key "your_key" --app-secret "your_secret"'
      );
    }
  }

  private async apiCall(apiPath: string, params: Record<string, string>): Promise<any> {
    const timestamp = String(Date.now());

    // Build parameter string for signing
    const allParams: Record<string, string> = {
      ...params,
      _aop_timestamp: timestamp,
      appKey: this.appKey
    };

    if (this.accessToken) {
      allParams.access_token = this.accessToken;
    }

    // Sort params and create sign string
    const sortedKeys = Object.keys(allParams).sort();
    const signStr = sortedKeys.map(k => `${k}${allParams[k]}`).join('');

    // HMAC-SHA256 signature
    const signature = crypto
      .createHmac('sha256', this.appSecret)
      .update(signStr)
      .digest('hex')
      .toUpperCase();

    // Build URL
    const qs = sortedKeys
      .map(k => `${encodeURIComponent(k)}=${encodeURIComponent(allParams[k])}`)
      .join('&');

    const url = `https://gw.open.1688.com/openapi/param2/1/com.alibaba.product/${apiPath}/${this.appKey}?${qs}&_aop_signature=${signature}`;

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
            if (parsed.errorCode) {
              reject(new Error(`1688 API 错误 [${parsed.errorCode}]: ${parsed.errorMessage || '未知错误'}`));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`1688 返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('1688 请求超时')); });
      req.end();
    });
  }
}

registerAdapter('alibaba1688', () => new Alibaba1688Adapter());
