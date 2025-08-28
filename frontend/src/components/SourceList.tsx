import React from "react";
import { fetchSources } from "../lib/api";

export default function SourceList({ refreshKey }: { refreshKey: number }) {
  const [sources, setSources] = React.useState<Record<string, any>>({});
  React.useEffect(() => { fetchSources().then(setSources); }, [refreshKey]);

  const entries = Object.entries(sources);
  return (
    <div className="p-3 space-y-2">
      <div className="text-sm font-medium">资料库</div>
      <div className="space-y-1">
        {entries.length === 0 && <div className="text-xs text-neutral-500">尚无资料，先导入文件或URL</div>}
        {entries.map(([id, s]) => (
          <div key={id} className="px-3 py-2 rounded-xl border bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-700">
            <div className="text-sm font-medium truncate">{s.title || id}</div>
            <div className="text-xs text-neutral-500">{s.kind}</div>
          </div>
        ))}
      </div>
    </div>
  );
}