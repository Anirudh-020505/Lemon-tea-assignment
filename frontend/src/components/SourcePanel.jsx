import React, { useEffect, useRef } from 'react';

export function SourcePanel({ documents, activeCitationIndex }) {
  const containerRef = useRef(null);
  const itemRefs = useRef({});

  useEffect(() => {
    if (activeCitationIndex && itemRefs.current[activeCitationIndex]) {
      itemRefs.current[activeCitationIndex].scrollIntoView({
        behavior: 'smooth',
        block: 'nearest',
      });
    }
  }, [activeCitationIndex]);

  if (documents.length === 0) return null;

  return (
    <div className="bg-surface-elevated rounded-xl p-4 border border-border-low-opacity w-full h-full flex flex-col max-h-[380px]" ref={containerRef}>
      <div className="flex items-center gap-2 pb-2 mb-2 border-b border-border-low-opacity shrink-0">
        <span className="material-symbols-outlined text-secondary text-sm">library_books</span>
        <h3 className="font-headline-md text-sm font-semibold text-on-surface">Source Context</h3>
      </div>
      <div className="flex flex-col gap-3 overflow-y-auto pr-1 flex-1">
        {documents.map((doc, idx) => {
          const indexNum = idx + 1;
          const isActive = indexNum === activeCitationIndex;
          
          return (
            <div
              key={doc.chunk_id || idx}
              ref={(el) => (itemRefs.current[indexNum] = el)}
              className={`border rounded-lg p-3 flex flex-col gap-2 transition-all ${
                isActive 
                  ? 'border-secondary shadow-[0_0_12px_rgba(78,222,163,0.15)] bg-secondary/5' 
                  : 'border-border-low-opacity bg-surface-container'
              }`}
            >
              <div className="flex items-center justify-between text-xs">
                <div className="flex items-center gap-2 overflow-hidden flex-1">
                  <span
                    className={`inline-flex items-center justify-center text-[10px] font-bold px-1.5 py-0.5 rounded ${
                      isActive ? 'bg-secondary text-on-secondary' : 'bg-surface-elevated border border-border-low-opacity text-on-surface'
                    }`}
                  >
                    [{indexNum}]
                  </span>
                  <div className="flex flex-col overflow-hidden">
                    <span className="font-semibold text-on-surface truncate max-w-[180px]" title={doc.document}>
                      {doc.document}
                    </span>
                    <span className="text-[10px] text-text-muted mt-px">
                      Chunk {doc.id || idx + 1}
                    </span>
                  </div>
                </div>
                <div className="flex items-center gap-1 bg-surface-elevated/50 px-1.5 py-0.5 rounded border border-border-low-opacity shrink-0">
                  <span className="material-symbols-outlined text-[12px] text-secondary">workspace_premium</span>
                  <span className="text-[10px] font-bold text-secondary">
                    {Math.round((doc.score || 0) * 100)}% Match
                  </span>
                </div>
              </div>
              <p className="text-xs text-text-secondary leading-relaxed whitespace-pre-wrap bg-black/20 p-2 rounded border-l-2 border-border-low-opacity">
                {doc.content}
              </p>
            </div>
          );
        })}
      </div>
    </div>
  );
}

export default SourcePanel;
