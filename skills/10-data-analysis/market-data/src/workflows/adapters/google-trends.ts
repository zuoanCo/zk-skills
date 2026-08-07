// ============================================================
// Google Trends Adapter — 全球搜索趋势
// ============================================================
// Google Trends doesn't have an official public API.
// This adapter uses the unofficial endpoints:
//   /trends/api/dailytrends     — daily trending searches
//   /trends/api/widgetdata/multiline — interest over time
//   /trends/api/autocomplete    — related queries
//
// Requires browser-like headers and may need cookie for some regions.
// Free tier is very limited; consider using a proxy.

import * as https from 'https';
import {
  MarketDataAdapter, PlatformCredentials, TrendResult, KeywordResult,
  registerAdapter
} from '../market-data-adapters';

class GoogleTrendsAdapter implements MarketDataAdapter {
  readonly platformId = 'google_trends';
  readonly platformName = 'Google Trends';
  readonly supportedCapabilities = ['trends', 'keywords'];

  private cookie = '';

  configure(credentials: PlatformCredentials): void {
    this.cookie = credentials.cookie || '';
  }

  async getTrends(keyword: string, period: string): Promise<TrendResult> {
    // Map period to Google Trends date range
    const periodMap: Record<string, string> = {
      '7d': 'now 7-d',
      '30d': 'today 1-m',
      '90d': 'today 3-m',
      '180d': 'today 6-m',
      '1y': 'today 12-m'
    };
    const dateRange = periodMap[period] || 'today 3-m';

    // Step 1: Get explore token
    const exploreUrl = `https://trends.google.com/trends/api/explore?` +
      `hl=en-US&tz=-480&req=${encodeURIComponent(JSON.stringify({
        comparisonItem: [{ keyword, geo: '', time: dateRange }],
        category: 0,
        property: ''
      }))}`;

    const exploreData = await this.httpGet(exploreUrl, true);

    // Find the TIMESERIES widget token
    const widgets = exploreData.widgets || [];
    const timeseriesWidget = widgets.find((w: any) => w.id === 'TIMESERIES');
    if (!timeseriesWidget) {
      return { keyword, platform: this.platformName, period, search_index: 0, trend: 'stable', data_points: [] };
    }

    // Step 2: Get actual data
    const token = timeseriesWidget.token;
    const reqBody = timeseriesWidget.request;

    const dataUrl = `https://trends.google.com/trends/api/widgetdata/multiline?` +
      `hl=en-US&tz=-480&req=${encodeURIComponent(JSON.stringify(reqBody))}` +
      `&token=${encodeURIComponent(token)}`;

    const rawData = await this.httpGet(dataUrl, true);

    // Parse the timeline data
    const timelineData = rawData.default?.timelineData || [];
    const dataPoints = timelineData.map((point: any) => ({
      date: point.formattedAxisTime || point.time,
      value: point.value?.[0] || 0
    }));

    // Calculate trend direction
    let trend: 'rising' | 'stable' | 'declining' = 'stable';
    if (dataPoints.length >= 10) {
      const firstHalf = dataPoints.slice(0, Math.floor(dataPoints.length / 2));
      const secondHalf = dataPoints.slice(Math.floor(dataPoints.length / 2));
      const avgFirst = firstHalf.reduce((s: number, d: any) => s + d.value, 0) / firstHalf.length;
      const avgSecond = secondHalf.reduce((s: number, d: any) => s + d.value, 0) / secondHalf.length;
      if (avgSecond > avgFirst * 1.15) trend = 'rising';
      else if (avgSecond < avgFirst * 0.85) trend = 'declining';
    }

    const avgIndex = dataPoints.length > 0
      ? Math.round(dataPoints.reduce((s: number, d: any) => s + d.value, 0) / dataPoints.length)
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
    // Get autocomplete suggestions
    const autoUrl = `https://trends.google.com/trends/api/autocomplete/${encodeURIComponent(keyword)}?hl=en-US`;
    const autoData = await this.httpGet(autoUrl, true);

    const result: KeywordResult = {
      keyword,
      platform: this.platformName
    };

    if (options.related) {
      const topics = autoData.default?.topics || [];
      result.related_keywords = topics.map((t: any) => ({
        keyword: t.title || t.mid || '',
        volume: undefined
      }));
    }

    return result;
  }

  // ---- HTTP helper ----
  // Google Trends responses start with ")]}'\n" — strip it before parsing

  private httpGet(url: string, stripPrefix = false): Promise<any> {
    return new Promise((resolve, reject) => {
      const parsed = new URL(url);
      const options = {
        hostname: parsed.hostname,
        path: parsed.pathname + parsed.search,
        method: 'GET',
        headers: {
          'Cookie': this.cookie,
          'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
          'Accept': 'application/json, text/plain, */*',
          'Referer': 'https://trends.google.com/trends/',
          'Accept-Language': 'en-US,en;q=0.9'
        }
      };

      const req = https.request(options, (res) => {
        let data = '';
        res.on('data', chunk => data += chunk);
        res.on('end', () => {
          try {
            let jsonStr = data;
            if (stripPrefix && data.startsWith(")]}'")) {
              jsonStr = data.substring(data.indexOf('\n') + 1);
            }
            resolve(JSON.parse(jsonStr));
          } catch {
            reject(new Error(`Google Trends 返回非 JSON (status ${res.statusCode}): ${data.slice(0, 200)}`));
          }
        });
      });

      req.on('error', reject);
      req.setTimeout(15000, () => { req.destroy(); reject(new Error('Google Trends 请求超时')); });
      req.end();
    });
  }
}

registerAdapter('google_trends', () => new GoogleTrendsAdapter());
