import { useState, useCallback, useEffect, useRef } from 'react';

export function useSSE() {
  const [loading, setLoading] = useState(false);
  const [cacheHit, setCacheHit] = useState(false);
  const [traces, setTraces] = useState([]);
  const [answer, setAnswer] = useState('');
  const [documents, setDocuments] = useState([]);
  const [error, setError] = useState(null);
  const [confidenceScore, setConfidenceScore] = useState(null);
  const [citationsVerified, setCitationsVerified] = useState(false);
  
  const eventSourceRef = useRef(null);

  const clearSession = useCallback(() => {
    if (eventSourceRef.current) {
      eventSourceRef.current.close();
      eventSourceRef.current = null;
    }
    setLoading(false);
    setCacheHit(false);
    setTraces([]);
    setAnswer('');
    setDocuments([]);
    setError(null);
    setConfidenceScore(null);
    setCitationsVerified(false);
  }, []);

  const triggerQuery = useCallback((question) => {
    clearSession();
    setLoading(true);

    const API_BASE = import.meta.env.VITE_API_URL || '';
    const sseUrl = `${API_BASE}/api/query?question=${encodeURIComponent(question)}`;
    const eventSource = new EventSource(sseUrl);
    eventSourceRef.current = eventSource;

    eventSource.onmessage = (event) => {
      try {
        const payload = JSON.parse(event.data);
        const { event: eventType, data } = payload;

        switch (eventType) {
          case 'cache_hit':
            setCacheHit(data);
            break;
            
          case 'trace':
            setTraces((prev) => {
              const existingIdx = prev.findIndex((t) => t.step === data.step);
              if (existingIdx >= 0) {
                const copy = [...prev];
                copy[existingIdx] = data;
                return copy;
              }
              return [...prev, data];
            });
            break;

          case 'docs':
            setDocuments(data);
            break;
            
          case 'score':
            setConfidenceScore(data.confidence);
            setCitationsVerified(data.citations);
            break;

          case 'token':
            setAnswer((prev) => prev + data);
            break;

          case 'error':
            setError(data);
            eventSource.close();
            setLoading(false);
            break;

          case 'done':
            eventSource.close();
            setLoading(false);
            break;

          default:
            break;
        }
      } catch (err) {
        console.error('Failed to parse SSE payload:', err);
      }
    };

    eventSource.onerror = (err) => {
      console.error('SSE connection error:', err);
      setError('Connection interrupted. Please make sure the backend is active.');
      eventSource.close();
      setLoading(false);
    };

  }, [clearSession]);

  useEffect(() => {
    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, []);

  return {
    loading,
    cacheHit,
    traces,
    answer,
    documents,
    error,
    confidenceScore,
    citationsVerified,
    triggerQuery,
    clearSession
  };
}
export default useSSE;
