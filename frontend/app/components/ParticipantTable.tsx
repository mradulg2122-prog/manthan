"use client";

import { ParticipantRow } from "@/app/services/api";

interface Props {
  rows: ParticipantRow[];
  page: number;
  totalPages: number;
  onPageChange: (p: number) => void;
  onRowClick: (regId: string) => void;
  sortBy: string;
  sortOrder: string;
  onSort: (col: string) => void;
}

const columns = [
  { key: "registration_id", label: "Reg ID" },
  { key: "name", label: "Name" },
  { key: "email", label: "Email" },
  { key: "phone", label: "Phone" },
  { key: "attendance_status", label: "Attendance" },
  { key: "check_in_time", label: "Check-in" },
];

export default function ParticipantTable({
  rows, page, totalPages, onPageChange, onRowClick, sortBy, sortOrder, onSort,
}: Props) {
  const arrow = (col: string) => {
    if (sortBy !== col) return "";
    return sortOrder === "asc" ? " ↑" : " ↓";
  };

  return (
    <div className="bg-gray-800/40 border border-gray-700/40 rounded-xl overflow-hidden">
      {/* Table */}
      <div className="overflow-x-auto">
        <table className="w-full text-sm">
          <thead>
            <tr className="text-left text-gray-400 text-xs uppercase tracking-wider border-b border-gray-700/50">
              {columns.map((c) => (
                <th
                  key={c.key}
                  onClick={() => onSort(c.key)}
                  className="px-4 py-3 cursor-pointer hover:text-white transition-colors select-none"
                >
                  {c.label}{arrow(c.key)}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {rows.length === 0 && (
              <tr>
                <td colSpan={6} className="px-4 py-8 text-center text-gray-500">
                  No participants found.
                </td>
              </tr>
            )}
            {rows.map((r) => (
              <tr
                key={r.id}
                onClick={() => r.registration_id && onRowClick(r.registration_id)}
                className="border-b border-gray-800/50 hover:bg-gray-700/20 cursor-pointer transition-colors"
              >
                <td className="px-4 py-3 font-mono text-indigo-300 text-xs">{r.registration_id || "—"}</td>
                <td className="px-4 py-3 text-white">{r.name}</td>
                <td className="px-4 py-3 text-gray-300 hidden md:table-cell">{r.email}</td>
                <td className="px-4 py-3 text-gray-300 hidden lg:table-cell">{r.phone}</td>
                <td className="px-4 py-3">
                  <span className={`px-2 py-0.5 rounded-full text-xs font-medium ${
                    r.attendance_status === "Present"
                      ? "bg-emerald-500/20 text-emerald-400"
                      : "bg-red-500/15 text-red-400"
                  }`}>
                    {r.attendance_status}
                  </span>
                </td>
                <td className="px-4 py-3 text-gray-400 text-xs">{r.check_in_time || "—"}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between px-4 py-3 border-t border-gray-700/50 text-sm">
          <button
            disabled={page <= 1}
            onClick={() => onPageChange(page - 1)}
            className="px-3 py-1 bg-gray-700/50 rounded-lg disabled:opacity-30 hover:bg-gray-600 transition-colors text-gray-300"
          >
            Prev
          </button>
          <span className="text-gray-400">
            Page {page} of {totalPages}
          </span>
          <button
            disabled={page >= totalPages}
            onClick={() => onPageChange(page + 1)}
            className="px-3 py-1 bg-gray-700/50 rounded-lg disabled:opacity-30 hover:bg-gray-600 transition-colors text-gray-300"
          >
            Next
          </button>
        </div>
      )}
    </div>
  );
}
