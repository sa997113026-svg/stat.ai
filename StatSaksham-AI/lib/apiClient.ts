// Thin client for the StatSaksham AI FastAPI backend (/api/v1).
// Handles the {data, meta, request_id} response envelope, demo auto-login,
// and JWT bearer attachment. Used by lib/services.ts.

export type Role = 'learner' | 'trainer' | 'admin';

export const API_MODE: 'mock' | 'live' =
  (process.env.NEXT_PUBLIC_API_MODE as 'mock' | 'live') || 'mock';

const BASE_URL =
  process.env.NEXT_PUBLIC_API_BASE_URL || 'http://localhost:8000/api/v1';

export function isLiveMode() {
  return API_MODE === 'live';
}

// Credentials match the demo accounts seeded by backend/app/repositories/in_memory.py
// and documented in backend/docs/API_CONTRACT.md — not secrets, just seed fixtures.
const DEMO_CREDENTIALS: Record<Role, { email: string; password: string }> = {
  learner: { email: 'ananya.sharma@mospi.gov.in', password: 'StatSaksham@2026' },
  trainer: { email: 'trainer@nssta.gov.in', password: 'Trainer@2026' },
  admin: { email: 'admin@mospi.gov.in', password: 'Admin@2026' },
};

type TokenEntry = { token: string; expiresAt: number };
const tokenCache = new Map<Role, TokenEntry>();

async function rawRequest<T>(path: string, options: RequestInit = {}): Promise<T> {
  const res = await fetch(`${BASE_URL}${path}`, {
    ...options,
    headers: { 'Content-Type': 'application/json', ...(options.headers || {}) },
  });
  const json = await res.json().catch(() => null);
  if (!res.ok) {
    const message = json?.error?.message || `Request to ${path} failed with ${res.status}`;
    throw new Error(message);
  }
  return (json as { data: T }).data;
}

async function login(role: Role): Promise<string> {
  const cached = tokenCache.get(role);
  if (cached && cached.expiresAt > Date.now()) return cached.token;

  const creds = DEMO_CREDENTIALS[role];
  const data = await rawRequest<{ access_token: string }>('/auth/login', {
    method: 'POST',
    body: JSON.stringify(creds),
  });
  // Backend tokens expire in ACCESS_TOKEN_EXPIRE_MINUTES (default 30); refresh a little early.
  tokenCache.set(role, { token: data.access_token, expiresAt: Date.now() + 25 * 60 * 1000 });
  return data.access_token;
}

export async function apiGet<T>(path: string, role: Role = 'learner'): Promise<T> {
  const token = await login(role);
  return rawRequest<T>(path, { headers: { Authorization: `Bearer ${token}` } });
}

export async function apiPost<T>(path: string, body: unknown, role: Role = 'learner'): Promise<T> {
  const token = await login(role);
  return rawRequest<T>(path, {
    method: 'POST',
    headers: { Authorization: `Bearer ${token}` },
    body: JSON.stringify(body ?? {}),
  });
}
