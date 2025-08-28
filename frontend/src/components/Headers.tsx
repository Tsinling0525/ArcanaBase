import React from "react";

export default function Header() {
  return (
    <div className="flex items-center justify-between px-4 py-3 border-b bg-white/70 backdrop-blur sticky top-0 z-10 dark:bg-neutral-900 dark:border-neutral-800">
      <div className="font-semibold">📓 NotebookLM‑Style KB</div>
      <div className="text-sm text-neutral-500">First Cut · Local RAG</div>
    </div>
  );
}