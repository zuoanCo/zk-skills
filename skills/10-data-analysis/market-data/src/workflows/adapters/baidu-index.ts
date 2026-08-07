// ============================================================
// Baidu Index Adapter — 搜索趋势数据
// ============================================================
// Baidu Index provides search volume trends for Chinese keywords.
// Requires a valid Baidu cookie (login session).
// API: https://index.baidu.com
//
// Key endpoints:
//   /api/SearchApi/index    — search index data
//   /api/SugApi/sug        — related keyword suggestions
//   /api/WordGraph/multi    — word graph / related words
//
// The AES decrypt key is fetched from /Interface/ptbk?uniqid=...

import * as https from 'https';
import * as http from 'http';
import {
  MarketDataAdapter, PlatformCredentials, TrendResult, KeywordResult,
  registerAdapter
} from '../market-data-adapters';

class BaiduIndexAdapter implements MarketDataAdapter {
  readonly platformId = 'baidu_index';
  readonly platformName = '百度指数';
  readonly supportedCapabilities = ['trends', 'keywords'];

  private cookie = '';

  configure(credentials: PlatformCredentials): void {
    this.cookie = credentials.cookie || '';
  }

  async getTrends(keyword: string, period: string): Promise<TrendResult> {
    if (!this.cookie) {
      throw new Error('百度指数需要 cookie。请先登录 index.baidu.com 获取 cookie，然后配置：market-data config set --platform baidu_index --cookie "your_cookie"');
    }

    const daysMap: Record<string, number> = { '7d': 7, '30d': 30, '90d': 90, '180d': 180, '1y': 365 };
    const days = daysMap[period] || 30;

    const endDate = new Date().toISOString().slice(0, 10);
    const startDate = new Date(Date.now() - days * 86400000).toISOString().slice(0, 10);
    const dateRange = `${startDate},${endDate}`;

    // Step 1: Get uniqid
    const indexUrl = `https://index.baidu.com/api/SearchApi/index?area=0&word=${encodeURIComponent(JSON.stringify([[keyword]]))}&days=${days}&date=${dateRange}`;
    const indexData = await this.httpGet(indexUrl);

    if (indexData.status !== 0 && indexData.status !== 200) {
      throw new Error(`百度指数 API 错误: ${indexData.message || JSON.stringify(indexData)}`);
    }

    const uniqid = indexData.data?.uniqid;
    if (!uniqid) {
      // Some keywords return data directly without encryption
      const allDate = indexData.data?.userIndexes?.[0]?.all?.startDate;
      if (!allDate) {
        return {
          keyword,
          platform: this.platformName,
          period,
          search_index: 0,
          trend: 'stable',
          data_points: []
        };
      }
    }

    // Step 2: Get decrypt key
    let decryptKey = '';
    if (uniqid) {
      const ptbkUrl = `https://index.baidu.com/Interface/ptbk?uniqid=${uniqid}`;
      const ptbkData = await this.httpGet(ptbkUrl);
      decryptKey = ptbkData.data || '';
    }

    // Step 3: Decrypt the data
    const encryptedData = indexData.data?.userIndexes?.[0]?.all?.data || '';
    let dataPoints: Array<{ date: string; value: number }> = [];

    if (encryptedData && decryptKey) {
      const values = this.decryptBaiduIndex(encryptedData, decryptKey);
      const startTs = new Date(indexData.data.userIndexes[0].all.startDate).getTime();

      dataPoints = values.map((v, i) => ({
        date: new Date(startTs + i * 86400000).toISOString().slice(0, 10),
        value: v
      }));
    }

    // Calculate trend
    let trend: 'rising' | 'stable' | 'declining' = 'stable';
    if (dataPoints.length >= 14) {
      const firstHalf = dataPoints.slice(0, Math.floor(dataPoints.length / 2));
      const secondHalf = dataPoints.slice(Math.floor(dataPoints.length / 2));
      const avgFirst = firstHalf.reduce((s, d) => s + d.value, 0) / firstHalf.length;
      const avgSecond = secondHalf.reduce((s, d) => s + d.value, 0) / secondHalf.length;
      if (avgSecond > avgFirst * 1.15) trend = 'rising';
      else if (avgSecond < avgFirst * 0.85) trend = 'declining';
    }

    const avgIndex = dataPoints.length > 0
      ? Math.round(dataPoints.reduce((s, d) => s + d.value, 0) / dataPoints.length)
      : 0;

    return {
      keyword,
      platform: this.platformName,
      period,
      search_index: avgIndex,
      trend,
      data_points: dataPoints
    };
  }

  async getKeywords(keyword: string, options: { related?: boolean; history?: boolean }): Promise<KeywordResult> {
    if (!this.cookie) {
      throw new Error('百度指数需要 cookie');
    }

    const result: KeywordResult = {
      keyword,
      platform: this.platformName
    };

    // Get related keywords via SugApi
    if (options.related) {
      const sugUrl = `https://index.baidu.com/api/SugApi/sug?inputword=${encodeURIComponent(keyword)}`;
      const sugData = await this.httpGet(sugUrl);

      if (sugData.data) {
        result.related_keywords = (Array.isArray(sugData.data) ? sugData.data : [])
          .map((item: any) => ({
            keyword: typeof item === 'string' ? item : item.word || item,
            volume: undefined
          }));
      }
    }

    // Get word graph
    const graphUrl = `https://index.baidu.com/api/WordGraph/multi?wordlist[]=${encodeURIComponent(keyword)}`;
    const graphData = await this.httpGet(graphUrl);

    if (graphData.data?.wordlist?.[0]?.wordGraph) {
      const graph = graphData.data.wordlist[0].wordGraph;
      if (!result.related_keywords) result.related_keywords = [];
      for (const item of graph) {
        if (!result.related_keywords.find(r => r.keyword === item.word)) {
          result.related_keywords.push({ keyword: item.word, volume: item.pv });
        }
      }
    }

    return result;
  }

  // ---- Baidu Index AES-like decryption ----
  private decryptBaiduIndex(encrypted: string, key: string): number[] {
    // Baidu uses a custom substitution cipher, not standard AES
    // The key maps positions: key[i] → original position
    const keyLen = key.length;
    const halfLen = Math.floor(keyLen / 2);
    const a: Record<string, string> = {};

    for (let i = 0; i < halfLen; i++) {
      a[key[i]] = key[halfLen + i];
    }

    // Decrypt: substitute each character using the mapping
    let decrypted = '';
    for (const ch of encrypted) {
      decrypted += a[ch] || ch;
    }

    // Split by comma to get values
    return decrypted.split(',').map(v => parseInt(v, 10)).filter(v => !isNaN(v));
  }

  // ---- HTTP helper ----
  private httpGet(url: string): Promise<any> {
    return new Promise((resolve, reject) => {
      const parsed = new URL(url);
      const options = {
        hostname: parsed.hostname,
        path: parsed.pathname + parsed.search,
        method: 'GET',
        headers: {
          'Cookie': this.cookie,
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
          'Referer': 'https://index.baidu.com/v2/index.html',
          'Accept': 'application/json, text/plain, */*'
        }
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            resolve(JSON.parse(data));
          } catch {
            reject(new Error(`百度指数返回非 JSON: ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('百度指数请求超时')); });
      req.end();
    });
  }
}

registerAdapter('baidu_index', () => new BaiduIndexAdapter());
