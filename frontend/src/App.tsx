import React from "react";
import Header from "./components/Headers";
import UploadPanel from "./components/UploadPanel";
import SourceList from "./components/SourceList";
import ChatPanel from "./components/ChatPanel";

export default function App() {
  const [refreshKey, setRefreshKey] = React.useState(0);
  return (
    <div className="h-screen grid grid-cols-12 bg-neutral-50 dark:bg-neutral-950 text-neutral-900 dark:text-neutral-100">
      <div className="col-span-12"><Header /></div>
      <div className="col-span-12 md:col-span-3 xl:col-span-3 border-r dark:border-neutral-800 flex flex-col">
        <UploadPanel onIngested={() => setRefreshKey(k=>k+1)} />
        <div className="flex-1 overflow-auto"><SourceList refreshKey={refreshKey} /></div>
      </div>
      <div className="col-span-12 md:col-span-9 xl:col-span-9"><ChatPanel /></div>
    </div>
  );
}