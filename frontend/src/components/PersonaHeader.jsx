import React from 'react';
import { Bot, Sparkles, FolderKanban, Github, Linkedin, Mail, Settings, Database, BrainCircuit } from 'lucide-react';

export default function PersonaHeader({ onOpenKnowledgeManager, stats }) {
  return (
    <header className="glass-card" style={{ padding: '24px', marginBottom: '24px' }}>
      <div style={{ display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '20px' }}>
        
        {/* Left Column: Avatar & Bio */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '16px', minWidth: '280px' }}>
          <div style={{
            position: 'relative',
            width: '64px',
            height: '64px',
            borderRadius: '50%',
            background: 'linear-gradient(135deg, #6366f1, #a855f7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            boxShadow: '0 0 20px rgba(99, 102, 241, 0.4)',
            flexShrink: 0
          }}>
            <Bot size={36} color="#ffffff" />
            <div style={{
              position: 'absolute',
              bottom: '2px',
              right: '2px',
              width: '14px',
              height: '14px',
              borderRadius: '50%',
              backgroundColor: '#10b981',
              border: '2px solid #090d16',
              boxShadow: '0 0 8px #10b981'
            }} />
          </div>

          <div>
            <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
              <h1 style={{ fontSize: '1.4rem', margin: 0 }}>
                Luvkesh <span className="gradient-text">AI Persona</span>
              </h1>
              <span className="pill-badge">
                <Sparkles size={12} /> RAG v1.0
              </span>
            </div>
            <p style={{ color: '#94a3b8', fontSize: '0.9rem', margin: 0 }}>
              AI Assistant trained on Luvkesh's resume, skills, projects, and personal knowledge base.
            </p>
          </div>
        </div>

        {/* Right Column: Stats & Action Buttons */}
        <div style={{ display: 'flex', alignItems: 'center', flexWrap: 'wrap', gap: '12px' }}>
          
          <div style={{
            display: 'flex',
            alignItems: 'center',
            gap: '12px',
            padding: '8px 16px',
            background: 'rgba(15, 23, 42, 0.6)',
            borderRadius: '12px',
            border: '1px solid rgba(255, 255, 255, 0.05)',
            fontSize: '0.85rem'
          }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#a5b4fc' }}>
              <Database size={14} />
              <span>Docs: <strong>{stats?.knowledge_base_files ?? 3}</strong></span>
            </div>
            <div style={{ width: '1px', height: '14px', background: 'rgba(255, 255, 255, 0.1)' }} />
            <div style={{ display: 'flex', alignItems: 'center', gap: '6px', color: '#c084fc' }}>
              <BrainCircuit size={14} />
              <span>Model: <strong>Groq Llama-3.3</strong></span>
            </div>
          </div>

          <button className="btn-secondary" onClick={onOpenKnowledgeManager} title="Manage Knowledge Base & Documents">
            <Settings size={16} />
            <span>Manage Knowledge</span>
          </button>
        </div>

      </div>
    </header>
  );
}
