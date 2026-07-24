"use client";

/**
 * System Status Card — shows backend, database, watcher, email status.
 */

export interface SystemHealth {
  status: string;
  database: string;
  watcher: string;
  email: string;
}

interface Props {
  health: SystemHealth | null;
}

export default function SystemStatus({ health }: Props) {
  if (!health) return null;

  const services = [
    { label: "Backend", ok: true },
    { label: "Database", ok: health.database === "connected" },
    { label: "Watcher", ok: health.watcher === "running" },
    { label: "Email", ok: health.email === "connected" },
  ];

  return (
    <div className="bg-gray-800/30 border border-gray-700/40 rounded-xl p-5">
      <h2 className="text-sm font-semibold text-gray-300 uppercase tracking-wider mb-3">
        System Status
      </h2>
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
        {services.map((s) => (
          <div key={s.label} className="flex items-center gap-2">
            <span className={`text-sm ${s.ok ? "text-emerald-400" : "text-red-400"}`}>
              {s.ok ? "🟢" : "🔴"}
            </span>
            <div>
              <p className="text-white text-sm">{s.label}</p>
              <p className={`text-xs ${s.ok ? "text-emerald-400" : "text-red-400"}`}>
                {s.ok ? "Running" : "Offline"}
              </p>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}
