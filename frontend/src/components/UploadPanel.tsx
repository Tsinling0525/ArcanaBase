import React, { useRef } from "react";
import { ingestFile, ingestURL } from "../lib/api";

export default function UploadPanel({ onIngested }: { onIngested: () => void }) {
  const fileRef = useRef<HTMLInputElement>(null);
  const [url, setUrl] = React.useState("");
  const [busy, setBusy] = React.useState(false);

  async function handleFile(e: React.ChangeEvent<HTMLInputElement>) {
    const f = e.target.files?.[0];
    if (!f) return;
    setBusy(true);
    try {
      await ingestFile(f);
      onIngested();
    } finally {
      setBusy(false);
      if (fileRef.current) fileRef.current.value = "";
    }
  }

  async function handleURL() {
    if (!url) return;
    setBusy(true);
    try {
      await ingestURL(url);
      setUrl("");
      onIngested();
    } finally { setBusy(false); }
  }

  return (
    <div className="p-3 space-y-2">
      <div className="text-sm font-medium">导入资料</div>
      <input ref={fileRef} type="file" accept=".pdf,.txt,.md" onChange={handleFile}
             className="block w-full text-sm file:mr-3 file:py-1 file:px-3 file:rounded-xl file:border file:bg-white file:hover:bg-neutral-50 dark:file:bg-neutral-900 dark:file:hover:bg-neutral-800 file:border-neutral-200 dark:file:border-neutral-700" />
      <div className="flex gap-2">
        <input value={url} onChange={e=>setUrl(e.target.value)} placeholder="https://example.com/article" className="flex-1 px-3 py-2 rounded-xl border bg-white dark:bg-neutral-900 border-neutral-200 dark:border-neutral-700 text-sm" />
        <button onClick={handleURL} disabled={busy} className="px-3 py-2 rounded-xl border text-sm bg-black text-white dark:bg-white dark:text-black disabled:opacity-50">抓取URL</button>
      </div>
      {busy && <div className="text-xs text-neutral-500">处理中…</div>}
    </div>
  );
}