export type JsonValue =
  | null
  | boolean
  | number
  | string
  | JsonValue[]
  | { [key: string]: JsonValue };

export type JsonResponse<T = JsonValue> = {
  ok: boolean;
  status: number;
  data: T | null;
};

export declare function resolveCoreBaseUrl(env?: Record<string, string | undefined>): string;
export declare function resolveProofwalletBaseUrl(env?: Record<string, string | undefined>): string;
export declare function resolveNativeExplorerBaseUrl(env?: Record<string, string | undefined>): string;

export declare function getJson<T = JsonValue>(
  url: string,
  opts?: { timeoutMs?: number; headers?: Record<string, string> }
): Promise<JsonResponse<T>>;

export declare function postJson<T = JsonValue>(
  url: string,
  payload?: JsonValue,
  opts?: { timeoutMs?: number; headers?: Record<string, string> }
): Promise<JsonResponse<T>>;

export type VnovaPricesPayload = Record<string, JsonValue>;

export declare function getVnovaPrices(
  baseUrl: string,
  opts?: { maxAgeSec?: number; timeoutMs?: number }
): Promise<JsonResponse<VnovaPricesPayload>>;

export declare function getVnovaHealth(
  baseUrl: string,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function getVnovaOverview(
  baseUrl: string,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function getApiStatus(
  baseUrl: string,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function getCoreInfo(
  baseUrl: string,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function getCoreTip(
  baseUrl: string,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function getCoreAssets(
  baseUrl: string,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function getProofwalletReadyz(
  baseUrl: string,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export type AiChatRequest = {
  profile?: string;
  includeDocs?: boolean;
  walletId?: string;
  messages: { role: string; content: string }[];
};

export declare function aiChat(
  baseUrl: string,
  req: AiChatRequest,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function aiDocsSearch(
  baseUrl: string,
  q: string,
  opts?: { topK?: number; maxChars?: number; timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function getAiQbitContext(
  baseUrl: string,
  opts?: { maxChars?: number; limitBlocks?: number; timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export type RegisterProofwalletAddressRequest = {
  wallet: string;
  asset: string;
  address: string;
};

export declare function registerProofwalletAddress(
  proofwalletBaseUrl: string,
  req: RegisterProofwalletAddressRequest,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export type RegisterEvmBridgeAddressRequest = {
  walletId: string;
  evmAddress: string;
  assets?: string[];
};

export declare function registerEvmBridgeAddress(
  nativeExplorerBaseUrl: string,
  req: RegisterEvmBridgeAddressRequest,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function getSdkNodeInfo(
  nativeExplorerBaseUrl: string,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;

export declare function getSdkIndexStats(
  nativeExplorerBaseUrl: string,
  opts?: { timeoutMs?: number }
): Promise<JsonResponse<Record<string, JsonValue>>>;
