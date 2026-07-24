import { createFileRoute, useNavigate } from "@tanstack/react-router";
import { useState, useEffect, useCallback } from "react";
import { SiteShell } from "@/components/site/SiteShell";
import { Users, UserCheck, Clock3, TrendingUp, Search, Download, LogOut } from "lucide-react";
import {
  getStats, getParticipants, getActivity, getExportUrl, getMe, clearToken,
  type DashboardStats, type ParticipantRow, type ActivityItem,
} from "@/lib/api";

export const Route = createFileRoute("/admin")({
  head: () => ({
    meta: [
      { title: "Admin Dashboard — Youth Parliament 6.0" },
      { name: "description", content: "Administrator dashboard for Youth Parliament 6.0 event management." },
      { name: "robots", content: "noindex" },
    ],
  }),
  component: AdminDashboard,
});

function AdminDashboard() {
  const navigate = useNavigate();

  // Auth guard
  const [authed, setAuthed] = useState(false);
  useEffect(() => {
    getMe().then((user) => {
      if (!user || user.role !== "ADMIN") {
        clearToken();
        navigate({ to: "/admin-login" });
      } else {
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

  // Fetch functions
  const fetchStats = useCallback(async () => {
    try { setStats(await getStats()); } catch { /* ignore */ }
  }, []);

  const fetchParticipants = useCallback(async () => {
    try {
      const res = await getParticipants(search, page);
      setParticipants(res.participants);
      setTotalPages(res.total_pages);
    } catch { /* ignore */ }
  }, [search, page]);

  const fetchActivity = useCallback(async () => {
    try { setActivity(await getActivity()); } catch { /* ignore */ }
  }, []);

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
        <div className="py-20 text-center text-sm text-muted-foreground">Checking access…</div>
      </SiteShell>
    );
  }

  const statCards = [
    { icon: Users, label: "Total Registrations", value: String(stats.total), trend: `${stats.present + stats.absent} total` },
    { icon: UserCheck, label: "Checked-In", value: String(stats.present), trend: `${stats.percentage}% attendance` },
    { icon: Clock3, label: "Pending", value: String(stats.absent), trend: "Awaiting arrival" },
    { icon: TrendingUp, label: "Attendance %", value: `${stats.percentage}%`, trend: `${stats.present} of ${stats.total}` },
  ];

  return (
    <SiteShell hideFooter>
      <section className="py-12">
        <div className="mx-auto max-w-7xl px-6 lg:px-10">
          {/* Header */}
          <div className="flex flex-wrap items-end justify-between gap-4">
            <div>
              <div className="eyebrow">Administration</div>
              <h1 className="mt-2 font-serif text-4xl text-foreground">Event Dashboard</h1>
              <p className="mt-2 text-sm text-muted-foreground">Youth Parliament 6.0 · Real-time overview</p>
            </div>
            <div className="flex gap-2">
              <button onClick={handleExport} className="btn-primary">
                <Download className="h-4 w-4" /> Export Attendance
              </button>
              <button onClick={handleLogout} className="btn-outline !py-2 !px-4">
                <LogOut className="h-4 w-4" />
              </button>
            </div>
          </div>
          <div className="gold-divider mt-6" />

          {/* Stats */}
          <div className="mt-8 grid gap-5 sm:grid-cols-2 lg:grid-cols-4">
            {statCards.map((s) => (
              <div key={s.label} className="gov-card p-6">
                <div className="flex items-center justify-between">
                  <div className="text-[11px] font-semibold tracking-[0.22em] uppercase text-muted-foreground">{s.label}</div>
                  <div className="flex h-9 w-9 items-center justify-center rounded-md bg-[color:var(--crimson)] text-white">
                    <s.icon className="h-4 w-4" />
                  </div>
                </div>
                <div className="mt-5 font-serif text-3xl text-foreground">{s.value}</div>
                <div className="mt-1 text-xs text-muted-foreground">{s.trend}</div>
              </div>
            ))}
          </div>

          <div className="mt-10 grid gap-6 lg:grid-cols-3">
            {/* Table */}
            <div className="gov-card lg:col-span-2 overflow-hidden">
              <div className="p-6 flex items-center justify-between gap-4 border-b border-border">
                <div>
                  <div className="text-[11px] font-semibold tracking-[0.22em] uppercase text-muted-foreground">Participants</div>
                  <h2 className="mt-1 font-serif text-xl text-foreground">Delegate Registry</h2>
                </div>
                <div className="relative w-full max-w-xs">
                  <Search className="pointer-events-none absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-muted-foreground" />
                  <input
                    className="w-full bg-white border border-border rounded-md pl-9 pr-3 py-2 text-sm focus:outline-none focus:border-[color:var(--gold)] focus:ring-2 focus:ring-[color:var(--gold)]/25"
                    placeholder="Search delegates..."
                    value={search}
                    onChange={(e) => { setSearch(e.target.value); setPage(1); }}
                  />
                </div>
              </div>
              <div className="gold-divider" />
              <div className="overflow-x-auto">
                <table className="w-full text-sm">
                  <thead>
                    <tr className="bg-[color:var(--surface)] text-left text-[11px] font-semibold tracking-[0.18em] uppercase text-muted-foreground">
                      <th className="px-6 py-3">ID</th>
                      <th className="px-6 py-3">Name</th>
                      <th className="px-6 py-3">Phone</th>
                      <th className="px-6 py-3">Status</th>
                    </tr>
                  </thead>
                  <tbody>
                    {participants.length === 0 ? (
                      <tr><td colSpan={4} className="px-6 py-8 text-center text-muted-foreground">No participants found.</td></tr>
                    ) : (
                      participants.map((p, i) => (
                        <tr key={p.id} className={i !== participants.length - 1 ? "border-b border-border" : ""}>
                          <td className="px-6 py-4 font-mono text-xs text-muted-foreground">{p.registration_id || "—"}</td>
                          <td className="px-6 py-4">
                            <div className="font-medium text-foreground">{p.name}</div>
                            <div className="text-xs text-muted-foreground">{p.email}</div>
                          </td>
                          <td className="px-6 py-4 text-foreground/80">{p.phone || "—"}</td>
                          <td className="px-6 py-4">
                            {p.attendance_status === "Present" ? (
                              <span className="inline-flex items-center gap-1.5 rounded-full bg-emerald-50 text-emerald-700 border border-emerald-200 px-2.5 py-1 text-xs font-medium">
                                <span className="h-1.5 w-1.5 rounded-full bg-emerald-600" /> Present
                              </span>
                            ) : (
                              <span className="inline-flex items-center gap-1.5 rounded-full bg-[#fbf5e6] text-[color:var(--maroon)] border border-[color:var(--gold)]/50 px-2.5 py-1 text-xs font-medium">
                                <span className="h-1.5 w-1.5 rounded-full bg-[color:var(--gold)]" /> Absent
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
                <div className="p-4 flex items-center justify-center gap-2 border-t border-border">
                  <button
                    disabled={page <= 1}
                    onClick={() => setPage(page - 1)}
                    className="btn-outline !py-1.5 !px-3 !text-xs disabled:opacity-40"
                  >
                    Previous
                  </button>
                  <span className="text-xs text-muted-foreground">Page {page} of {totalPages}</span>
                  <button
                    disabled={page >= totalPages}
                    onClick={() => setPage(page + 1)}
                    className="btn-outline !py-1.5 !px-3 !text-xs disabled:opacity-40"
                  >
                    Next
                  </button>
                </div>
              )}
            </div>

            {/* Activity */}
            <div className="gov-card p-6">
              <div className="text-[11px] font-semibold tracking-[0.22em] uppercase text-muted-foreground">Recent Activity</div>
              <h2 className="mt-1 font-serif text-xl text-foreground">Live Feed</h2>
              <div className="gold-divider mt-4" />
              {activity.length === 0 ? (
                <p className="mt-6 text-sm text-muted-foreground">No recent activity.</p>
              ) : (
                <ul className="mt-5 space-y-4">
                  {activity.map((a, i) => (
                    <li key={i} className="flex gap-4">
                      <div className="pt-1 text-xs font-mono text-muted-foreground w-14 shrink-0">{a.time}</div>
                      <div className="flex-1 border-l border-border pl-4 pb-2 -mt-1">
                        <div className="text-sm text-foreground">{a.name} checked in</div>
                        <div className="text-xs text-muted-foreground">{a.registration_id}</div>
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
