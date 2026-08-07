// ============================================================
// Market Data Platform Adapter Framework
// ============================================================

// ---- Common types ----

export interface TrendResult {
  keyword: string;
  platform: string;
  period: string;
  search_index?: number;
  trend?: 'rising' | 'stable' | 'declining';
  data_points?: Array<{ date: string; value: number }>;
  related_keywords?: string[];
}

export interface CompetitorResult {
  platform: string;
  items: CompetitorItem[];
}

export interface CompetitorItem {
  title: string;
  price: number;
  currency: string;
  sales?: number;
  rating?: number;
  review_count?: number;
  url?: string;
  image_url?: string;
  shop_name?: string;
  location?: string;
  extra?: Record<string, any>;
}

export interface KeywordResult {
  keyword: string;
  platform: string;
  search_volume?: number;
  competition?: 'high' | 'medium' | 'low';
  cpc?: number;
  related_keywords?: Array<{ keyword: string; volume?: number }>;
  history?: Array<{ date: string; value: number }>;
}

export interface PriceResult {
  platform: string;
  items: PriceItem[];
}

export interface PriceItem {
  title: string;
  current_price: number;
  currency: string;
  url?: string;
  price_history?: Array<{ date: string; price: number }>;
  shop_name?: string;
}

export interface SupplierResult {
  platform: string;
  items: SupplierItem[];
}

export interface SupplierItem {
  company_name: string;
  product_name: string;
  price: number;
  currency: string;
  moq?: number;
  location?: string;
  url?: string;
  verified?: boolean;
  years?: number;
  response_rate?: string;
  extra?: Record<string, any>;
}

export interface PlatformCredentials {
  [key: string]: string;
}

// ---- Adapter interface ----

export interface MarketDataAdapter {
  readonly platformId: string;
  readonly platformName: string;
  readonly supportedCapabilities: string[];

  // Initialize with credentials
  configure(credentials: PlatformCredentials): void;

  // Core capabilities
  getTrends?(keyword: string, period: string): Promise<TrendResult>;
  getCompetitors?(keyword: string, top: number): Promise<CompetitorResult>;
  getKeywords?(keyword: string, options: { related?: boolean; history?: boolean }): Promise<KeywordResult>;
  getPrices?(keyword: string, options: { history?: number }): Promise<PriceResult>;
  getSuppliers?(keyword: string): Promise<SupplierResult>;
}

// ---- Adapter registry ----

const adapterRegistry = new Map<string, () => MarketDataAdapter>();

export function registerAdapter(platformId: string, factory: () => MarketDataAdapter): void {
  adapterRegistry.set(platformId, factory);
}

export function createAdapter(platformId: string, credentials: PlatformCredentials): MarketDataAdapter | null {
  const factory = adapterRegistry.get(platformId);
  if (!factory) return null;
  const adapter = factory();
  adapter.configure(credentials);
  return adapter;
}

export function getRegisteredAdapters(): string[] {
  return Array.from(adapterRegistry.keys());
}

// ---- Import and register adapters ----
// Each adapter file calls registerAdapter() at module load time

import './adapters/baidu-index';
import './adapters/alibaba1688';
import './adapters/keepa';
import './adapters/google-trends';
import './adapters/seller-spirit';
import './adapters/chanmama';
import './adapters/feigua';
import './adapters/douchacha';
import './adapters/pdd-duoduo';
import './adapters/jd-shangzhi';
import './adapters/qichacha';
import './adapters/free-sources';
