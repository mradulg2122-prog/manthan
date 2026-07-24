"use client";

import { ActivityItem } from "@/app/services/api";

interface Props {
  items: ActivityItem[];
}

export default function ActivityFeed({ items }: Props) {
  if (items.length === 0) {
    return <p className="text-gray-500 text-sm text-center py-6">No check-ins yet.</p>;
  }

  return (
    <div className="space-y-2 max-h-80 overflow-y-auto pr-1">
      {items.map((item, i) => (
        <div
          key={`${item.registration_id}-${i}`}
          className="flex items-center gap-3 bg-gray-800/40 rounded-lg px-4 py-2.5"
        >
          <span className="text-xs text-gray-500 font-mono w-16 shrink-0">{item.time}</span>
          <div className="flex-1 min-w-0">
            <p className="text-white text-sm truncate">{item.name}</p>
            <p className="text-gray-500 text-xs">Marked {item.status}</p>
          </div>
          <span className="text-xs font-mono text-indigo-400">{item.registration_id}</span>
        </div>
      ))}
    </div>
  );
}
