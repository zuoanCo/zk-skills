import * as fs from 'fs';
import * as path from 'path';

// ============================================================
// Market Data Configuration Manager
// ============================================================

const CONFIG_PATH = path.join(__dirname, '..', '..', 'skills', 'market-data', 'config.json');

interface PlatformConfig {
  enabled: boolean;
  name: string;
  description: string;
  [key: string]: any;
}

interface MarketDataConfig {
  mode: 'auto' | 'domestic' | 'international' | 'both';
  platforms: {
    domestic: Record<string, PlatformConfig>;
    international: Record<string, PlatformConfig>;
    shared: Record<string, PlatformConfig>;
  };
}

// Platform → mode mapping
const PLATFORM_MODES: Record<string, 'domestic' | 'international' | 'shared'> = {
  // Free sources (always available, domestic + international)
  free_sources: 'shared',
  // Domestic
  shengyicanmou: 'domestic',
  alibaba1688: 'domestic',
  chanmama: 'domestic',
  feigua: 'domestic',
  douchacha: 'domestic',
  pdd_duoduo: 'domestic',
  jd_shangzhi: 'domestic',
  baidu_index: 'domestic',
  wechat_index: 'domestic',
  qichacha: 'domestic',
  tianyancha: 'domestic',
  // International
  seller_spirit: 'international',
  keepa: 'international',
  helium10: 'international',
  jungle_scout: 'international',
  amzscout: 'international',
  ciel: 'international',
  amazon_sp_api: 'international',
  aliexpress_api: 'international',
  shopee_api: 'international',
  shopify_api: 'international',
  diantu_shijue: 'international',
  google_trends: 'international',
  // Shared (count as both)
  dianxiaomi: 'shared',
  mabang: 'shared',
  tongtool: 'shared',
  mangguo: 'shared',
  saihe: 'shared',
  yishutong: 'shared'
};

// Credential field names per platform (used for config set)
const PLATFORM_CREDENTIAL_FIELDS: Record<string, string[]> = {
  free_sources: [],  // 无需凭证
  shengyicanmou: ['app_key', 'app_secret', 'access_token', 'shop_id'],
  alibaba1688: ['app_key', 'app_secret', 'access_token'],
  chanmama: ['api_key', 'api_secret'],
  feigua: ['api_key', 'api_secret'],
  douchacha: ['api_key'],
  pdd_duoduo: ['api_key', 'api_secret'],
  jd_shangzhi: ['app_key', 'app_secret', 'access_token'],
  baidu_index: ['cookie'],
  wechat_index: ['cookie'],
  qichacha: ['api_key', 'api_secret'],
  tianyancha: ['api_key', 'api_secret'],
  seller_spirit: ['api_key', 'api_secret'],
  keepa: ['api_key'],
  helium10: ['api_key', 'api_secret'],
  jungle_scout: ['api_key', 'api_secret'],
  amzscout: ['api_key'],
  ciel: ['api_key'],
  amazon_sp_api: ['refresh_token', 'lwa_app_id', 'lwa_client_secret', 'aws_access_key', 'aws_secret_key', 'role_arn'],
  aliexpress_api: ['app_key', 'app_secret', 'access_token'],
  shopee_api: ['partner_id', 'partner_key', 'shop_id', 'access_token', 'refresh_token'],
  shopify_api: ['shop_domain', 'access_token'],
  diantu_shijue: ['api_key'],
  google_trends: ['cookie'],
  dianxiaomi: ['app_key', 'app_secret', 'access_token'],
  mabang: ['app_key', 'app_secret', 'access_token'],
  tongtool: ['app_key', 'app_secret', 'access_token'],
  mangguo: ['app_key', 'app_secret', 'access_token'],
  saihe: ['api_key', 'api_secret'],
  yishutong: ['api_key']
};

// ---- Config I/O ----

export function loadConfig(): MarketDataConfig {
  try {
    const raw = fs.readFileSync(CONFIG_PATH, 'utf-8');
    return JSON.parse(raw);
  } catch {
    return { mode: 'auto', platforms: { domestic: {}, international: {}, shared: {} } };
  }
}

export function saveConfig(config: MarketDataConfig): void {
  fs.writeFileSync(CONFIG_PATH, JSON.stringify(config, null, 2) + '\n', 'utf-8');
}

// ---- Platform queries ----

export function getEnabledPlatforms(config: MarketDataConfig): { domestic: string[]; international: string[] } {
  const result: { domestic: string[]; international: string[] } = { domestic: [], international: [] };

  for (const [id, plat] of Object.entries(config.platforms.domestic)) {
    if (plat.enabled) result.domestic.push(id);
  }
  for (const [id, plat] of Object.entries(config.platforms.international)) {
    if (plat.enabled) result.international.push(id);
  }
  for (const [id, plat] of Object.entries(config.platforms.shared)) {
    if (plat.enabled) {
      result.domestic.push(id);
      result.international.push(id);
    }
  }
  return result;
}

export function resolveMode(config: MarketDataConfig): 'domestic' | 'international' | 'both' {
  if (config.mode !== 'auto') return config.mode;

  const enabled = getEnabledPlatforms(config);
  const hasDomestic = enabled.domestic.length > 0;
  const hasInternational = enabled.international.length > 0;

  if (hasDomestic && hasInternational) return 'both';
  if (hasDomestic) return 'domestic';
  if (hasInternational) return 'international';
  return 'both'; // nothing configured
}

export function getPlatformConfig(config: MarketDataConfig, platformId: string): PlatformConfig | null {
  return config.platforms.domestic[platformId]
    || config.platforms.international[platformId]
    || config.platforms.shared[platformId]
    || null;
}

export function getAllPlatformIds(): string[] {
  return Object.keys(PLATFORM_MODES);
}

export function getPlatformMode(platformId: string): string {
  return PLATFORM_MODES[platformId] || 'unknown';
}

export function getPlatformCredentialFields(platformId: string): string[] {
  return PLATFORM_CREDENTIAL_FIELDS[platformId] || ['api_key'];
}

// ---- Config commands ----

export function configStatus(): any {
  const config = loadConfig();
  const mode = resolveMode(config);
  const enabled = getEnabledPlatforms(config);

  const allPlatforms: Array<{ id: string; name: string; category: string; enabled: boolean }> = [];

  for (const [id, plat] of Object.entries(config.platforms.domestic)) {
    allPlatforms.push({ id, name: plat.name, category: 'domestic', enabled: plat.enabled });
  }
  for (const [id, plat] of Object.entries(config.platforms.international)) {
    allPlatforms.push({ id, name: plat.name, category: 'international', enabled: plat.enabled });
  }
  for (const [id, plat] of Object.entries(config.platforms.shared)) {
    allPlatforms.push({ id, name: plat.name, category: 'shared', enabled: plat.enabled });
  }

  return {
    ok: true,
    data: {
      configured_mode: config.mode,
      resolved_mode: mode,
      enabled_count: {
        domestic: enabled.domestic.length,
        international: enabled.international.length
      },
      platforms: allPlatforms
    }
  };
}

export function configSet(platformId: string, credentials: Record<string, string>): any {
  const config = loadConfig();

  // Find the platform in all categories
  let target: PlatformConfig | null = null;
  let targetCategory: string | null = null;

  for (const cat of ['domestic', 'international', 'shared'] as const) {
    if (config.platforms[cat][platformId]) {
      target = config.platforms[cat][platformId];
      targetCategory = cat;
      break;
    }
  }

  if (!target || !targetCategory) {
    return {
      ok: false,
      error: { code: 'not_found', message: `Unknown platform: "${platformId}". Run "market-data config status" to see available platforms.` }
    };
  }

  // Apply credentials
  for (const [key, value] of Object.entries(credentials)) {
    target[key] = value;
  }

  // Auto-enable when credentials are set
  const requiredFields = PLATFORM_CREDENTIAL_FIELDS[platformId] || [];
  const hasAnyCredential = requiredFields.some(f => credentials[f] || target![f]);
  if (hasAnyCredential) {
    target.enabled = true;
  }

  saveConfig(config);

  return {
    ok: true,
    data: {
      platform: target.name,
      category: targetCategory,
      enabled: target.enabled,
      updated_fields: Object.keys(credentials)
    }
  };
}

export function configEnable(platformId: string, enable: boolean): any {
  const config = loadConfig();

  for (const cat of ['domestic', 'international', 'shared'] as const) {
    if (config.platforms[cat][platformId]) {
      config.platforms[cat][platformId].enabled = enable;
      saveConfig(config);
      return {
        ok: true,
        data: {
          platform: config.platforms[cat][platformId].name,
          enabled: enable
        }
      };
    }
  }

  return {
    ok: false,
    error: { code: 'not_found', message: `Unknown platform: "${platformId}"` }
  };
}

export function configMode(mode: string): any {
  const valid = ['auto', 'domestic', 'international', 'both'];
  if (!valid.includes(mode)) {
    return {
      ok: false,
      error: { code: 'invalid_input', message: `Invalid mode: "${mode}". Must be one of: ${valid.join(', ')}` }
    };
  }

  const config = loadConfig();
  config.mode = mode as MarketDataConfig['mode'];
  saveConfig(config);

  const resolved = resolveMode(config);
  return {
    ok: true,
    data: { configured_mode: mode, resolved_mode: resolved }
  };
}
