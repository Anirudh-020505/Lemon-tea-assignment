import React, { useState, useRef, useEffect } from 'react';

export function QueryInput({ onSubmit, loading }) {
  const [query, setQuery] = useState('');
  const textareaRef = useRef(null);

  useEffect(() => {
    if (textareaRef.current) {
      textareaRef.current.style.height = 'auto';
      textareaRef.current.style.height = `${Math.min(textareaRef.current.scrollHeight, 128)}px`;
    }
  }, [query]);

  const handleSubmit = (e) => {
    e?.preventDefault();
    if (!query.trim() || loading) return;
    onSubmit(query.trim());
    setQuery('');
  };

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSubmit();
    }
  };

  return (
    <div className="w-full max-w-max-content-width relative">
      <form 
        onSubmit={handleSubmit}
        className="bg-surface-elevated border border-border-low-opacity rounded-xl p-2 flex items-end gap-2 focus-within:border-primary/50 transition-colors shadow-lg"
      >
        <textarea
          ref={textareaRef}
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={handleKeyDown}
          className="w-full bg-transparent border-none focus:ring-0 text-body-md font-body-md text-on-surface resize-none max-h-32 min-h-[44px] py-2 px-3 placeholder:text-text-muted outline-none"
          placeholder="Ask a question about your documents..."
          rows={1}
          disabled={loading}
        />
        <button
          type="submit"
          disabled={!query.trim() || loading}
          className={`w-11 h-11 rounded-lg flex items-center justify-center shrink-0 transition-opacity ${
            query.trim() && !loading 
              ? 'bg-gradient-to-br from-primary to-primary-container text-on-primary-container hover:opacity-90' 
              : 'bg-surface-container text-text-muted opacity-50 cursor-not-allowed'
          }`}
        >
          <span className="material-symbols-outlined">send</span>
        </button>
      </form>
      <div className="mt-2 flex items-center justify-between px-2">
        <span className="font-label-caps text-label-caps text-warning-amber flex items-center gap-1 opacity-0">
          <span className="material-symbols-outlined text-[14px]">warning</span>
          Context may be incomplete
        </span>
        <span className="font-label-caps text-label-caps text-text-muted">Press Enter to send</span>
      </div>
    </div>
  );
}

export default QueryInput;
