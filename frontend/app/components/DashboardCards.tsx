"use client";

import { DashboardStats } from "@/app/services/api";

interface Props {
  stats: DashboardStats | null;
}

export default function DashboardCards({ stats }: Props) {
  if (!stats) return null;

  const cards = [
    { label: "Total Registrations", value: stats.total, color: "text-indigo-400", bg: "bg-indigo-500/10 border-indigo-500/20" },
    { label: "Present", value: stats.present, color: "text-emerald-400", bg: "bg-emerald-500/10 border-emerald-500/20" },
    { label: "Absent", value: stats.absent, color: "text-red-400", bg: "bg-red-500/10 border-red-500/20" },
    { label: "Attendance %", value: `${stats.percentage}%`, color: "text-amber-400", bg: "bg-amber-500/10 border-amber-500/20" },
  ];

  return (
    <div className="grid grid-cols-2 lg:grid-cols-4 gap-4">
      {cards.map((c) => (
        <div key={c.label} className={`rounded-xl border p-5 ${c.bg}`}>
          <p className="text-gray-400 text-xs uppercase tracking-wider">{c.label}</p>
          <p className={`text-3xl font-bold mt-1 ${c.color}`}>{c.value}</p>
        </div>
      ))}
    </div>
  );
}
