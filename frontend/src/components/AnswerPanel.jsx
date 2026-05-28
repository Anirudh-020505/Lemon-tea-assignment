import React from 'react';

export function AnswerPanel({ answer, loading, cacheHit, confidenceScore, citationsVerified, onCitationClick }) {
  if (!answer && !loading) return null;

  const renderFormattedAnswer = (text) => {
    if (!text) return null;
    const lines = text.split('\n');
    return lines.map((line, lineIdx) => {
      const isBullet = line.trim().startsWith('-') || line.trim().startsWith('*');
      const cleanLine = isBullet ? line.replace(/^[-*]\s+/, '') : line;
      const citationRegex = /\[(\d+)\]/g;
      const elements = [];
      let lastIdx = 0;
      let match;

      while ((match = citationRegex.exec(cleanLine)) !== null) {
        const matchIdx = match.index;
        const citationNumber = match[1];

        if (matchIdx > lastIdx) {
          elements.push(cleanLine.substring(lastIdx, matchIdx));
        }

        elements.push(
          <button
            key={`cit-${matchIdx}`}
            className="inline-flex items-center justify-center w-4 h-4 text-[10px] font-bold rounded-full bg-secondary/10 border border-secondary/30 text-secondary hover:bg-secondary hover:text-on-secondary transition-colors cursor-pointer mx-1 align-middle -translate-y-px"
            onClick={() => onCitationClick && onCitationClick(parseInt(citationNumber, 10))}
            title={`View Source Context [${citationNumber}]`}
          >
            {citationNumber}
          </button>
        );

        lastIdx = citationRegex.lastIndex;
      }

      if (lastIdx < cleanLine.length) {
        elements.push(cleanLine.substring(lastIdx));
      }

      if (isBullet) {
        return <li key={lineIdx} className="ml-5 mb-2 list-square">{elements}</li>;
      }
      if (!line.trim()) {
        return <div key={lineIdx} className="h-3" />;
      }
      return <p key={lineIdx} className="mb-3">{elements}</p>;
    });
  };

  return (
    <div className="bg-surface-elevated rounded-xl p-6 border border-border-low-opacity mb-4 w-full text-left">
      <div className="flex items-center justify-between pb-3 mb-4 border-b border-border-low-opacity">
        <h2 className="font-headline-lg text-headline-lg text-on-surface flex items-center gap-2">
          <span className="material-symbols-outlined text-primary">auto_awesome</span>
          Generated Answer
        </h2>
        <div className="flex items-center gap-2">
          {confidenceScore !== null && (
            <span className="text-[10px] font-bold bg-secondary/10 text-secondary border border-secondary/20 px-2 py-0.5 rounded flex items-center gap-1">
              <span className="material-symbols-outlined text-[12px]">verified</span>
              {confidenceScore}% Confidence
            </span>
          )}
          {citationsVerified && (
            <span className="text-[10px] font-bold bg-tertiary/10 text-tertiary border border-tertiary/20 px-2 py-0.5 rounded flex items-center gap-1">
              <span className="material-symbols-outlined text-[12px]">fact_check</span>
              Citations Verified
            </span>
          )}
          {cacheHit && (
            <span className="text-[10px] font-bold bg-primary/10 text-primary border border-primary/20 px-2 py-0.5 rounded uppercase">
              Cached Response
            </span>
          )}
        </div>
      </div>

      <div className="leading-relaxed text-[15px] text-on-surface/95">
        {answer ? (
          <div>
            {renderFormattedAnswer(answer)}
            {loading && <span className="text-primary animate-pulse ml-1">▋</span>}
          </div>
        ) : (
          <div className="flex flex-col gap-3">
            <div className="h-3.5 rounded bg-surface-container-high animate-pulse w-full"></div>
            <div className="h-3.5 rounded bg-surface-container-high animate-pulse w-5/6"></div>
            <div className="h-3.5 rounded bg-surface-container-high animate-pulse w-3/4"></div>
          </div>
        )}
      </div>
    </div>
  );
}

export default AnswerPanel;
