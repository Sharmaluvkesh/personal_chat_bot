import React, { useState, useEffect } from 'react';
import { X, Upload, Trash2, FileText, Plus, Key, Database, Sparkles, Check, AlertCircle } from 'lucide-react';

export default function KnowledgeManager({ isOpen, onClose, apiKey, setApiKey, onRefreshStats }) {
  const [documents, setDocuments] = useState([]);
  const [facts, setFacts] = useState([]);
  const [activeTab, setActiveTab] = useState('docs'); // 'docs' | 'facts' | 'api'
  
  // Upload State
  const [uploading, setUploading] = useState(false);
  const [uploadMessage, setUploadMessage] = useState(null);

  // New Fact State
  const [newQuestion, setNewQuestion] = useState('');
  const [newAnswer, setNewAnswer] = useState('');
  const [newCategory, setNewCategory] = useState('General');
  const [addingFact, setAddingFact] = useState(false);

  // Temp API key state
  const [keyInput, setKeyInput] = useState(apiKey || '');
  const [keySaved, setKeySaved] = useState(false);

  useEffect(() => {
    if (isOpen) {
      fetchDocuments();
      fetchFacts();
    }
  }, [isOpen]);

  const fetchDocuments = async () => {
    try {
      const res = await fetch('/api/documents');
      if (res.ok) {
        const data = await res.json();
        setDocuments(data.documents || []);
        if (onRefreshStats) onRefreshStats();
      }
    } catch (err) {
      console.error("Error fetching docs:", err);
    }
  };

  const fetchFacts = async () => {
    try {
      const res = await fetch('/api/facts');
      if (res.ok) {
        const data = await res.json();
        setFacts(data.facts || []);
      }
    } catch (err) {
      console.error("Error fetching facts:", err);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;

    setUploading(true);
    setUploadMessage(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const res = await fetch('/api/documents/upload', {
        method: 'POST',
        body: formData
      });

      const data = await res.json();
      if (res.ok) {
        setUploadMessage({ type: 'success', text: data.message });
        fetchDocuments();
      } else {
        setUploadMessage({ type: 'error', text: data.detail || 'Upload failed.' });
      }
    } catch (err) {
      setUploadMessage({ type: 'error', text: 'Error uploading file.' });
    } finally {
      setUploading(false);
    }
  };

  const handleDeleteDoc = async (filename) => {
    if (!confirm(`Delete ${filename} from knowledge base?`)) return;
    try {
      const res = await fetch(`/api/documents/${encodeURIComponent(filename)}`, { method: 'DELETE' });
      if (res.ok) {
        fetchDocuments();
      }
    } catch (err) {
      console.error("Delete doc error:", err);
    }
  };

  const handleAddFact = async (e) => {
    e.preventDefault();
    if (!newQuestion.trim() || !newAnswer.trim()) return;

    setAddingFact(true);
    try {
      const res = await fetch('/api/facts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: newQuestion.trim(),
          answer: newAnswer.trim(),
          category: newCategory
        })
      });

      if (res.ok) {
        setNewQuestion('');
        setNewAnswer('');
        fetchFacts();
      }
    } catch (err) {
      console.error("Add fact error:", err);
    } finally {
      setAddingFact(false);
    }
  };

  const handleDeleteFact = async (factId) => {
    try {
      const res = await fetch(`/api/facts/${factId}`, { method: 'DELETE' });
      if (res.ok) {
        fetchFacts();
      }
    } catch (err) {
      console.error("Delete fact error:", err);
    }
  };

  const handleSaveApiKey = () => {
    setApiKey(keyInput.trim());
    localStorage.setItem('groq_api_key', keyInput.trim());
    setKeySaved(true);
    setTimeout(() => setKeySaved(false), 2000);
  };

  if (!isOpen) return null;

  return (
    <div style={{
      position: 'fixed',
      top: 0,
      left: 0,
      right: 0,
      bottom: 0,
      backgroundColor: 'rgba(9, 13, 22, 0.85)',
      backdropFilter: 'blur(12px)',
      zIndex: 1000,
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: '20px'
    }}>
      <div className="glass-card animate-fade-in" style={{
        width: '100%',
        maxWidth: '680px',
        maxHeight: '85vh',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden'
      }}>
        
        {/* Modal Header */}
        <div style={{
          padding: '18px 24px',
          borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between'
        }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
            <Database size={20} color="#a5b4fc" />
            <h2 style={{ fontSize: '1.2rem', margin: 0 }}>Knowledge Base Manager</h2>
          </div>
          <button
            onClick={onClose}
            style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}
          >
            <X size={20} />
          </button>
        </div>

        {/* Modal Tabs */}
        <div style={{
          display: 'flex',
          borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
          background: 'rgba(15, 23, 42, 0.5)'
        }}>
          <button
            onClick={() => setActiveTab('docs')}
            style={{
              flex: 1,
              padding: '12px',
              border: 'none',
              background: activeTab === 'docs' ? 'rgba(99, 102, 241, 0.15)' : 'transparent',
              color: activeTab === 'docs' ? '#a5b4fc' : '#94a3b8',
              borderBottom: activeTab === 'docs' ? '2px solid #6366f1' : 'none',
              fontWeight: 600,
              fontSize: '0.88rem',
              cursor: 'pointer'
            }}
          >
            📄 Documents & PDFs ({documents.length})
          </button>

          <button
            onClick={() => setActiveTab('facts')}
            style={{
              flex: 1,
              padding: '12px',
              border: 'none',
              background: activeTab === 'facts' ? 'rgba(99, 102, 241, 0.15)' : 'transparent',
              color: activeTab === 'facts' ? '#a5b4fc' : '#94a3b8',
              borderBottom: activeTab === 'facts' ? '2px solid #6366f1' : 'none',
              fontWeight: 600,
              fontSize: '0.88rem',
              cursor: 'pointer'
            }}
          >
            ⚡ Quick Personal Facts ({facts.length})
          </button>

          <button
            onClick={() => setActiveTab('api')}
            style={{
              flex: 1,
              padding: '12px',
              border: 'none',
              background: activeTab === 'api' ? 'rgba(99, 102, 241, 0.15)' : 'transparent',
              color: activeTab === 'api' ? '#a5b4fc' : '#94a3b8',
              borderBottom: activeTab === 'api' ? '2px solid #6366f1' : 'none',
              fontWeight: 600,
              fontSize: '0.88rem',
              cursor: 'pointer'
            }}
          >
            🔑 API Settings
          </button>
        </div>

        {/* Modal Body */}
        <div style={{ flex: 1, padding: '24px', overflowY: 'auto' }}>
          
          {/* TAB 1: Documents Upload & Management */}
          {activeTab === 'docs' && (
            <div>
              {/* File Uploader */}
              <div style={{
                border: '2px dashed rgba(99, 102, 241, 0.3)',
                borderRadius: '12px',
                padding: '24px',
                textAlign: 'center',
                background: 'rgba(99, 102, 241, 0.04)',
                marginBottom: '20px'
              }}>
                <Upload size={32} color="#a5b4fc" style={{ marginBottom: '8px' }} />
                <h4 style={{ margin: '0 0 4px 0', fontSize: '0.95rem' }}>Upload PDF, Resume, or Text File</h4>
                <p style={{ color: '#94a3b8', fontSize: '0.82rem', margin: '0 0 14px 0' }}>
                  Supports .pdf, .txt, and .md files to expand Luvkesh's RAG knowledge base.
                </p>
                <label className="btn-primary" style={{ cursor: 'pointer', display: 'inline-flex' }}>
                  <Upload size={14} />
                  <span>{uploading ? 'Processing & Indexing...' : 'Select File'}</span>
                  <input type="file" accept=".pdf,.txt,.md" onChange={handleFileUpload} disabled={uploading} style={{ display: 'none' }} />
                </label>
              </div>

              {uploadMessage && (
                <div style={{
                  padding: '10px 14px',
                  borderRadius: '8px',
                  marginBottom: '16px',
                  fontSize: '0.85rem',
                  display: 'flex',
                  alignItems: 'center',
                  gap: '8px',
                  background: uploadMessage.type === 'success' ? 'rgba(16, 185, 129, 0.15)' : 'rgba(239, 68, 68, 0.15)',
                  color: uploadMessage.type === 'success' ? '#34d399' : '#f87171'
                }}>
                  {uploadMessage.type === 'success' ? <Check size={16} /> : <AlertCircle size={16} />}
                  <span>{uploadMessage.text}</span>
                </div>
              )}

              {/* Indexed Files List */}
              <h4 style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '10px' }}>Currently Indexed Documents</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {documents.map((doc, idx) => (
                  <div key={idx} style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '12px 16px',
                    background: 'rgba(30, 41, 59, 0.6)',
                    borderRadius: '10px',
                    border: '1px solid rgba(255, 255, 255, 0.05)'
                  }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '10px' }}>
                      <FileText size={18} color="#818cf8" />
                      <div>
                        <div style={{ fontWeight: 500, fontSize: '0.9rem' }}>{doc.name}</div>
                        <div style={{ color: '#64748b', fontSize: '0.78rem' }}>{doc.chunks} vector chunk(s) indexed</div>
                      </div>
                    </div>
                    <button
                      onClick={() => handleDeleteDoc(doc.name)}
                      style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', padding: '6px' }}
                      title="Delete document"
                    >
                      <Trash2 size={16} />
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* TAB 2: Quick Facts Q&A Manager */}
          {activeTab === 'facts' && (
            <div>
              <form onSubmit={handleAddFact} style={{ display: 'flex', flexDirection: 'column', gap: '12px', marginBottom: '24px' }}>
                <div>
                  <label style={{ fontSize: '0.82rem', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Question / Fact Topic</label>
                  <input
                    type="text"
                    value={newQuestion}
                    onChange={(e) => setNewQuestion(e.target.value)}
                    placeholder="e.g. What is Luvkesh's favorite tech stack?"
                    style={{
                      width: '100%',
                      background: 'var(--bg-input)',
                      border: '1px solid var(--border-light)',
                      borderRadius: '8px',
                      padding: '10px 14px',
                      color: 'white',
                      fontSize: '0.9rem'
                    }}
                  />
                </div>

                <div>
                  <label style={{ fontSize: '0.82rem', color: '#94a3b8', display: 'block', marginBottom: '4px' }}>Fact Details / Answer</label>
                  <textarea
                    rows={3}
                    value={newAnswer}
                    onChange={(e) => setNewAnswer(e.target.value)}
                    placeholder="e.g. Luvkesh loves building RAG models with Python, FastAPI, Groq, and modern React interfaces..."
                    style={{
                      width: '100%',
                      background: 'var(--bg-input)',
                      border: '1px solid var(--border-light)',
                      borderRadius: '8px',
                      padding: '10px 14px',
                      color: 'white',
                      fontSize: '0.9rem',
                      fontFamily: 'inherit'
                    }}
                  />
                </div>

                <button type="submit" className="btn-primary" disabled={addingFact} style={{ alignSelf: 'flex-end' }}>
                  <Plus size={14} />
                  <span>Add Fact</span>
                </button>
              </form>

              <h4 style={{ fontSize: '0.9rem', color: '#94a3b8', marginBottom: '10px' }}>Custom Facts List</h4>
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                {facts.length === 0 ? (
                  <p style={{ color: '#64748b', fontSize: '0.85rem' }}>No custom facts added yet.</p>
                ) : (
                  facts.map((fact) => (
                    <div key={fact.id} style={{
                      padding: '12px 16px',
                      background: 'rgba(30, 41, 59, 0.6)',
                      borderRadius: '10px',
                      border: '1px solid rgba(255, 255, 255, 0.05)',
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'flex-start',
                      gap: '12px'
                    }}>
                      <div>
                        <div style={{ fontWeight: 600, color: '#a5b4fc', fontSize: '0.88rem' }}>Q: {fact.question}</div>
                        <div style={{ color: '#e2e8f0', fontSize: '0.85rem', marginTop: '4px' }}>{fact.answer}</div>
                      </div>
                      <button
                        onClick={() => handleDeleteFact(fact.id)}
                        style={{ background: 'none', border: 'none', color: '#ef4444', cursor: 'pointer', padding: '4px' }}
                      >
                        <Trash2 size={16} />
                      </button>
                    </div>
                  ))
                )}
              </div>
            </div>
          )}

          {/* TAB 3: API Settings */}
          {activeTab === 'api' && (
            <div>
              <div style={{ marginBottom: '16px' }}>
                <label style={{ fontSize: '0.85rem', color: '#94a3b8', display: 'block', marginBottom: '6px' }}>
                  Groq API Key (Optional Override)
                </label>
                <div style={{ display: 'flex', gap: '10px' }}>
                  <input
                    type="password"
                    value={keyInput}
                    onChange={(e) => setKeyInput(e.target.value)}
                    placeholder="Enter Groq API Key..."
                    style={{
                      flex: 1,
                      background: 'var(--bg-input)',
                      border: '1px solid var(--border-light)',
                      borderRadius: '8px',
                      padding: '10px 14px',
                      color: 'white',
                      fontSize: '0.9rem',
                      fontFamily: 'monospace'
                    }}
                  />
                  <button className="btn-primary" onClick={handleSaveApiKey}>
                    <Key size={14} />
                    <span>Save Key</span>
                  </button>
                </div>
                {keySaved && (
                  <p style={{ color: '#34d399', fontSize: '0.82rem', marginTop: '6px' }}>
                    ✓ API key saved to browser storage!
                  </p>
                )}
              </div>
              <p style={{ color: '#64748b', fontSize: '0.82rem', lineHeight: '1.4' }}>
                Note: A default Groq API key is pre-configured in the Python backend. Entering your own key here will override the default key for high-rate-limit inference.
              </p>
            </div>
          )}

        </div>

      </div>
    </div>
  );
}
