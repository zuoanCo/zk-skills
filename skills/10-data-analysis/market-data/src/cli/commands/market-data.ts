import { Command } from 'commander';
import { OutputOptions, success, failure } from '../output';
import {
  loadConfig, configStatus, configSet, configEnable,
  configMode, resolveMode, getEnabledPlatforms, getPlatformConfig,
  getAllPlatformIds, getPlatformMode, getPlatformCredentialFields
} from '../../workflows/market-data';
import { createAdapter, getRegisteredAdapters } from '../../workflows/market-data-adapters';

// ============================================================
// market-data CLI commands
// ============================================================

function output(result: any, opts: OutputOptions) {
  if (result.ok === false) {
    failure(result.error, opts);
    process.exit(1);
  } else {
    success(result.data || result, opts);
  }
}

export function registerMarketDataCommands(program: Command): void {
  const md = program.command('market-data')
    .description('Market data platform integration — domestic & international e-commerce data');

  // ---- config ----
  const config = md.command('config')
    .description('Manage market data platform configuration');

  config.command('status')
    .description('Show current configuration and enabled platforms')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      output(configStatus(), outputOpts);
    });

  config.command('set')
    .description('Set credentials for a platform')
    .requiredOption('--platform <platformId>', 'Platform ID (e.g. chanmama, keepa, alibaba1688)')
    .option('--api-key <value>', 'API key')
    .option('--api-secret <value>', 'API secret')
    .option('--app-key <value>', 'App key')
    .option('--app-secret <value>', 'App secret')
    .option('--access-token <value>', 'Access token')
    .option('--refresh-token <value>', 'Refresh token')
    .option('--cookie <value>', 'Cookie / session string')
    .option('--shop-id <value>', 'Shop/store ID')
    .option('--partner-id <value>', 'Partner ID (Shopee)')
    .option('--partner-key <value>', 'Partner key (Shopee)')
    .option('--shop-domain <value>', 'Shop domain (Shopify)')
    .option('--lwa-app-id <value>', 'LWA App ID (Amazon)')
    .option('--lwa-client-secret <value>', 'LWA Client Secret (Amazon)')
    .option('--aws-access-key <value>', 'AWS Access Key (Amazon)')
    .option('--aws-secret-key <value>', 'AWS Secret Key (Amazon)')
    .option('--role-arn <value>', 'IAM Role ARN (Amazon)')
    .option('--marketplace <value>', 'Marketplace ID (Amazon)')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };

      // Collect all non-empty credential options into a flat record
      const credentials: Record<string, string> = {};
      const optionMap: Record<string, string> = {
        'apiKey': 'api_key',
        'apiSecret': 'api_secret',
        'appKey': 'app_key',
        'appSecret': 'app_secret',
        'accessToken': 'access_token',
        'refreshToken': 'refresh_token',
        'cookie': 'cookie',
        'shopId': 'shop_id',
        'partnerId': 'partner_id',
        'partnerKey': 'partner_key',
        'shopDomain': 'shop_domain',
        'lwaAppId': 'lwa_app_id',
        'lwaClientSecret': 'lwa_client_secret',
        'awsAccessKey': 'aws_access_key',
        'awsSecretKey': 'aws_secret_key',
        'roleArn': 'role_arn',
        'marketplace': 'marketplace'
      };

      for (const [camel, snake] of Object.entries(optionMap)) {
        if (opts[camel]) credentials[snake] = opts[camel];
      }

      if (Object.keys(credentials).length === 0) {
        output({ ok: false, error: { code: 'invalid_input', message: 'No credentials provided. Use --api-key, --app-key, --cookie, etc.' } }, outputOpts);
        return;
      }

      output(configSet(opts.platform, credentials), outputOpts);
    });

  config.command('mode <mode>')
    .description('Set operating mode: auto, domestic, international, both')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(function (this: Command, modeArg: string) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      output(configMode(modeArg), outputOpts);
    });

  config.command('enable')
    .description('Enable a platform')
    .requiredOption('--platform <platformId>', 'Platform ID')
    .option('--pretty', 'Pretty print JSON output')
    .action(function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty };
      output(configEnable(opts.platform, true), outputOpts);
    });

  config.command('disable')
    .description('Disable a platform')
    .requiredOption('--platform <platformId>', 'Platform ID')
    .option('--pretty', 'Pretty print JSON output')
    .action(function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty };
      output(configEnable(opts.platform, false), outputOpts);
    });

  config.command('list')
    .description('List all available platforms')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      const config = loadConfig();
      const platforms = getAllPlatformIds().map(id => {
        const plat = getPlatformConfig(config, id);
        return {
          id,
          name: plat?.name || id,
          category: getPlatformMode(id),
          enabled: plat?.enabled || false,
          credential_fields: getPlatformCredentialFields(id)
        };
      });
      output({ ok: true, data: platforms }, outputOpts);
    });

  // ---- trends ----
  md.command('trends')
    .description('Analyze market trends for a keyword')
    .requiredOption('--keyword <keyword>', 'Search keyword')
    .option('--market <market>', 'domestic / international / all (default: auto)')
    .option('--period <period>', 'Time range: 7d/30d/90d/180d/1y (default: 30d)')
    .option('--platform <platform>', 'Specific platform to query')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(async function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      const result = requireEnabledPlatforms(opts.market, opts.platform);
      if (!result.ok) { output(result, outputOpts); return; }

      const keyword = opts.keyword;
      const period = opts.period || '30d';
      const results: any[] = [];
      const errors: any[] = [];

      for (const pid of result.data!.enabled) {
        const plat = getPlatformConfig(loadConfig(), pid);
        if (!plat) continue;
        const adapter = createAdapter(pid, plat);
        if (!adapter || !adapter.getTrends) continue;
        try {
          const data = await adapter.getTrends(keyword, period);
          results.push(data);
        } catch (err: any) {
          errors.push({ platform: pid, error: err.message });
        }
      }

      if (results.length === 0 && errors.length > 0) {
        output({ ok: false, error: { code: 'adapter_error', message: errors.map(e => `[${e.platform}] ${e.error}`).join('\n') } }, outputOpts);
        return;
      }

      output({
        ok: true,
        data: {
          keyword,
          period,
          results,
          errors: errors.length > 0 ? errors : undefined
        }
      }, outputOpts);
    });

  // ---- competitor ----
  md.command('competitor')
    .description('Competitor analysis')
    .option('--keyword <keyword>', 'Search by keyword')
    .option('--asin <asin>', 'Amazon ASIN')
    .option('--url <url>', 'Product URL')
    .option('--market <market>', 'domestic / international / all')
    .option('--top <n>', 'Return top N competitors (default: 10)')
    .option('--fields <fields>', 'Comma-separated: price,sales,rating,review_count,bsr')
    .option('--platform <platform>', 'Specific platform')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(async function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      const result = requireEnabledPlatforms(opts.market, opts.platform);
      if (!result.ok) { output(result, outputOpts); return; }

      const query = opts.keyword || opts.asin || opts.url;
      const top = parseInt(opts.top) || 10;
      const results: any[] = [];
      const errors: any[] = [];

      for (const pid of result.data!.enabled) {
        const plat = getPlatformConfig(loadConfig(), pid);
        if (!plat) continue;
        const adapter = createAdapter(pid, plat);
        if (!adapter || !adapter.getCompetitors) continue;
        try {
          const data = await adapter.getCompetitors(query, top);
          results.push(data);
        } catch (err: any) {
          errors.push({ platform: pid, error: err.message });
        }
      }

      if (results.length === 0 && errors.length > 0) {
        output({ ok: false, error: { code: 'adapter_error', message: errors.map(e => `[${e.platform}] ${e.error}`).join('\n') } }, outputOpts);
        return;
      }

      output({ ok: true, data: { query, top, results, errors: errors.length > 0 ? errors : undefined } }, outputOpts);
    });

  // ---- product-select ----
  md.command('product-select')
    .description('Product selection analysis')
    .option('--category <category>', 'Product category')
    .option('--keyword <keyword>', 'Keyword')
    .option('--market <market>', 'domestic / international / all')
    .option('--budget <budget>', 'Max procurement price')
    .option('--min-margin <margin>', 'Minimum profit margin (e.g. 30%)')
    .option('--min-sales <sales>', 'Minimum monthly sales')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      const result = requireEnabledPlatforms(opts.market, opts.platform);
      if (!result.ok) { output(result, outputOpts); return; }
      output({
        ok: true,
        data: {
          query: opts.category || opts.keyword,
          market: opts.market || 'auto',
          budget: opts.budget,
          min_margin: opts.minMargin,
          platforms_queried: result.data!.enabled,
          status: 'platform_adapter_not_implemented'
        }
      }, outputOpts);
    });

  // ---- keyword ----
  md.command('keyword')
    .description('Keyword analysis')
    .requiredOption('--word <word>', 'Target keyword')
    .option('--market <market>', 'domestic / international / all')
    .option('--related', 'Include related keywords')
    .option('--history', 'Include search trend history')
    .option('--platform <platform>', 'Specific platform')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(async function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      const result = requireEnabledPlatforms(opts.market, opts.platform);
      if (!result.ok) { output(result, outputOpts); return; }

      const results: any[] = [];
      const errors: any[] = [];
      for (const pid of result.data!.enabled) {
        const plat = getPlatformConfig(loadConfig(), pid);
        if (!plat) continue;
        const adapter = createAdapter(pid, plat);
        if (!adapter || !adapter.getKeywords) continue;
        try {
          const data = await adapter.getKeywords(opts.word, { related: opts.related, history: opts.history });
          results.push(data);
        } catch (err: any) {
          errors.push({ platform: pid, error: err.message });
        }
      }

      if (results.length === 0 && errors.length > 0) {
        output({ ok: false, error: { code: 'adapter_error', message: errors.map(e => `[${e.platform}] ${e.error}`).join('\n') } }, outputOpts);
        return;
      }
      output({ ok: true, data: { keyword: opts.word, results, errors: errors.length > 0 ? errors : undefined } }, outputOpts);
    });

  // ---- price ----
  md.command('price')
    .description('Price monitoring')
    .option('--keyword <keyword>', 'Product keyword')
    .option('--asin <asin>', 'Amazon ASIN')
    .option('--url <url>', 'Product URL')
    .option('--market <market>', 'domestic / international / all')
    .option('--alert-below <price>', 'Alert when price drops below')
    .option('--alert-above <price>', 'Alert when price rises above')
    .option('--history <days>', 'Show price history for N days')
    .option('--platform <platform>', 'Specific platform')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(async function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      const result = requireEnabledPlatforms(opts.market, opts.platform);
      if (!result.ok) { output(result, outputOpts); return; }

      const query = opts.keyword || opts.asin || opts.url;
      const results: any[] = [];
      const errors: any[] = [];
      for (const pid of result.data!.enabled) {
        const plat = getPlatformConfig(loadConfig(), pid);
        if (!plat) continue;
        const adapter = createAdapter(pid, plat);
        if (!adapter || !adapter.getPrices) continue;
        try {
          const data = await adapter.getPrices(query, { history: opts.history ? parseInt(opts.history) : undefined });
          results.push(data);
        } catch (err: any) {
          errors.push({ platform: pid, error: err.message });
        }
      }

      if (results.length === 0 && errors.length > 0) {
        output({ ok: false, error: { code: 'adapter_error', message: errors.map(e => `[${e.platform}] ${e.error}`).join('\n') } }, outputOpts);
        return;
      }
      output({ ok: true, data: { query, alert_below: opts.alertBelow, alert_above: opts.alertAbove, results, errors: errors.length > 0 ? errors : undefined } }, outputOpts);
    });

  // ---- supplier ----
  md.command('supplier')
    .description('Supplier search')
    .option('--keyword <keyword>', 'Product keyword')
    .option('--company <company>', 'Company name')
    .option('--platform <platform>', 'Specific platform (e.g. alibaba1688, qichacha)')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(async function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      const result = requireEnabledPlatforms('domestic', opts.platform);
      if (!result.ok) { output(result, outputOpts); return; }

      const query = opts.keyword || opts.company;
      const results: any[] = [];
      const errors: any[] = [];
      for (const pid of result.data!.enabled) {
        const plat = getPlatformConfig(loadConfig(), pid);
        if (!plat) continue;
        const adapter = createAdapter(pid, plat);
        if (!adapter || !adapter.getSuppliers) continue;
        try {
          const data = await adapter.getSuppliers(query);
          results.push(data);
        } catch (err: any) {
          errors.push({ platform: pid, error: err.message });
        }
      }

      if (results.length === 0 && errors.length > 0) {
        output({ ok: false, error: { code: 'adapter_error', message: errors.map(e => `[${e.platform}] ${e.error}`).join('\n') } }, outputOpts);
        return;
      }
      output({ ok: true, data: { query, results, errors: errors.length > 0 ? errors : undefined } }, outputOpts);
    });

  // ---- report ----
  md.command('report')
    .description('Generate comprehensive market analysis report')
    .requiredOption('--keyword <keyword>', 'Product keyword')
    .option('--market <market>', 'domestic / international / both (default: both)')
    .option('--format <format>', 'Output format: json/markdown (default: markdown)')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      const result = requireEnabledPlatforms(opts.market || 'both', undefined);
      if (!result.ok) { output(result, outputOpts); return; }
      output({
        ok: true,
        data: {
          keyword: opts.keyword,
          market: opts.market || 'both',
          format: opts.format || 'markdown',
          platforms_queried: result.data!.enabled,
          status: 'platform_adapter_not_implemented',
          message: 'Full report generation requires platform adapters to be implemented'
        }
      }, outputOpts);
    });

  // ---- compare (ERP + market data) ----
  md.command('compare')
    .description('Compare internal ERP data with market data')
    .requiredOption('--keyword <keyword>', 'Market keyword')
    .option('--erp-product <product>', 'Product name in ERP (default: same as keyword)')
    .option('--pretty', 'Pretty print JSON output')
    .option('--raw', 'Raw JSON output')
    .action(function (this: Command) {
      const opts = this.optsWithGlobals ? this.optsWithGlobals() : this.opts();
      const outputOpts: OutputOptions = { pretty: opts.pretty, raw: opts.raw };
      const result = requireEnabledPlatforms('all', undefined);
      if (!result.ok) { output(result, outputOpts); return; }
      output({
        ok: true,
        data: {
          keyword: opts.keyword,
          erp_product: opts.erpProduct || opts.keyword,
          platforms_queried: result.data!.enabled,
          status: 'platform_adapter_not_implemented',
          message: 'ERP comparison requires both market data adapters and Odoo integration'
        }
      }, outputOpts);
    });
}

// ---- Helper: check if any platforms are enabled for the requested market ----

function requireEnabledPlatforms(
  market: string | undefined,
  specificPlatform: string | undefined
): { ok: boolean; data?: { enabled: string[] }; error?: { code: string; message: string } } {
  const config = loadConfig();
  const enabled = getEnabledPlatforms(config);

  // If a specific platform is requested
  if (specificPlatform) {
    // free_sources is always available
    if (specificPlatform === 'free_sources') {
      return { ok: true, data: { enabled: ['free_sources'] } };
    }
    const plat = getPlatformConfig(config, specificPlatform);
    if (!plat || !plat.enabled) {
      return {
        ok: false,
        error: {
          code: 'platform_not_configured',
          message: `Platform "${specificPlatform}" is not configured or not enabled. Run:\n  market-data config set --platform ${specificPlatform} --api-key "your_key"\n  market-data config enable --platform ${specificPlatform}`
        }
      };
    }
    return { ok: true, data: { enabled: [specificPlatform] } };
  }

  // Determine effective market
  const resolvedMode = resolveMode(config);
  const effectiveMarket = market || resolvedMode;

  let relevantPlatforms: string[] = [];

  if (effectiveMarket === 'domestic') {
    relevantPlatforms = enabled.domestic;
  } else if (effectiveMarket === 'international') {
    relevantPlatforms = enabled.international;
  } else {
    // 'both' or 'all'
    relevantPlatforms = [...new Set([...enabled.domestic, ...enabled.international])];
  }

  if (relevantPlatforms.length === 0) {
    // free_sources is always available — no error needed
  }

  // Always include free_sources (no credentials required)
  return { ok: true, data: { enabled: [...new Set([...relevantPlatforms, 'free_sources'])] } };
}
