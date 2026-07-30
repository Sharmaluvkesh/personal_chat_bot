import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import { Send, Bot, User, Sparkles, Copy, Check, BookOpen, Mic, MicOff, Volume2, RefreshCw, ChevronDown, ChevronUp } from 'lucide-react';

const SUGGESTED_QUESTIONS = [
  "What are Luvkesh's top technical skills?",
  "Tell me about the projects Luvkesh has built.",
  "What is Luvkesh's educational background?",
  "How can I contact Luvkesh for a project or role?"
];

const INITIAL_WELCOME_MSG = {
  id: 'welcome',
  role: 'assistant',
  content: "👋 **Hi there! I am Luvkesh Sharma's official AI Assistant.**\n\nAsk me anything about Luvkesh's technical skills, software projects, background, resume details, or how to contact him!",
  citations: []
};

export default function ChatWindow({ apiKey, onAsk }) {
  const [messages, setMessages] = useState(() => {
    try {
      const saved = localStorage.getItem('chat_messages');
      return saved ? JSON.parse(saved) : [INITIAL_WELCOME_MSG];
    } catch {
      return [INITIAL_WELCOME_MSG];
    }
  });

  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [copiedId, setCopiedId] = useState(null);
  const [isListening, setIsListening] = useState(false);
  const [expandedCitations, setExpandedCitations] = useState({});

  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
    try {
      localStorage.setItem('chat_messages', JSON.stringify(messages));
    } catch (e) {
      console.error("Error saving chat memory:", e);
    }
  }, [messages, loading]);

  const handleSend = async (questionText) => {
    const query = questionText || input.trim();
    if (!query || loading) return;

    const userMsg = {
      id: Date.now().toString(),
      role: 'user',
      content: query
    };

    setMessages(prev => [...prev, userMsg]);
    if (!questionText) setInput('');
    setLoading(true);

    try {
      // Build recent conversation history for RAG memory
      const history = messages
        .filter(m => m.id !== 'welcome')
        .slice(-6)
        .map(m => ({ role: m.role, content: m.content }));

      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          question: query,
          api_key: apiKey || null,
          history: history
        })
      });

      if (!res.ok) {
        throw new Error(`Server status ${res.status}`);
      }

      const data = await res.json();
      const botMsg = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: data.answer || "I retrieved information but couldn't generate a response.",
        citations: data.citations || []
      };

      setMessages(prev => [...prev, botMsg]);
    } catch (err) {
      console.error("Chat error:", err);
      const errorMsg = {
        id: (Date.now() + 1).toString(),
        role: 'assistant',
        content: "⚠️ **Unable to connect to the backend server.** Please make sure the Python FastAPI backend is running on `http://localhost:8000`.",
        citations: []
      };
      setMessages(prev => [...prev, errorMsg]);
    } finally {
      setLoading(false);
    }
  };

  const handleCopy = (id, text) => {
    navigator.clipboard.writeText(text);
    setCopiedId(id);
    setTimeout(() => setCopiedId(null), 2000);
  };

  const handleSpeak = (text) => {
    if ('speechSynthesis' in window) {
      window.speechSynthesis.cancel();
      const utterance = new SpeechSynthesisUtterance(text.replace(/[*_#`]/g, ''));
      utterance.rate = 1.0;
      window.speechSynthesis.speak(utterance);
    }
  };

  const toggleSpeechInput = () => {
    if (!('webkitSpeechRecognition' in window || 'SpeechRecognition' in window)) {
      alert("Speech recognition is not supported in your browser.");
      return;
    }

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    const recognition = new SpeechRecognition();

    if (isListening) {
      setIsListening(false);
      return;
    }

    recognition.continuous = false;
    recognition.interimResults = false;
    recognition.lang = 'en-US';

    recognition.onstart = () => setIsListening(true);
    recognition.onend = () => setIsListening(false);
    recognition.onresult = (event) => {
      const transcript = event.results[0][0].transcript;
      setInput(transcript);
      handleSend(transcript);
    };

    recognition.start();
  };

  const toggleCitation = (msgId) => {
    setExpandedCitations(prev => ({
      ...prev,
      [msgId]: !prev[msgId]
    }));
  };

  const handleResetChat = () => {
    localStorage.removeItem('chat_messages');
    setMessages([INITIAL_WELCOME_MSG]);
  };

  return (
    <div className="glass-card" style={{ display: 'flex', flexDirection: 'column', height: '640px', overflow: 'hidden' }}>
      
      {/* Top Header / Bar */}
      <div style={{
        padding: '14px 20px',
        borderBottom: '1px solid rgba(255, 255, 255, 0.08)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'rgba(15, 23, 42, 0.4)'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
          <Sparkles size={18} color="#818cf8" />
          <span style={{ fontWeight: 600, fontSize: '0.95rem' }}>Ask AI Luvkesh</span>
        </div>
        <button
          className="btn-secondary"
          onClick={handleResetChat}
          style={{ padding: '4px 10px', fontSize: '0.8rem' }}
          title="Clear & Reset Conversation Memory"
        >
          <RefreshCw size={12} /> Clear Memory
        </button>
      </div>

      {/* Messages Scroll Area */}
      <div style={{ flex: 1, padding: '20px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '16px' }}>
        
        {messages.map((msg) => (
          <div key={msg.id} className="animate-fade-in" style={{
            display: 'flex',
            gap: '12px',
            flexDirection: msg.role === 'user' ? 'row-reverse' : 'row',
            alignItems: 'flex-start'
          }}>
            {/* Avatar Icon */}
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: msg.role === 'user' 
                ? 'linear-gradient(135deg, #06b6d4, #3b82f6)' 
                : 'linear-gradient(135deg, #6366f1, #a855f7)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0,
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)'
            }}>
              {msg.role === 'user' ? <User size={18} color="#fff" /> : <Bot size={18} color="#fff" />}
            </div>

            {/* Bubble */}
            <div style={{
              maxWidth: '80%',
              background: msg.role === 'user' ? 'rgba(99, 102, 241, 0.2)' : 'rgba(30, 41, 59, 0.7)',
              border: msg.role === 'user' ? '1px solid rgba(99, 102, 241, 0.35)' : '1px solid rgba(255, 255, 255, 0.08)',
              borderRadius: msg.role === 'user' ? '18px 18px 4px 18px' : '18px 18px 18px 4px',
              padding: '14px 18px',
              fontSize: '0.92rem',
              lineHeight: '1.5',
              position: 'relative'
            }}>
              <ReactMarkdown remarkPlugins={[remarkGfm]}>
                {msg.content}
              </ReactMarkdown>

              {/* Bot Message Utilities & Citations */}
              {msg.role === 'assistant' && (
                <div style={{ marginTop: '12px', paddingTop: '8px', borderTop: '1px solid rgba(255, 255, 255, 0.05)', display: 'flex', flexWrap: 'wrap', alignItems: 'center', justifyContent: 'space-between', gap: '8px' }}>
                  
                  {/* Citations Pill Toggle */}
                  {msg.citations && msg.citations.length > 0 ? (
                    <button
                      onClick={() => toggleCitation(msg.id)}
                      style={{
                        background: 'rgba(99, 102, 241, 0.1)',
                        border: '1px solid rgba(99, 102, 241, 0.2)',
                        color: '#a5b4fc',
                        borderRadius: '6px',
                        padding: '3px 8px',
                        fontSize: '0.75rem',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '4px'
                      }}
                    >
                      <BookOpen size={12} />
                      <span>{msg.citations.length} Source Citation(s)</span>
                      {expandedCitations[msg.id] ? <ChevronUp size={12} /> : <ChevronDown size={12} />}
                    </button>
                  ) : <div />}

                  {/* Actions: Copy & TTS */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
                    <button
                      onClick={() => handleSpeak(msg.content)}
                      style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}
                      title="Read Aloud"
                    >
                      <Volume2 size={14} />
                    </button>
                    <button
                      onClick={() => handleCopy(msg.id, msg.content)}
                      style={{ background: 'none', border: 'none', color: '#94a3b8', cursor: 'pointer', padding: '4px' }}
                      title="Copy response"
                    >
                      {copiedId === msg.id ? <Check size={14} color="#10b981" /> : <Copy size={14} />}
                    </button>
                  </div>

                </div>
              )}

              {/* Expanded Citations Panel */}
              {msg.role === 'assistant' && expandedCitations[msg.id] && msg.citations && (
                <div style={{
                  marginTop: '10px',
                  padding: '10px',
                  background: 'rgba(15, 23, 42, 0.9)',
                  borderRadius: '8px',
                  border: '1px solid rgba(99, 102, 241, 0.2)',
                  fontSize: '0.8rem'
                }}>
                  <div style={{ fontWeight: 600, color: '#c084fc', marginBottom: '6px' }}>Verified Knowledge Sources:</div>
                  {msg.citations.map((c, i) => (
                    <div key={i} style={{ marginBottom: '6px', paddingBottom: '6px', borderBottom: i < msg.citations.length - 1 ? '1px solid rgba(255,255,255,0.05)' : 'none' }}>
                      <span style={{ color: '#818cf8', fontWeight: 500 }}>📄 {c.source}</span> {c.page ? `(Page ${c.page})` : ''}
                      <p style={{ color: '#94a3b8', fontStyle: 'italic', margin: '2px 0 0 0', fontSize: '0.78rem' }}>"{c.snippet}"</p>
                    </div>
                  ))}
                </div>
              )}

            </div>
          </div>
        ))}

        {/* Loading Indicator */}
        {loading && (
          <div className="animate-fade-in" style={{ display: 'flex', gap: '12px', alignItems: 'center' }}>
            <div style={{
              width: '36px',
              height: '36px',
              borderRadius: '50%',
              background: 'linear-gradient(135deg, #6366f1, #a855f7)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              flexShrink: 0
            }}>
              <Bot size={18} color="#fff" />
            </div>
            <div style={{ background: 'rgba(30, 41, 59, 0.7)', borderRadius: '16px', padding: '12px 18px' }}>
              <div className="typing-indicator">
                <div className="typing-dot" />
                <div className="typing-dot" />
                <div className="typing-dot" />
              </div>
            </div>
          </div>
        )}

        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Questions Pills */}
      <div style={{
        padding: '8px 16px',
        borderTop: '1px solid rgba(255, 255, 255, 0.05)',
        background: 'rgba(15, 23, 42, 0.3)',
        display: 'flex',
        gap: '8px',
        overflowX: 'auto',
        whiteSpace: 'nowrap'
      }}>
        {SUGGESTED_QUESTIONS.map((q, idx) => (
          <button
            key={idx}
            onClick={() => handleSend(q)}
            disabled={loading}
            style={{
              background: 'rgba(99, 102, 241, 0.1)',
              border: '1px solid rgba(99, 102, 241, 0.2)',
              color: '#c7d2fe',
              padding: '4px 12px',
              borderRadius: '16px',
              fontSize: '0.78rem',
              cursor: 'pointer',
              transition: 'all 0.2s ease',
              flexShrink: 0
            }}
          >
            {q}
          </button>
        ))}
      </div>

      {/* Input Form Box */}
      <form
        onSubmit={(e) => { e.preventDefault(); handleSend(); }}
        style={{
          padding: '16px',
          borderTop: '1px solid rgba(255, 255, 255, 0.08)',
          background: 'rgba(15, 23, 42, 0.8)',
          display: 'flex',
          gap: '10px',
          alignItems: 'center'
        }}
      >
        <button
          type="button"
          onClick={toggleSpeechInput}
          style={{
            background: isListening ? '#ef4444' : 'rgba(30, 41, 59, 0.8)',
            border: '1px solid rgba(255, 255, 255, 0.1)',
            color: 'white',
            borderRadius: '12px',
            width: '42px',
            height: '42px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            cursor: 'pointer',
            flexShrink: 0
          }}
          title={isListening ? "Stop voice input" : "Voice input"}
        >
          {isListening ? <MicOff size={18} /> : <Mic size={18} />}
        </button>

        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask anything about Luvkesh (skills, projects, experience)..."
          disabled={loading}
          style={{
            flex: 1,
            background: 'var(--bg-input)',
            border: '1px solid var(--border-light)',
            borderRadius: '12px',
            padding: '12px 16px',
            color: 'white',
            fontSize: '0.95rem',
            outline: 'none',
            transition: 'border-color 0.2s ease'
          }}
        />

        <button
          type="submit"
          className="btn-primary"
          disabled={loading || !input.trim()}
          style={{ height: '42px', padding: '0 18px', flexShrink: 0 }}
        >
          <Send size={16} />
          <span>Send</span>
        </button>
      </form>

    </div>
  );
}
