import React, { useState } from 'react';
import useSSE from './hooks/useSSE';
import UploadPanel from './components/UploadPanel';
import DocumentList from './components/DocumentList';
import QueryInput from './components/QueryInput';
import ReasoningTrace from './components/ReasoningTrace';
import AnswerPanel from './components/AnswerPanel';
import SourcePanel from './components/SourcePanel';
import RelevanceChart from './components/RelevanceChart';

export function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);
  const [activeCitationIndex, setActiveCitationIndex] = useState(null);

  const {
    loading,
    cacheHit,
    traces,
    answer,
    documents,
    error,
    confidenceScore,
    citationsVerified,
    triggerQuery,
    clearSession,
  } = useSSE();

  const handleUploadSuccess = () => {
    setRefreshTrigger((prev) => prev + 1);
  };

  const handleSearchSubmit = (question) => {
    setActiveCitationIndex(null);
    triggerQuery(question);
  };

  const handleCitationClick = (index) => {
    setActiveCitationIndex(index);
  };

  return (
    <>
      {}
      <nav className="bg-surface-container-low dark:bg-surface-container-low docked h-screen w-sidebar-width left-0 border-r border-border-low-opacity flat no shadows fixed top-0 bottom-0 flex flex-col z-50">
        
        {}
        <div className="p-section-padding flex flex-col gap-2 border-b border-border-low-opacity">
          <div className="flex items-center gap-3">
            <div className="w-8 h-8 rounded-full bg-primary-container flex items-center justify-center text-on-primary-container">
              <span className="material-symbols-outlined">auto_awesome</span>
            </div>
            <div>
              <h1 className="text-headline-md font-headline-md text-on-surface dark:text-on-surface">DocMind</h1>
              <p className="text-label-caps font-label-caps text-on-surface-variant">Deep Research Engine</p>
            </div>
          </div>
          
          <div className="mt-4">
            <UploadPanel onUploadSuccess={handleUploadSuccess} />
          </div>
        </div>

        {}
        <div className="flex-1 overflow-y-auto py-4 px-2 flex flex-col gap-1">
          <div className="px-2 pb-2 text-label-caps font-label-caps text-on-surface-variant opacity-70">Navigation</div>
          <a className="text-primary dark:text-primary font-semibold border-r-2 border-primary bg-surface-elevated hover:bg-surface-elevated transition-colors duration-200 flex items-center gap-3 px-3 py-2 rounded-l" href="#">
            <span className="material-symbols-outlined">folder_open</span>
            <span className="font-body-sm text-body-sm">All Documents</span>
          </a>
          <a className="text-on-surface-variant dark:text-on-surface-variant hover:bg-surface-elevated transition-colors duration-200 flex items-center gap-3 px-3 py-2 rounded-lg" href="#">
            <span className="material-symbols-outlined">history</span>
            <span className="font-body-sm text-body-sm">Recent Queries</span>
          </a>

          {}
          <div className="mt-6">
             <DocumentList refreshTrigger={refreshTrigger} onRefresh={handleUploadSuccess} />
          </div>
        </div>

        {}
        <div className="p-4 border-t border-border-low-opacity flex flex-col gap-2">
          <a className="text-on-surface-variant hover:text-on-surface transition-colors flex items-center gap-3" href="#">
            <span className="material-symbols-outlined">analytics</span>
            <span className="font-label-caps text-label-caps">System Health</span>
          </a>
        </div>
      </nav>

      {}
      <main className="flex-1 ml-sidebar-width flex flex-col h-screen relative">
        
        {}
        {error && (
          <div className="absolute top-4 left-1/2 -translate-x-1/2 z-50 w-full max-w-md">
            <div className="bg-error-container text-on-error-container px-4 py-3 rounded-lg border border-error/20 flex items-center gap-3 shadow-lg">
              <span className="material-symbols-outlined text-error">warning</span>
              <p className="font-body-sm text-body-sm flex-1">{error}</p>
              <button className="text-on-error-container hover:text-error opacity-70 hover:opacity-100 transition-opacity">
                <span className="material-symbols-outlined">close</span>
              </button>
            </div>
          </div>
        )}

        {}
        <header className="bg-background/80 backdrop-blur-md docked full-width top-0 z-40 border-b border-border-low-opacity flat no shadows flex justify-between items-center px-gutter py-4">
          <div className="flex items-center gap-6">
            <div className="font-headline-md text-headline-md font-bold text-on-surface hidden md:block">DocMind</div>
            <nav className="flex items-center gap-6">
              <a className="text-primary border-b-2 border-primary pb-2 font-label-caps text-label-caps opacity-80" href="#">Research</a>
              <a className="text-on-surface-variant hover:text-on-surface hover:text-primary transition-colors font-label-caps text-label-caps pb-2" href="#">Sources</a>
              <a className="text-on-surface-variant hover:text-on-surface hover:text-primary transition-colors font-label-caps text-label-caps pb-2" href="#">Reasoning</a>
            </nav>
          </div>
          <div className="flex items-center gap-4">
            <button onClick={clearSession} className="px-4 py-1.5 bg-surface-elevated border border-border-low-opacity rounded text-primary font-label-caps text-label-caps hover:border-primary/50 transition-colors">
              New Session
            </button>
          </div>
        </header>

        {}
        <div className="flex-1 overflow-y-auto p-section-padding flex flex-col items-center">
          <div className="w-full max-w-max-content-width flex flex-col gap-stack-gap min-h-full pb-40">
            
            {(!loading && !answer && !error) && (
              <div className="bg-surface-elevated rounded-xl p-6 border border-border-low-opacity mb-4 text-center">
                 <span className="material-symbols-outlined text-text-muted text-4xl mb-4 opacity-40">help_center</span>
                 <h2 className="font-headline-lg text-headline-lg text-on-surface mb-2">RAG Engine Ready</h2>
                 <p className="font-body-md text-body-md text-on-surface-variant">Upload files on the left menu, then write your question below.</p>
              </div>
            )}

            {(loading || traces.length > 0) && (
              <ReasoningTrace traces={traces} loading={loading} />
            )}

            {answer && (
              <AnswerPanel
                answer={answer}
                loading={loading}
                cacheHit={cacheHit}
                confidenceScore={confidenceScore}
                citationsVerified={citationsVerified}
                onCitationClick={handleCitationClick}
              />
            )}

            {documents.length > 0 && (
              <div className="flex gap-4 mt-6">
                <div className="flex-1 min-w-0">
                  <RelevanceChart documents={documents} />
                </div>
                <div className="flex-1 min-w-0">
                  <SourcePanel documents={documents} activeCitationIndex={activeCitationIndex} />
                </div>
              </div>
            )}

          </div>
        </div>

        {}
        <div className="absolute bottom-0 left-0 w-full p-section-padding bg-gradient-to-t from-background via-background/90 to-transparent flex justify-center pb-8">
          <QueryInput onSubmit={handleSearchSubmit} loading={loading} />
        </div>
      </main>
    </>
  );
}

export default App;
