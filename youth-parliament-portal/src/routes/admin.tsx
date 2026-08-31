import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState, useEffect, useCallback } from "react";
import { SiteShell } from "@/components/site/SiteShell";
import {
  Users,
  UserCheck,
  Clock3,
  TrendingUp,
  Search,
  Download,
  LogOut,
  Sparkles,
  ShieldCheck,
  RefreshCw,
} from "lucide-react";
import {
  getStats,
  getParticipants,
  getActivity,
  getExportUrl,
  getMe,
  clearToken,
  type DashboardStats,
  type ParticipantRow,
  type ActivityItem,
} from "@/lib/api";

export const Route = createFileRoute("/admin")({
  head: () => ({
    meta: [
      { title: "Admin Dashboard — MANTHAN | PRARAMBH 2K26" },
      { name: "description", content: "Administrator dashboard for MANTHAN event management at GLA University." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: AdminDashboard,
});

function AdminDashboard() {
  const navigate = useNavigate();

  // Auth guard
  const [authed, setAuthed] = useState(false);
  const [adminName, setAdminName] = useState("Administrator");

  useEffect(() => {
    getMe().then((user) => {
      if (!user || user.role !== "ADMIN") {
        clearToken();
        navigate({ to: "/admin-login" });
      } else {
        setAdminName(user.name || "Administrator");
        setAuthed(true);
      }
    });
  }, [navigate]);

  // Data state
  const [stats, setStats] = useState<DashboardStats>({ total: 0, present: 0, absent: 0, percentage: 0 });
  const [participants, setParticipants] = useState<ParticipantRow[]>([]);
  const [activity, setActivity] = useState<ActivityItem[]>([]);
  const [search, setSearch] = useState("");
  const [page, setPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [refreshing, setRefreshing] = useState(false);

  // Fetch functions
  const fetchStats = useCallback(async () => {
    try {
      setStats(await getStats());
    } catch {
      /* ignore */
    }
  }, []);

  const fetchParticipants = useCallback(async () => {
    try {
      const res = await getParticipants(search, page);
      setParticipants(res.participants);
      setTotalPages(res.total_pages);
    } catch {
      /* ignore */
    }
  }, [search, page]);

  const fetchActivity = useCallback(async () => {
    try {
      setActivity(await getActivity());
    } catch {
      /* ignore */
    }
  }, []);

  const handleManualRefresh = async () => {
    setRefreshing(true);
    await Promise.all([fetchStats(), fetchParticipants(), fetchActivity()]);
    setRefreshing(false);
  };

  // Initial load + auto-refresh
  useEffect(() => {
    if (!authed) return;
    fetchStats();
    fetchParticipants();
    fetchActivity();

    const statsInterval = setInterval(fetchStats, 15000);
    const activityInterval = setInterval(fetchActivity, 10000);

    return () => {
      clearInterval(statsInterval);
      clearInterval(activityInterval);
    };
  }, [authed, fetchStats, fetchParticipants, fetchActivity]);

  // Refetch participants when search or page changes
  useEffect(() => {
    if (authed) fetchParticipants();
  }, [search, page, authed, fetchParticipants]);

  const handleExport = () => {
    window.open(getExportUrl(), "_blank");
  };

  const handleLogout = () => {
    clearToken();
    navigate({ to: "/admin-login" });
  };

  if (!authed) {
    return (
      <SiteShell hideFooter>
        <div className="py-24 text-center bg-[#F7F4EC] min-h-[calc(100vh-5rem)]">
          <div className="mx-auto h-10 w-10 rounded-full border-3 border-[#C49A45] border-t-transparent animate-spin" />
          <p className="mt-4 text-xs font-bold uppercase tracking-wider text-[#627D98]">Verifying Admin Privileges…</p>
        </div>
      </SiteShell>
    );
  }

  const statCards = [
    {
      icon: Users,
      label: "Total Registered",
      value: String(stats.total),
      trend: "Freshers enrolled",
      highlightColor: "bg-[#102A43] text-white",
    },
    {
      icon: UserCheck,
      label: "Checked-In",
      value: String(stats.present),
      trend: `${stats.percentage}% of total`,
      highlightColor: "bg-emerald-600 text-white",
    },
    {
      icon: Clock3,
      label: "Pending Entry",
      value: String(stats.absent),
      trend: "Awaiting check-in",
      highlightColor: "bg-[#C49A45] text-white",
    },
    {
      icon: TrendingUp,
      label: "Turnout Ratio",
      value: `${stats.percentage}%`,
      trend: `${stats.present} / ${stats.total} present`,
      highlightColor: "bg-[#102A43] text-white",
    },
  ];

  return (
    <SiteShell hideFooter>
      <section className="py-10 sm:py-12 bg-[#F7F4EC] min-h-[calc(100vh-5rem)]">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-10">
          {/* Header */}
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <div className="inline-flex items-center gap-2 rounded-full border border-[#C49A45]/40 bg-white px-3 py-0.5 text-[11px] font-bold tracking-wider uppercase text-[#102A43]">
                <span className="h-1.5 w-1.5 rounded-full bg-[#C49A45]" />
                PRARAMBH 2K26 · MANTHAN
              </div>
              <h1 className="mt-2 font-serif text-3xl sm:text-4xl font-extrabold text-[#102A43]">
                Admin Command Center
              </h1>
              <p className="mt-1 text-xs sm:text-sm text-[#627D98]">
                Real-time participant oversight, live scanner feed & export
              </p>
            </div>
            <div className="flex flex-wrap items-center gap-2.5">
              <button
                onClick={handleManualRefresh}
                disabled={refreshing}
                title="Refresh data"
                className="btn-outline !py-2 !px-3 text-xs font-bold"
              >
                <RefreshCw className={`h-3.5 w-3.5 ${refreshing ? "animate-spin" : ""}`} />
              </button>
              <button onClick={handleExport} className="btn-primary !py-2.5 !px-4 text-xs sm:text-sm font-bold shadow-md">
                <Download className="h-4 w-4 text-[#C49A45]" /> Export Attendance CSV
              </button>
              <button
                onClick={handleLogout}
                className="btn-outline !py-2.5 !px-3.5 text-xs font-bold text-[#9E2A2B] hover:border-[#9E2A2B]"
                title="Sign out"
              >
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          </div>

          <div className="gold-divider mt-6" />

          {/* Stats Grid */}
          <div className="mt-8 grid gap-4 sm:grid-cols-2 lg:grid-cols-4">
            {statCards.map((s) => (
              <div
                key={s.label}
                className="gov-card p-6 bg-white border border-[#DDD7C9] rounded-xl hover:shadow-md transition-all"
              >
                <div className="flex items-center justify-between">
                  <div className="text-[11px] font-bold tracking-[0.18em] uppercase text-[#627D98]">{s.label}</div>
                  <div className={`flex h-9 w-9 items-center justify-center rounded-lg shadow-xs ${s.highlightColor}`}>
                    <s.icon className="h-4 w-4" />
                  </div>
                </div>
                <div className="mt-4 font-serif text-3xl sm:text-4xl font-extrabold text-[#102A43]">{s.value}</div>
                <div className="mt-1 text-xs text-[#627D98] font-medium">{s.trend}</div>
              </div>
            ))}
          </div>

          <div className="mt-8 grid gap-6 lg:grid-cols-3 items-start">
            {/* Participant Table (2 cols) */}
            <div className="gov-card lg:col-span-2 overflow-hidden bg-white border border-[#DDD7C9] rounded-2xl shadow-md">
              <div className="p-5 sm:p-6 flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4 border-b border-[#DDD7C9]">
                <div>
                  <div className="text-[11px] font-bold tracking-[0.18em] uppercase text-[#C49A45]">Registry</div>
                  <h2 className="mt-0.5 font-serif text-xl font-bold text-[#102A43]">Participant List</h2>
                </div>
                <div className="relative w-full sm:w-72">
                  <Search className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-[#627D98]" />
                  <input
                    className="w-full bg-[#FAF8F3] border border-[#DDD7C9] rounded-lg pl-9 pr-3 py-2 text-xs sm:text-sm text-[#102A43] focus:outline-none focus:border-[#C49A45] focus:bg-white transition"
                    placeholder="Search by name, ID, phone..."
                    value={search}
                    onChange={(e) => {
                      setSearch(e.target.value);
                      setPage(1);
                    }}
                  />
                </div>
              </div>

              <div className="overflow-x-auto">
                <table className="w-full text-left text-xs sm:text-sm">
                  <thead>
                    <tr className="bg-[#FAF8F3] border-b border-[#DDD7C9] text-[11px] font-bold tracking-[0.16em] uppercase text-[#627D98]">
                      <th className="px-5 py-3.5">Registration ID</th>
                      <th className="px-5 py-3.5">Participant / Affiliation</th>
                      <th className="px-5 py-3.5">Contact</th>
                      <th className="px-5 py-3.5">Status</th>
                    </tr>
                  </thead>
                  <tbody className="divide-y divide-[#DDD7C9]">
                    {participants.length === 0 ? (
                      <tr>
                        <td colSpan={4} className="px-5 py-10 text-center text-[#627D98] text-xs sm:text-sm">
                          No registered participants found.
                        </td>
                      </tr>
                    ) : (
                      participants.map((p) => (
                        <tr key={p.id} className="hover:bg-[#FAF8F3]/60 transition-colors">
                          <td className="px-5 py-3.5 font-mono text-xs font-semibold text-[#102A43]">
                            {p.registration_id || "—"}
                          </td>
                          <td className="px-5 py-3.5">
                            <div className="font-bold text-[#102A43]">{p.name}</div>
                            <div className="text-xs text-[#627D98]">{p.email}</div>
                          </td>
                          <td className="px-5 py-3.5 text-[#102A43]/80 font-mono text-xs">
                            {p.phone || "—"}
                          </td>
                          <td className="px-5 py-3.5">
                            {p.attendance_status === "Present" ? (
                              <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-1 text-xs font-semibold">
                                <span className="h-1.5 w-1.5 rounded-full bg-emerald-600" /> Present
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1.5 rounded-full bg-[#FAF2DC] text-[#8A631E] border border-[#ECD8A5] px-2.5 py-1 text-xs font-semibold">
                                <span className="h-1.5 w-1.5 rounded-full bg-[#C49A45]" /> Absent
                              </span>
                            )}
                          </td>
                        </tr>
                      ))
                    )}
                  </tbody>
                </table>
              </div>

              {/* Pagination */}
              {totalPages > 1 && (
                <div className="p-4 flex items-center justify-between border-t border-[#DDD7C9] bg-[#FAF8F3]">
                  <span className="text-xs text-[#627D98] font-medium">
                    Page {page} of {totalPages}
                  </span>
                  <div className="flex items-center gap-2">
                    <button
                      disabled={page <= 1}
                      onClick={() => setPage(page - 1)}
                      className="btn-outline !py-1.5 !px-3 !text-xs font-semibold disabled:opacity-40"
                    >
                      Previous
                    </button>
                    <button
                      disabled={page >= totalPages}
                      onClick={() => setPage(page + 1)}
                      className="btn-outline !py-1.5 !px-3 !text-xs font-semibold disabled:opacity-40"
                    >
                      Next
                    </button>
                  </div>
                </div>
              )}
            </div>

            {/* Live Activity Feed (1 col) */}
            <div className="gov-card p-5 sm:p-6 bg-white border border-[#DDD7C9] rounded-2xl shadow-md">
              <div className="flex items-center justify-between">
                <div>
                  <div className="text-[11px] font-bold tracking-[0.18em] uppercase text-[#C49A45]">Live Feed</div>
                  <h2 className="mt-0.5 font-serif text-xl font-bold text-[#102A43]">Check-In Activity</h2>
                </div>
                <div className="flex h-2.5 w-2.5 relative">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75" />
                  <span className="relative inline-flex rounded-full h-2.5 w-2.5 bg-emerald-500" />
                </div>
              </div>
              <div className="gold-divider mt-4" />

              {activity.length === 0 ? (
                <div className="py-12 text-center text-xs text-[#627D98]">
                  No check-ins recorded yet. Activity will appear live when volunteers scan QR passes.
                </div>
              ) : (
                <ul className="mt-4 space-y-3">
                  {activity.map((a, i) => (
                    <li key={i} className="flex gap-3 text-xs">
                      <div className="pt-0.5 font-mono text-[#627D98] w-14 shrink-0 font-medium">{a.time}</div>
                      <div className="flex-1 border-l-2 border-[#ECD8A5] pl-3 pb-1">
                        <div className="font-bold text-[#102A43]">{a.name}</div>
                        <div className="text-[11px] text-[#627D98] font-mono">{a.registration_id}</div>
                      </div>
                    </li>
                  ))}
                </ul>
              )}
            </div>
          </div>
        </div>
      </section>
    </SiteShell>
  );
}
