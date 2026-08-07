// ============================================================
// 企查查 (Qichacha) Adapter — 企业信息查询/供应商背调
// ============================================================
// 企查查是国内领先的企业信息查询平台
// 用于供应商背景调查、工厂资质核实、风险评估
//
// Auth: API Key + API Secret (E-Business Certificate)
// Key endpoints:
//   /api/enterprise/search    — 企业搜索
//   /api/enterprise/detail    — 企业详情
//   /api/risk/check           — 风险查询
//   /api/ipr/trademark        — 商标查询

import * as https from 'https';
import * as crypto from 'crypto';
import {
  MarketDataAdapter, PlatformCredentials, SupplierResult, SupplierItem,
  registerAdapter
} from '../market-data-adapters';

class QichachaAdapter implements MarketDataAdapter {
  readonly platformId = 'qichacha';
  readonly platformName = '企查查';
  readonly supportedCapabilities = ['suppliers'];

  private apiKey = '';
  private apiSecret = '';

  configure(credentials: PlatformCredentials): void {
    this.apiKey = credentials.api_key || '';
    this.apiSecret = credentials.api_secret || '';
  }

  async getSuppliers(keyword: string): Promise<SupplierResult> {
    this.requireAuth();

    const data = await this.qccApiCall('/api/enterprise/search', {
      keyword,
      pageIndex: '1',
      pageSize: '20'
    });

    const items: SupplierItem[] = (data.Result || data.data || []).map((item: any) => ({
      company_name: item.Name || item.keyNo || '',
      product_name: keyword,
      price: 0, // 企查查不提供价格
      currency: 'CNY',
      location: item.RegistCapi ? `${item.Province || ''}${item.City || ''}` : (item.Address || ''),
      url: item.KeyNo ? `https://www.qcc.com/firm/${item.KeyNo}.html` : '',
      verified: (item.RegistCapi && parseFloat(item.RegistCapi) > 0) || false,
      years: item.StartDate ? Math.floor((Date.now() - new Date(item.StartDate).getTime()) / (365.25 * 86400000)) : undefined,
      extra: {
        key_no: item.KeyNo,
        legal_person: item.OperName,
        registered_capital: item.RegistCapi,
        established_date: item.StartDate,
        status: item.Status,
        industry: item.Scope,
        credit_code: item.CreditCode
      }
    }));

    return { platform: this.platformName, items };
  }

  private requireAuth(): void {
    if (!this.apiKey || !this.apiSecret) {
      throw new Error(
        '企查查需要 API Key 和 API Secret。\n' +
        '请在 https://open.qcc.com 注册开发者并购买 API 套餐，然后配置：\n' +
        '  market-data config set --platform qichacha --api-key "your_key" --api-secret "your_secret"'
      );
    }
  }

  private async qccApiCall(path: string, params: Record<string, string>): Promise<any> {
    const timestamp = String(Date.now());

    // 企查查签名: HMAC-SHA1(appSecret, "appKey={appKey}&timestamp={timestamp}&{params}")
    const sortedKeys = Object.keys(params).sort();
    const paramStr = sortedKeys.map(k => `${k}=${params[k]}`).join('&');
    const signStr = `appKey=${this.apiKey}&timestamp=${timestamp}&${paramStr}`;
    const signature = crypto.createHmac('sha1', this.apiSecret).update(signStr).digest('base64');

    const headers: Record<string, string> = {
      'User-Agent': 'market-data-cli/1.0',
      'Accept': 'application/json',
      'Token': signature,
      'Key': this.apiKey,
      'Timespan': timestamp
    };

    const qs = Object.entries(params).map(([k, v]) => `${encodeURIComponent(k)}=${encodeURIComponent(v)}`).join('&');
    return this.httpGet(`https://api.qichacha.com${path}?${qs}`, headers);
  }

  private httpGet(url: string, headers: Record<string, string> = {}): Promise<any> {
    return new Promise((resolve, reject) => {
      const parsed = new URL(url);
      const options = {
        hostname: parsed.hostname,
        path: parsed.pathname + parsed.search,
        method: 'GET',
        headers: { 'Accept': 'application/json', ...headers }
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            const parsed = JSON.parse(data);
            if (parsed.Status && parsed.Status !== '200' && parsed.Status !== 200) {
              reject(new Error(`企查查 API 错误 [${parsed.Status}]: ${parsed.Message || parsed.Message || '未知错误'}`));
            } else {
              resolve(parsed);
            }
          } catch {
            reject(new Error(`企查查返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('企查查请求超时')); });
      req.end();
    });
  }
}

registerAdapter('qichacha', () => new QichachaAdapter());
