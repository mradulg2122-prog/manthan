/**
 * API service — communicates with the FastAPI backend.
 */

import axios from "axios";

// Backend URL — change this if your backend runs on a different port
const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

// =========================================================================
// Token helpers
// =========================================================================
const TOKEN_KEY = "eventflow_token";

export function saveToken(token: string) {
  if (typeof window !== "undefined") localStorage.setItem(TOKEN_KEY, token);
}

export function getToken(): string | null {
  if (typeof window !== "undefined") return localStorage.getItem(TOKEN_KEY);
  return null;
}

export function clearToken() {
  if (typeof window !== "undefined") localStorage.removeItem(TOKEN_KEY);
}

// =========================================================================
// Registration
// =========================================================================
export interface RegisterData {
  name: string;
  email: string;
  phone: string;
  college: string;
  event: string;
}

export interface RegisterResult {
  success: boolean;
  message: string;
  participant_id?: number;
}

export async function registerParticipant(data: RegisterData): Promise<RegisterResult> {
  try {
    const res = await axios.post<RegisterResult>(`${API_BASE}/register`, data);
    return res.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      const detail = error.response.data?.detail;
      let msg = "Registration failed.";
      if (typeof detail === "string") {
        msg = detail;
      } else if (Array.isArray(detail)) {
        msg = detail.map((d: { msg?: string }) => d.msg || "Invalid input").join(", ");
      } else if (typeof detail === "object" && detail?.message) {
        msg = detail.message;
      }
      return { success: false, message: msg };
    }
    return { success: false, message: "Cannot connect to server." };
  }
}

// =========================================================================
// Auth
// =========================================================================
export interface LoginResult {
  success: boolean;
  token?: string;
  user?: { name: string; role: string };
  message?: string;
}

export async function login(email: string, password: string): Promise<LoginResult> {
  try {
    const res = await axios.post(`${API_BASE}/login`, { email, password });
    return res.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      return { success: false, message: error.response.data?.detail || "Login failed." };
    }
    return { success: false, message: "Cannot connect to server." };
  }
}

export interface MeResult {
  name: string;
  email: string;
  role: string;
}

export async function getMe(): Promise<MeResult | null> {
  const token = getToken();
  if (!token) return null;
  try {
    const res = await axios.get(`${API_BASE}/me`, {
      headers: { Authorization: `Bearer ${token}` },
    });
    return res.data;
  } catch {
    return null;
  }
}

// =========================================================================
// Scanner
// =========================================================================
export interface ScanResult {
  success: boolean;
  message?: string;
  name?: string;
  event?: string;
  time?: string;
}

export async function scanQR(registrationId: string): Promise<ScanResult> {
  try {
    const response = await axios.post<ScanResult>(`${API_BASE}/scan`, {
      registration_id: registrationId,
    });
    return response.data;
  } catch (error: unknown) {
    if (axios.isAxiosError(error) && error.response) {
      const detail = error.response.data?.detail;
      return {
        success: false,
        message:
          typeof detail === "object" ? detail.message : detail || "Unknown error",
      };
    }
    return { success: false, message: "Cannot connect to server." };
  }
}

// =========================================================================
// Dashboard (Admin)
// =========================================================================
function authHeaders() {
  return { Authorization: `Bearer ${getToken()}` };
}

export interface DashboardStats {
  total: number;
  present: number;
  absent: number;
  percentage: number;
}

export async function getStats(): Promise<DashboardStats> {
  const res = await axios.get(`${API_BASE}/dashboard/stats`, { headers: authHeaders() });
  return res.data;
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
  search = "", page = 1, sortBy = "id", sortOrder = "desc"
): Promise<ParticipantsResponse> {
  const res = await axios.get(`${API_BASE}/dashboard/participants`, {
    headers: authHeaders(),
    params: { search, page, per_page: 20, sort_by: sortBy, sort_order: sortOrder },
  });
  return res.data;
}

export interface ParticipantDetail {
  registration_id: string;
  name: string;
  email: string;
  phone: string;
  college: string;
  event: string;
  attendance_status: string;
  check_in_time: string;
  qr_sent: boolean;
  email_sent: boolean;
  error?: string;
}

export async function getParticipantDetail(regId: string): Promise<ParticipantDetail> {
  const res = await axios.get(`${API_BASE}/dashboard/participant/${regId}`, { headers: authHeaders() });
  return res.data;
}

export async function updateAttendance(regId: string, action: "present" | "absent") {
  const res = await axios.patch(
    `${API_BASE}/dashboard/participant/${regId}/attendance`,
    null,
    { headers: authHeaders(), params: { action } },
  );
  return res.data;
}

export interface ActivityItem {
  name: string;
  registration_id: string;
  time: string;
  status: string;
}

export async function getActivity(): Promise<ActivityItem[]> {
  const res = await axios.get(`${API_BASE}/dashboard/activity`, { headers: authHeaders() });
  return res.data;
}

export function getExportUrl(): string {
  return `${API_BASE}/dashboard/export`;
}

// =========================================================================
// Health
// =========================================================================
export interface HealthResult {
  status: string;
  database: string;
  watcher: string;
  email: string;
}

export async function getHealth(): Promise<HealthResult | null> {
  try {
    const res = await axios.get(`${API_BASE}/health`);
    return res.data;
  } catch {
    return null;
  }
}
