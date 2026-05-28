import React from 'react';

export function ReasoningTrace({ traces, loading }) {
  if (traces.length === 0 && !loading) return null;

  const renderTraceDot = (status) => {
    if (status === 'in_progress') {
      return (
        <div className="absolute -left-[23px] top-0 w-3.5 h-3.5 rounded-full border-2 border-primary/50 flex items-center justify-center">
          <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></div>
        </div>
      );
    }
    if (status === 'failed') {
      return (
        <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-error border border-error"></div>
      );
    }
    return (
      <div className="absolute -left-[21px] top-1 w-2.5 h-2.5 rounded-full bg-secondary"></div>
    );
  };

  const getTextColor = (status) => {
    if (status === 'in_progress') return 'text-primary';
    if (status === 'failed') return 'text-error line-through opacity-70';
    return 'text-secondary';
  };

  return (
    <div className="bg-surface-elevated rounded-xl p-6 border border-border-low-opacity mb-4 w-full text-left">
      <h2 className="font-headline-md text-headline-md text-on-surface mb-6 flex items-center gap-2">
        <span className="material-symbols-outlined text-primary">psychology</span>
        Agent Reasoning
      </h2>
      
      <div className="flex flex-col gap-4 pl-4 border-l-2 border-border-low-opacity ml-4 relative">
        {traces.length === 0 && loading && (
           <div className="relative mt-2">
             <div className="absolute -left-[23px] top-0 w-3.5 h-3.5 rounded-full border-2 border-primary/50 flex items-center justify-center">
               <div className="w-1.5 h-1.5 rounded-full bg-primary animate-pulse"></div>
             </div>
             <p className="font-label-caps text-label-caps text-primary uppercase tracking-widest">Initializing graph state machine...</p>
           </div>
        )}

        {traces.map((trace, idx) => (
          <div key={idx} className="relative mt-2">
            {renderTraceDot(trace.status)}
            <p className={`font-label-caps text-label-caps uppercase tracking-widest ${getTextColor(trace.status)}`}>
              {trace.step}
            </p>
            <p className="font-body-sm text-body-sm text-text-muted mt-1">{trace.message}</p>
          </div>
        ))}
      </div>
    </div>
  );
}

export default ReasoningTrace;
