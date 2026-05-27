import React, { useEffect, useState } from 'react';

export function DocumentList({ refreshTrigger, onRefresh }) {
  const [documents, setDocuments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [deletingId, setDeletingId] = useState(null);

  const fetchDocuments = async () => {
    setLoading(true);
    try {
      const API_BASE = import.meta.env.VITE_API_URL || '';
      const response = await fetch(`${API_BASE}/api/documents`);
      if (response.ok) {
        const data = await response.json();
        setDocuments(data);
      }
    } catch (err) {
      console.error("Failed to load documents", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDocuments();
  }, [refreshTrigger]);

  const handleDelete = async (id, name, e) => {
    e.stopPropagation();
    if (!confirm(`Are you sure you want to delete '${name}'?`)) {
      return;
    }
    
    setDeletingId(id);
    try {
      const API_BASE = import.meta.env.VITE_API_URL || '';
      const response = await fetch(`${API_BASE}/api/documents/${id}`, {
        method: 'DELETE',
      });
      if (response.ok) {
        fetchDocuments();
        if (onRefresh) onRefresh();
      } else {
        const data = await response.json();
        alert(data.detail || "Failed to delete document.");
      }
    } catch (err) {
      console.error(err);
      alert("Network error.");
    } finally {
      setDeletingId(null);
    }
  };

  return (
    <div className="flex flex-col gap-2">
      <div className="px-2 pb-2 flex justify-between items-center">
        <span className="text-label-caps font-label-caps text-on-surface-variant opacity-70">Active Documents</span>
        <span className="w-4 h-4 rounded-full bg-surface-elevated border border-border-low-opacity flex items-center justify-center text-[10px] text-on-surface-variant">{documents.length}</span>
      </div>

      {loading ? (
        <div className="p-4 text-center">
          <span className="material-symbols-outlined animate-spin text-primary">sync</span>
        </div>
      ) : documents.length === 0 ? (
        <div className="p-4 text-center text-on-surface-variant text-body-sm font-body-sm opacity-70">
          No documents indexed yet.
        </div>
      ) : (
        <div className="flex flex-col gap-2 max-h-[40vh] overflow-y-auto px-1">
          {documents.map((doc) => (
            <div key={doc.id} className="bg-surface-elevated p-3 rounded-lg border border-border-low-opacity hover:border-primary/30 transition-colors cursor-pointer group relative">
              <div className="flex items-start gap-3">
                <span className="material-symbols-outlined text-secondary text-sm mt-0.5">description</span>
                <div className="flex-1 min-w-0 pr-6">
                  <p className="text-body-sm font-body-sm text-on-surface truncate" title={doc.filename}>{doc.filename}</p>
                  <div className="flex items-center gap-2 mt-1">
                    <div className="h-1 flex-1 bg-surface-container-high rounded-full overflow-hidden">
                      <div className="h-full bg-secondary w-full"></div>
                    </div>
                    <span className="text-label-caps font-label-caps text-secondary">{doc.chunk_count} CHKS</span>
                  </div>
                </div>
              </div>
              <button
                className="absolute top-2 right-2 text-text-muted hover:text-error hover:bg-error/10 p-1 rounded transition-colors"
                onClick={(e) => handleDelete(doc.id, doc.filename, e)}
                disabled={deletingId === doc.id}
                title="Delete document"
              >
                {deletingId === doc.id ? (
                  <span className="material-symbols-outlined text-sm animate-spin text-error">sync</span>
                ) : (
                  <span className="material-symbols-outlined text-sm">delete</span>
                )}
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default DocumentList;
