"use client";

/**
 * /admin — Youth Parliament 6.0 Dashboard
 * Admin-only. Auto-refreshing stats, participant table, activity feed, export.
 */

import { useEffect, useState, useCallback, useRef } from "react";
import { useRouter } from "next/navigation";
import {
  getMe, clearToken, getToken,
  getStats, DashboardStats,
  getParticipants, ParticipantsResponse,
  getParticipantDetail, ParticipantDetail,
  getActivity, ActivityItem,
  getExportUrl, getHealth, HealthResult,
} from "@/app/services/api";

import DashboardCards from "@/app/components/DashboardCards";
import SearchBar from "@/app/components/SearchBar";
import ParticipantTable from "@/app/components/ParticipantTable";
import ParticipantDetails from "@/app/components/ParticipantDetails";
import ActivityFeed from "@/app/components/ActivityFeed";
import SystemStatus from "@/app/components/SystemStatus";

export default function AdminPage() {
  const router = useRouter();
  const [checking, setChecking] = useState(true);
  const [userName, setUserName] = useState("");

  // Dashboard data
  const [stats, setStats] = useState<DashboardStats | null>(null);
  const [tableData, setTableData] = useState<ParticipantsResponse | null>(null);
  const [activity, setActivity] = useState<ActivityItem[]>([]);
  const [health, setHealth] = useState<HealthResult | null>(null);

  // Table controls
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [sortBy, setSortBy] = useState("id");
  const [sortOrder, setSortOrder] = useState("desc");

  // Detail panel
  const [selectedDetail, setSelectedDetail] = useState<ParticipantDetail | null>(null);

  // Debounce timer for search
  const searchTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  // ── Auth guard ──
  useEffect(() => {
    getMe().then((user) => {
      if (!user || user.role !== "ADMIN") {
        clearToken();
        router.replace("/login");
      } else {
        setUserName(user.name);
        setChecking(false);
      }
    });
  }, [router]);

  // ── Load stats + health ──
  const loadStats = useCallback(async () => {
    try { setStats(await getStats()); } catch { /* ignore */ }
    try { setHealth(await getHealth()); } catch { /* ignore */ }
  }, []);

  // ── Load participants ──
  const loadParticipants = useCallback(async () => {
    try { setTableData(await getParticipants(search, page, sortBy, sortOrder)); } catch { /* ignore */ }
  }, [search, page, sortBy, sortOrder]);

  // ── Load activity ──
  const loadActivity = useCallback(async () => {
    try { setActivity(await getActivity()); } catch { /* ignore */ }
  }, []);

  // ── Initial load + auto-refresh ──
  useEffect(() => {
    if (checking) return;
    loadStats();
    loadParticipants();
    loadActivity();

    const statsInterval = setInterval(loadStats, 15000);
    const activityInterval = setInterval(loadActivity, 10000);

    return () => {
      clearInterval(statsInterval);
      clearInterval(activityInterval);
    };
  }, [checking, loadStats, loadParticipants, loadActivity]);

  // ── Debounced search ──
  useEffect(() => {
    if (checking) return;
    if (searchTimer.current) clearTimeout(searchTimer.current);
    searchTimer.current = setTimeout(() => {
      setPage(1);
      loadParticipants();
    }, 400);
    return () => { if (searchTimer.current) clearTimeout(searchTimer.current); };
  }, [search, checking, loadParticipants]);

  // ── Sort handler ──
  const handleSort = (col: string) => {
    if (sortBy === col) {
      setSortOrder(sortOrder === "asc" ? "desc" : "asc");
    } else {
      setSortBy(col);
      setSortOrder("asc");
    }
  };
  useEffect(() => { if (!checking) loadParticipants(); }, [page, sortBy, sortOrder, checking, loadParticipants]);

  // ── Row click → detail ──
  const handleRowClick = async (regId: string) => {
    try {
      const detail = await getParticipantDetail(regId);
      if (!detail.error) setSelectedDetail(detail);
    } catch { /* ignore */ }
  };

  // ── After attendance update ──
  const handleDetailUpdated = () => {
    setSelectedDetail(null);
    loadStats();
    loadParticipants();
    loadActivity();
  };

  // ── Export ──
  const handleExport = () => {
    const token = getToken();
    window.open(`${getExportUrl()}?token=${token}`, "_blank");
  };

  // ── Logout ──
  const handleLogout = () => {
    clearToken();
    router.push("/login");
  };

  if (checking) {
    return (
      <main className="min-h-screen bg-gray-950 flex items-center justify-center text-gray-400">
        Checking access…
      </main>
    );
  }

  return (
    <main className="min-h-screen bg-gradient-to-b from-gray-950 via-gray-900 to-gray-950 text-white">
      <div className="max-w-7xl mx-auto px-4 py-6 space-y-6">

        {/* Header */}
        <div className="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold tracking-tight">
              Youth Parliament <span className="text-indigo-400">6.0</span> Dashboard
            </h1>
            <p className="text-gray-400 text-sm">Welcome, {userName}</p>
          </div>
          <div className="flex gap-3">
            <button
              onClick={handleExport}
              className="px-4 py-2 bg-indigo-600 hover:bg-indigo-500 text-white text-sm font-medium rounded-xl transition-colors"
            >
              Export Attendance
            </button>
            <button
              onClick={handleLogout}
              className="px-4 py-2 bg-gray-700/60 hover:bg-gray-600 text-gray-300 text-sm font-medium rounded-xl transition-colors"
            >
              Logout
            </button>
          </div>
        </div>

        {/* Stats Cards */}
        <DashboardCards stats={stats} />

        {/* Search + Table */}
        <div className="space-y-4">
          <SearchBar value={search} onChange={setSearch} />
          <ParticipantTable
            rows={tableData?.participants || []}
            page={page}
            totalPages={tableData?.total_pages || 1}
            onPageChange={setPage}
            onRowClick={handleRowClick}
            sortBy={sortBy}
            sortOrder={sortOrder}
            onSort={handleSort}
          />
        </div>

        {/* Activity + System Status row */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
          <div className="bg-gray-800/30 border border-gray-700/40 rounded-xl p-5">
            <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3">
              Recent Activity
            </h2>
            <ActivityFeed items={activity} />
          </div>
          <SystemStatus health={health} />
        </div>
      </div>

      {/* Detail Modal */}
      {selectedDetail && (
        <ParticipantDetails
          detail={selectedDetail}
          onClose={() => setSelectedDetail(null)}
          onUpdated={handleDetailUpdated}
        />
      )}
    </main>
  );
}
