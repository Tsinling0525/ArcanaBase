import React from "react";
import { Hit, QueryResponse } from "../types";
import { queryKB } from "../lib/api";

export default function ChatPanel() {
  const [q, setQ] = React.useState("");
  const [persona, setPersona] = React.useState<string | undefined>(undefined);
  const [loading, setLoading] = React.useState(false);
  const [resp, setResp] = React.useState<QueryResponse | null>(null);

  async function ask() {
    if (!q.trim()) return;
    setLoading(true);
    try { setResp(await queryKB(q, 5, persona)); }
    finally { setLoading(false); }
  }

  return (
    <div className="h-full flex flex-col">
      <div className="p-4 border-b dark:border-neutral-800 bg-white/60 dark:bg-neutral-900/60 backdrop-blur">
        <div className="flex gap-2">
          <input value={q} onChange={e=>setQ(e.target.value)} onKeyDown={e=>e.key==='Enter'&&ask()}
                 placeholder="提问：例如 ‘总结这份PDF的要点’"
                 className="flex-1 px-3 py-2 rounded-xl border bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-700" />
          <select value={persona||""} onChange={e=>setPersona(e.target.value||undefined)} className="px-3 py-2 rounded-xl border bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-700 text-sm">
            <option value="">默认</option>
            <option value="diviner">算命语气（仅风格）</option>
          </select>
          <button onClick={ask} disabled={loading}
                  className="px-4 py-2 rounded-xl bg-black text-white dark:bg-white dark:text-black disabled:opacity-50">检索</button>
        </div>
      </div>

      <div className="flex-1 overflow-auto p-6 space-y-4">
        {!resp && <div className="text-sm text-neutral-500">从左侧导入资料，然后在上方输入你的问题。</div>}
        {resp && (
          <div className="space-y-4">
            <div className="prose prose-neutral dark:prose-invert max-w-none bg-white dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-700 rounded-2xl p-4">
              <div className="text-sm text-neutral-500 mb-2">回答</div>
              <div className="whitespace-pre-wrap leading-relaxed">{resp.answer}</div>
            </div>
            <div>
              <div className="text-sm text-neutral-500 mb-2">依据（Citations）</div>
              <div className="grid md:grid-cols-2 gap-3">
                {resp.hits.map((h: Hit, i: number) => (
                  <div key={i} className="p-3 rounded-xl border bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-700">
                    <div className="text-xs text-neutral-500">{h.chunk.source_id} · 相似度 {h.score.toFixed(3)}</div>
                    <div className="text-sm mt-1 line-clamp-6 whitespace-pre-wrap">{h.chunk.text}</div>
                  </div>
                ))}
              </div>
            </div>
          </div>
        )}
        {loading && <div className="text-sm text-neutral-500">检索中……</div>}
      </div>
    </div>
  );
}