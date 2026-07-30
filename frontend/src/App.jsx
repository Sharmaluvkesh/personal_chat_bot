import React, { useState, useEffect } from 'react';
import PersonaHeader from './components/PersonaHeader';
import ChatWindow from './components/ChatWindow';
import KnowledgeManager from './components/KnowledgeManager';
import { Code2, Cpu, GraduationCap, Github, Linkedin, Mail, Heart, Sparkles } from 'lucide-react';

export default function App() {
  const [apiKey, setApiKey] = useState(localStorage.getItem('groq_api_key') || '');
  const [isKnowledgeOpen, setIsKnowledgeOpen] = useState(false);
  const [stats, setStats] = useState(null);

  const fetchStats = async () => {
    try {
      const res = await fetch('/api/health');
      if (res.ok) {
        const data = await res.json();
        setStats(data);
      }
    } catch (err) {
      console.log("Health check error:", err);
    }
  };

  useEffect(() => {
    fetchStats();
  }, []);

  return (
    <div style={{ maxWidth: '1200px', margin: '0 auto', padding: '24px 16px', minHeight: '100vh', display: 'flex', flexDirection: 'column' }}>
      
      {/* Header Banner */}
      <PersonaHeader
        onOpenKnowledgeManager={() => setIsKnowledgeOpen(true)}
        stats={stats}
      />

      {/* Main Grid Section */}
      <div style={{ display: 'grid', gridTemplateColumns: 'minmax(0, 1fr) 340px', gap: '24px', flex: 1 }}>
        
        {/* Left Column: Primary RAG Chatbot Interface */}
        <div>
          <ChatWindow
            apiKey={apiKey}
            onAsk={() => {}}
          />
        </div>

        {/* Right Column: Persona Profile Highlights Cards */}
        <div style={{ display: 'flex', flexDirection: 'column', gap: '20px' }}>
          
          {/* Card 1: Core Expertise */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px', color: '#818cf8' }}>
              <Cpu size={18} />
              <h3 style={{ fontSize: '1.05rem', margin: 0 }}>Core Specializations</h3>
            </div>
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: '6px' }}>
              {['RAG Architecture', 'LLM Prompt Engineering', 'FastAPI & Python', 'React & Vite', 'LangChain', 'FAISS Vector Search', 'Groq & Llama-3.3', 'Full Stack AI Apps'].map((skill, idx) => (
                <span key={idx} className="pill-badge" style={{ fontSize: '0.78rem' }}>
                  {skill}
                </span>
              ))}
            </div>
          </div>

          {/* Card 2: Contact & Social Links */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '14px', color: '#c084fc' }}>
              <Code2 size={18} />
              <h3 style={{ fontSize: '1.05rem', margin: 0 }}>Connect with Luvkesh</h3>
            </div>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '10px' }}>
              <a
                href="https://github.com/sharmaluvkesh"
                target="_blank"
                rel="noreferrer"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  color: '#e2e8f0',
                  textDecoration: 'none',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  background: 'rgba(30, 41, 59, 0.5)',
                  fontSize: '0.88rem',
                  transition: 'background 0.2s ease'
                }}
              >
                <Github size={16} color="#a5b4fc" />
                <span>GitHub (@sharmaluvkesh)</span>
              </a>

              <a
                href="https://www.linkedin.com/in/luvkesh-sharma"
                target="_blank"
                rel="noreferrer"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  color: '#e2e8f0',
                  textDecoration: 'none',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  background: 'rgba(30, 41, 59, 0.5)',
                  fontSize: '0.88rem',
                  transition: 'background 0.2s ease'
                }}
              >
                <Linkedin size={16} color="#a5b4fc" />
                <span>LinkedIn Profile</span>
              </a>

              <a
                href="mailto:lksharma18102005@gmail.com"
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '10px',
                  color: '#e2e8f0',
                  textDecoration: 'none',
                  padding: '8px 12px',
                  borderRadius: '8px',
                  background: 'rgba(30, 41, 59, 0.5)',
                  fontSize: '0.88rem',
                  transition: 'background 0.2s ease'
                }}
              >
                <Mail size={16} color="#a5b4fc" />
                <span>lksharma18102005@gmail.com</span>
              </a>
            </div>
          </div>

          {/* Card 3: RAG Engine Features */}
          <div className="glass-card" style={{ padding: '20px' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '10px', color: '#10b981' }}>
              <Sparkles size={18} />
              <h3 style={{ fontSize: '1.05rem', margin: 0 }}>RAG System Highlights</h3>
            </div>
            <ul style={{ color: '#94a3b8', fontSize: '0.82rem', paddingLeft: '18px', margin: 0, lineHeight: '1.6' }}>
              <li>Page-level source citation tracking</li>
              <li>Real-time PDF/TXT vector indexing</li>
              <li>Groq Llama-3.3 ultra-fast inference</li>
              <li>Speech input & Voice readout options</li>
            </ul>
          </div>

        </div>

      </div>

      {/* Footer */}
      <footer style={{
        marginTop: '32px',
        paddingTop: '16px',
        borderTop: '1px solid rgba(255, 255, 255, 0.05)',
        textAlign: 'center',
        color: '#64748b',
        fontSize: '0.82rem',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        gap: '6px'
      }}>
        <span>Built with</span>
        <Heart size={14} color="#ec4899" fill="#ec4899" />
        <span>for Luvkesh Sharma • Powered by FastAPI & Groq LLM</span>
      </footer>

      {/* Knowledge Base Modal */}
      <KnowledgeManager
        isOpen={isKnowledgeOpen}
        onClose={() => setIsKnowledgeOpen(false)}
        apiKey={apiKey}
        setApiKey={setApiKey}
        onRefreshStats={fetchStats}
      />

    </div>
  );
}
