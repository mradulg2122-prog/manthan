"use client";

import { ParticipantDetail as Detail, updateAttendance } from "@/app/services/api";
import { useState } from "react";

interface Props {
  detail: Detail;
  onClose: () => void;
  onUpdated: () => void;
}

export default function ParticipantDetails({ detail, onClose, onUpdated }: Props) {
  const [loading, setLoading] = useState(false);

  const toggle = async (action: "present" | "absent") => {
    setLoading(true);
    await updateAttendance(detail.registration_id, action);
    setLoading(false);
    onUpdated();
  };

  const rows = [
    { label: "Registration ID", value: detail.registration_id },
    { label: "Name", value: detail.name },
    { label: "Email", value: detail.email },
    { label: "Phone", value: detail.phone },
    { label: "College", value: detail.college },
    { label: "Event", value: detail.event },
    { label: "Attendance", value: detail.attendance_status },
    { label: "Check-in Time", value: detail.check_in_time || "—" },
    { label: "QR Status", value: detail.qr_sent ? "✅ Sent" : "❌ Pending" },
    { label: "Email Status", value: detail.email_sent ? "✅ Sent" : "❌ Pending" },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/60 backdrop-blur-sm px-4">
      <div className="bg-gray-900 border border-gray-700/50 rounded-2xl w-full max-w-md p-6 space-y-4 max-h-[90vh] overflow-y-auto">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white">Participant Details</h2>
          <button onClick={onClose} className="text-gray-400 hover:text-white text-xl leading-none">&times;</button>
        </div>

        <div className="space-y-2">
          {rows.map((r) => (
            <div key={r.label} className="flex justify-between text-sm">
              <span className="text-gray-400">{r.label}</span>
              <span className="text-white text-right max-w-[60%] break-all">{r.value || "—"}</span>
            </div>
          ))}
        </div>

        {/* Manual attendance buttons */}
        <div className="flex gap-3 pt-2">
          {detail.attendance_status !== "Present" ? (
            <button
              disabled={loading}
              onClick={() => toggle("present")}
              className="flex-1 py-2.5 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 text-white font-semibold rounded-xl transition-colors"
            >
              Mark Present
            </button>
          ) : (
            <button
              disabled={loading}
              onClick={() => toggle("absent")}
              className="flex-1 py-2.5 bg-red-600 hover:bg-red-500 disabled:opacity-50 text-white font-semibold rounded-xl transition-colors"
            >
              Mark Absent
            </button>
          )}
          <button
            onClick={onClose}
            className="flex-1 py-2.5 bg-gray-700 hover:bg-gray-600 text-gray-300 font-semibold rounded-xl transition-colors"
          >
            Close
          </button>
        </div>
      </div>
    </div>
  );
}
