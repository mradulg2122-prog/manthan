/**
 * Centralized API client for EventFlow AI.
 * Connects the Lovable frontend to the existing FastAPI backend.
 *
 * Every function maps to a verified backend endpoint.
 * Uses native fetch — no extra dependencies needed.
 */

// ---------------------------------------------------------------------------
// Base URL — reads from Vite env, fallback to localhost
// ---------------------------------------------------------------------------
const API_BASE = import.meta.env.VITE_API_URL || "http://localhost:8000";

// ---------------------------------------------------------------------------
// Token helpers (localStorage)
// ---------------------------------------------------------------------------
const TOKEN_KEY = "eventflow_token";

export function saveToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

// ---------------------------------------------------------------------------
// Generic fetch wrapper — auto-attaches JWT, handles 401
// ---------------------------------------------------------------------------
async function apiFetch<T>(
  path: string,
  options: RequestInit = {},
): Promise<T> {
  const token = getToken();
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };
  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  const res = await fetch(`${API_BASE}${path}`, { ...options, headers });

  // 401 → clear token, redirect to home
  if (res.status === 401) {
    clearToken();
    window.location.href = "/";
    throw new Error("Unauthorized");
  }

  if (!res.ok) {
    const body = await res.json().catch(() => null);
    const detail = body?.detail;
    let msg = "Request failed.";
    if (typeof detail === "string") {
      msg = detail;
    } else if (typeof detail === "object" && detail?.message) {
      msg = detail.message;
    } else if (Array.isArray(detail)) {
      msg = detail.map((d: { msg?: string }) => d.msg || "Invalid input").join(", ");
    }
    throw new Error(msg);
  }

  return res.json();
}

// ---------------------------------------------------------------------------
// Registration — POST /register
// ---------------------------------------------------------------------------
export interface RegisterData {
  name: string;
  email: string;
  phone: string;
  college: string;
  event: string;
}

export interface RegisterResult {
  success?: boolean;
  message?: string;
  participant_id?: number;
  id?: number;
  detail?: any;
}

export async function registerParticipant(data: RegisterData): Promise<RegisterResult> {
  try {
    return await apiFetch<RegisterResult>("/register", {
      method: "POST",
      body: JSON.stringify(data),
    });
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : "Cannot connect to server.";
    return { success: false, message: msg };
  }
}

// ---------------------------------------------------------------------------
// Auth — POST /login, GET /me
// ---------------------------------------------------------------------------
export interface LoginResult {
  success: boolean;
  token?: string;
  user?: { name: string; role: string };
  message?: string;
}

export async function login(email: string, password: string): Promise<LoginResult> {
  try {
    return await apiFetch<LoginResult>("/login", {
      method: "POST",
      body: JSON.stringify({ email, password }),
    });
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : "Cannot connect to server.";
    return { success: false, message: msg };
  }
}

export interface MeResult {
  name: string;
  email: string;
  role: string;
}

export async function getMe(): Promise<MeResult | null> {
  try {
    return await apiFetch<MeResult>("/me");
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Scanner — POST /scan
// ---------------------------------------------------------------------------
export interface ScanResult {
  success: boolean;
  message?: string;
  name?: string;
  event?: string;
  time?: string;
}

export async function scanQR(registrationId: string): Promise<ScanResult> {
  try {
    return await apiFetch<ScanResult>("/scan", {
      method: "POST",
      body: JSON.stringify({ registration_id: registrationId }),
    });
  } catch (error: unknown) {
    const msg = error instanceof Error ? error.message : "Cannot connect to server.";
    return { success: false, message: msg };
  }
}

// ---------------------------------------------------------------------------
// Dashboard — Admin APIs
// ---------------------------------------------------------------------------
export interface DashboardStats {
  total: number;
  present: number;
  absent: number;
  percentage: number;
}

export async function getStats(): Promise<DashboardStats> {
  return apiFetch<DashboardStats>("/dashboard/stats");
}

export interface ParticipantRow {
  id: number;
  registration_id: string;
  name: string;
  email: string;
  phone: string;
  attendance_status: string;
  check_in_time: string;
}

export interface ParticipantsResponse {
  participants: ParticipantRow[];
  total: number;
  page: number;
  per_page: number;
  total_pages: number;
}

export async function getParticipants(
  search = "",
  page = 1,
): Promise<ParticipantsResponse> {
  const params = new URLSearchParams({
    search,
    page: String(page),
    per_page: "20",
    sort_by: "id",
    sort_order: "desc",
  });
  return apiFetch<ParticipantsResponse>(`/dashboard/participants?${params}`);
}

export interface ActivityItem {
  name: string;
  registration_id: string;
  time: string;
  status: string;
}

export async function getActivity(): Promise<ActivityItem[]> {
  return apiFetch<ActivityItem[]>("/dashboard/activity?limit=20");
}

// ---------------------------------------------------------------------------
// Export — builds URL with token for browser download
// ---------------------------------------------------------------------------
export function getExportUrl(): string {
  const token = getToken();
  return `${API_BASE}/dashboard/export?token=${token}`;
}

// ---------------------------------------------------------------------------
// Health — GET /health
// ---------------------------------------------------------------------------
export interface HealthResult {
  status: string;
  database: any;
  watcher: string;
  email_smtp: any;
}

export async function getHealth(): Promise<HealthResult | null> {
  try {
    return await apiFetch<HealthResult>("/health");
  } catch {
    return null;
  }
}

// ---------------------------------------------------------------------------
// Reset Participants — POST /dashboard/reset (Admin Only)
// ---------------------------------------------------------------------------
export async function resetParticipants(): Promise<{ success: boolean; message: string; deleted_count: number }> {
  return apiFetch<{ success: boolean; message: string; deleted_count: number }>("/dashboard/reset", {
    method: "POST",
  });
}

