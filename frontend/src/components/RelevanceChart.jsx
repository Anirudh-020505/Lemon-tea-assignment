import React from 'react';

export function RelevanceChart({ documents }) {
  if (documents.length === 0) return null;

  const candidates = documents.slice(0, 5);
  const width = 450;
  const height = 180;
  const paddingLeft = 36;
  const paddingRight = 16;
  const paddingTop = 16;
  const paddingBottom = 24;

  const chartWidth = width - paddingLeft - paddingRight;
  const chartHeight = height - paddingTop - paddingBottom;
  const numGroups = candidates.length;
  const groupWidth = chartWidth / numGroups;
  const barSpacing = 4;
  const numBarsPerGroup = 3;
  const totalBarSpacing = (numBarsPerGroup - 1) * barSpacing;
  const barWidth = Math.max((groupWidth - 20 - totalBarSpacing) / numBarsPerGroup, 4);

  return (
    <div className="bg-surface-elevated rounded-xl p-4 border border-border-low-opacity w-full h-full flex flex-col">
      <div className="flex items-center gap-2 pb-2 mb-2 border-b border-border-low-opacity">
        <span className="material-symbols-outlined text-primary text-sm">bar_chart</span>
        <h3 className="font-headline-md text-sm font-semibold text-on-surface">Relevance Match</h3>
      </div>
      
      <div className="flex-1 w-full flex flex-col">
        <svg viewBox={`0 0 ${width} ${height}`} className="w-full h-full min-h-[140px]">
          {[0, 0.25, 0.5, 0.75, 1.0].map((val, idx) => {
            const y = paddingTop + (1 - val) * chartHeight;
            return (
              <g key={`grid-${idx}`}>
                <line x1={paddingLeft} y1={y} x2={width - paddingRight} y2={y} stroke="rgba(255,255,255,0.04)" strokeWidth="1" />
                <text x={paddingLeft - 8} y={y + 3} className="fill-text-muted text-[8px] font-mono" textAnchor="end">
                  {Math.round(val * 100)}%
                </text>
              </g>
            );
          })}

          {candidates.map((doc, idx) => {
            const groupX = paddingLeft + idx * groupWidth;
            const centerX = groupX + groupWidth / 2;
            const cVal = doc.score || 0.0;
            const dVal = doc.norm_dense || cVal * 0.95;
            const sVal = doc.norm_sparse || cVal * 0.85;
            const dHeight = dVal * chartHeight;
            const sHeight = sVal * chartHeight;
            const cHeight = cVal * chartHeight;
            const startX = groupX + (groupWidth - (barWidth * 3 + barSpacing * 2)) / 2;
            
            return (
              <g key={`group-${idx}`}>
                <rect x={startX} y={paddingTop + chartHeight - dHeight} width={barWidth} height={dHeight} className="fill-primary" rx="1" opacity="0.8" />
                <rect x={startX + barWidth + barSpacing} y={paddingTop + chartHeight - sHeight} width={barWidth} height={sHeight} className="fill-tertiary" rx="1" opacity="0.8" />
                <rect x={startX + (barWidth + barSpacing) * 2} y={paddingTop + chartHeight - cHeight} width={barWidth} height={cHeight} className="fill-secondary" rx="1.5" />
                <text x={centerX - 4} y={height - paddingBottom + 14} className="fill-text-secondary text-[9px] font-bold font-sans" textAnchor="middle">
                  [{idx + 1}]
                </text>
              </g>
            );
          })}
          <line x1={paddingLeft} y1={paddingTop + chartHeight} x2={width - paddingRight} y2={paddingTop + chartHeight} stroke="var(--color-border-low-opacity, rgba(255,255,255,0.08))" strokeWidth="1" />
        </svg>

        <div className="flex items-center justify-center gap-4 flex-wrap pt-2 mt-auto border-t border-border-low-opacity">
          <div className="flex items-center gap-1.5 text-[11px] text-text-secondary">
            <div className="w-1.5 h-1.5 rounded-full bg-primary" />
            <span>Dense</span>
          </div>
          <div className="flex items-center gap-1.5 text-[11px] text-text-secondary">
            <div className="w-1.5 h-1.5 rounded-full bg-tertiary" />
            <span>Sparse</span>
          </div>
          <div className="flex items-center gap-1.5 text-[11px] text-text-secondary">
            <div className="w-1.5 h-1.5 rounded-full bg-secondary" />
            <span>Combined</span>
          </div>
        </div>
      </div>
    </div>
  );
}

export default RelevanceChart;
