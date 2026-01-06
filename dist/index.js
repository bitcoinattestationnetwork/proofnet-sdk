/**
 * Proofnet SDK (JS)
 * - Small fetch-based client helpers for Proofnet core services.
 * - Intentionally minimal: no deps, no retries, safe defaults.
 */

function normalizeBaseUrl(baseUrl) {
  if (typeof baseUrl !== "string" || !baseUrl.trim()) return "";
  return baseUrl.replace(/\/+$/, "");
}

export function resolveCoreBaseUrl(env = process.env) {
  return normalizeBaseUrl(
    env?.NEXT_PUBLIC_CORE_API_BASE_URL ??
      env?.NEXT_PUBLIC_CORE_BACKEND_BASE_URL ??
      env?.CORE_API_BASE_URL ??
      "http://127.0.0.1:25556"
  );
}

export function resolveProofwalletBaseUrl(env = process.env) {
  return normalizeBaseUrl(
    env?.NEXT_PUBLIC_PROOFWALLET_API_BASE_URL ??
      env?.PROOFWALLET_API_BASE_URL ??
      "http://127.0.0.1:9756"
  );
}

export function resolveNativeExplorerBaseUrl(env = process.env) {
  return normalizeBaseUrl(
    env?.NEXT_PUBLIC_NATIVE_EXPLORER_BASE_URL ??
      env?.NATIVE_EXPLORER_BASE_URL ??
      "http://127.0.0.1:3006"
  );
}

export async function getJson(url, { timeoutMs = 1500, headers } = {}) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(url, {
      method: "GET",
      headers,
      signal: controller.signal,
    });
    const text = await resp.text();
    let data = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch {
      data = null;
    }
    return { ok: resp.ok, status: resp.status, data };
  } finally {
    clearTimeout(timeout);
  }
}

export async function postJson(
  url,
  payload,
  { timeoutMs = 2500, headers } = {}
) {
  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), timeoutMs);
  try {
    const resp = await fetch(url, {
      method: "POST",
      headers: { "Content-Type": "application/json", ...(headers ?? {}) },
      body: payload === undefined ? undefined : JSON.stringify(payload),
      signal: controller.signal,
    });
    const text = await resp.text();
    let data = null;
    try {
      data = text ? JSON.parse(text) : null;
    } catch {
      data = null;
    }
    return { ok: resp.ok, status: resp.status, data };
  } finally {
    clearTimeout(timeout);
  }
}

export async function getVnovaPrices(
  baseUrl,
  { maxAgeSec = 600, timeoutMs = 1500 } = {}
) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/vnova/prices?max_age_sec=${Number(maxAgeSec) || 600}`;
  return getJson(url, { timeoutMs });
}

export async function getVnovaHealth(baseUrl, { timeoutMs = 1500 } = {}) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/vnova/health`;
  return getJson(url, { timeoutMs });
}

export async function getVnovaOverview(baseUrl, { timeoutMs = 1500 } = {}) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/vnova/overview`;
  return getJson(url, { timeoutMs });
}

export async function getApiStatus(baseUrl, { timeoutMs = 1500 } = {}) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/api/status`;
  return getJson(url, { timeoutMs });
}

export async function getCoreInfo(baseUrl, { timeoutMs = 1500 } = {}) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/core/info`;
  return getJson(url, { timeoutMs });
}

export async function getCoreTip(baseUrl, { timeoutMs = 1500 } = {}) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/core/block/tip`;
  return getJson(url, { timeoutMs });
}

export async function getCoreAssets(baseUrl, { timeoutMs = 1500 } = {}) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/core/assets`;
  return getJson(url, { timeoutMs });
}

export async function getProofwalletReadyz(baseUrl, { timeoutMs = 1500 } = {}) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/readyz`;
  return getJson(url, { timeoutMs });
}

export async function aiChat(baseUrl, req, { timeoutMs = 180000 } = {}) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/ai/chat`;
  const payload = {
    profile: req?.profile,
    include_docs: req?.includeDocs,
    wallet_id: req?.walletId,
    messages: req?.messages ?? [],
  };
  // Drop undefined fields to keep payload stable.
  Object.keys(payload).forEach((k) => payload[k] === undefined && delete payload[k]);
  return postJson(url, payload, { timeoutMs });
}

export async function aiDocsSearch(
  baseUrl,
  q,
  { topK = 8, maxChars = 2400, timeoutMs = 1500 } = {}
) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/ai/docs/search?q=${encodeURIComponent(String(q ?? ""))}&top_k=${Number(topK) || 8}&max_chars=${
    Number(maxChars) || 2400
  }`;
  return getJson(url, { timeoutMs });
}

export async function getAiQbitContext(
  baseUrl,
  { maxChars = 2500, limitBlocks = 10, timeoutMs = 1500 } = {}
) {
  const b = normalizeBaseUrl(baseUrl);
  const url = `${b}/ai/qbit/context?max_chars=${Number(maxChars) || 2500}&limit_blocks=${Number(limitBlocks) || 10}`;
  return getJson(url, { timeoutMs });
}

export async function registerProofwalletAddress(
  proofwalletBaseUrl,
  req,
  { timeoutMs = 2500 } = {}
) {
  const b = normalizeBaseUrl(proofwalletBaseUrl);
  const url = `${b}/wallet/address/register`;
  return postJson(url, req, { timeoutMs });
}

export async function registerEvmBridgeAddress(
  nativeExplorerBaseUrl,
  req,
  { timeoutMs = 4000 } = {}
) {
  const b = normalizeBaseUrl(nativeExplorerBaseUrl);
  const url = `${b}/bridge/evm/register`;
  const payload = {
    wallet_id: req?.walletId,
    evm_address: req?.evmAddress,
    assets: req?.assets,
  };
  return postJson(url, payload, { timeoutMs });
}

export async function getSdkNodeInfo(
  nativeExplorerBaseUrl,
  { timeoutMs = 1500 } = {}
) {
  const b = normalizeBaseUrl(nativeExplorerBaseUrl);
  const url = `${b}/sdk/v1/node/info`;
  return getJson(url, { timeoutMs });
}

export async function getSdkIndexStats(
  nativeExplorerBaseUrl,
  { timeoutMs = 1500 } = {}
) {
  const b = normalizeBaseUrl(nativeExplorerBaseUrl);
  const url = `${b}/sdk/v1/index/stats`;
  return getJson(url, { timeoutMs });
}
