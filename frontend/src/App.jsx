import React, { useState, useEffect, useRef } from 'react';
import axios from 'axios';
import ReactMarkdown from 'react-markdown';
import {
  Send,
  Loader2,
  FolderGit2,
  Terminal,
  CheckCircle,
  AlertCircle
} from 'lucide-react';
import './App.css';

const API_BASE = 'http://localhost:8000';

function App() {
  const [repoUrl, setRepoUrl] = useState('');
  const [repoId, setRepoId] = useState('');
  const [status, setStatus] = useState('idle'); // idle, processing, completed, error
  const [messages, setMessages] = useState([]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef(null);

  // Auto-scroll to bottom of chat
  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  // Handle repo processing
  const handleProcessRepo = async () => {
    if (!repoUrl) return;
    setStatus('processing');
    setMessages([]);
    try {
      const response = await axios.post(`${API_BASE}/api/process`, { repo_url: repoUrl });
      setRepoId(response.data.repo_id);
    } catch (err) {
      setStatus('error');
      console.error(err);
    }
  };

  // Poll status
  useEffect(() => {
    let interval;
    if (status === 'processing' && repoId) {
      interval = setInterval(async () => {
        try {
          const response = await axios.get(`${API_BASE}/api/status/${repoId}`);
          if (response.data.status === 'completed') {
            setStatus('completed');
            clearInterval(interval);
          } else if (response.data.status.startsWith('failed')) {
            setStatus('error');
            clearInterval(interval);
          }
        } catch (err) {
          console.error(err);
        }
      }, 2000);
    }
    return () => clearInterval(interval);
  }, [status, repoId]);

  // Handle sending questions
  const handleSendQuery = async () => {
    if (!inputValue || status !== 'completed' || isLoading) return;

    const userMsg = { role: 'user', content: inputValue };
    setMessages(prev => [...prev, userMsg]);
    setInputValue('');
    setIsLoading(true);

    try {
      const response = await axios.post(`${API_BASE}/api/query`, {
        question: inputValue,
        repo_id: repoId
      });

      const aiMsg = {
        role: 'ai',
        content: response.data.answer,
        sources: response.data.sources
      };
      setMessages(prev => [...prev, aiMsg]);
    } catch (err) {
      setMessages(prev => [...prev, { role: 'ai', content: "Error communicating with intelligence server." }]);
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div className="chat-layout">
      {/* Sidebar */}
      <aside className="sidebar">
        <div className="sidebar-header">
          <FolderGit2 size={24} />
          <span>ASK Git</span>
        </div>

        <div className="repo-input-group">
          <label style={{ fontSize: '0.75rem', opacity: 0.6 }}>GitHub Repository URL</label>
          <input
            className="repo-input"
            placeholder="https://github.com/..."
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            disabled={status === 'processing'}
            onKeyPress={(e) => e.key === 'Enter' && handleProcessRepo()}
          />
          <button
            className="repo-btn"
            onClick={handleProcessRepo}
            disabled={status === 'processing'}
          >
            {status === 'processing' ? 'Indexing...' : 'Submit'}
          </button>
        </div>

        {status !== 'idle' && (
          <div className="status-indicator">
            {status === 'processing' && <><Loader2 size={14} className="spinner" /> <span>Analyzing codebase...</span></>}
            {status === 'completed' && <><CheckCircle size={14} color="#22c55e" /> <span style={{ color: '#22c55e' }}>Completed</span></>}
            {status === 'error' && <><AlertCircle size={14} color="#ef4444" /> <span style={{ color: '#ef4444' }}>Processing Failed</span></>}
          </div>
        )}

        <div style={{ flex: 1 }}></div>
        <div style={{ fontSize: '0.7rem', opacity: 0.4 }}>Powered by OpenAI & LangChain</div>
      </aside>

      {/* Main Chat Area */}
      <main className="chat-container">
        <div className="messages">
          {messages.length === 0 && (
            <div style={{ height: '70%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center', opacity: 0.5 }}>
              <Terminal size={48} style={{ marginBottom: '1rem' }} />
              <h2 style={{ margin: 0 }}>Start a conversation</h2>
              <p>Index a repository to ask technical questions.</p>
            </div>
          )}

          {messages.map((msg, idx) => (
            <div key={idx} className="message-row">
              <div className={`avatar ${msg.role}`}>
                {msg.role === 'user' ? 'U' : 'AI'}
              </div>
              <div className="message-content">
                <ReactMarkdown>{msg.content}</ReactMarkdown>
                {msg.sources && msg.sources.length > 0 && (
                  <div style={{ marginTop: '1rem', borderTop: '1px solid rgba(255,255,255,0.05)', paddingTop: '0.5rem' }}>
                    <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginTop: '0.5rem' }}>
                      {msg.sources.map((src, i) => (
                        <span key={i} title={src} style={{ fontSize: '0.65rem', background: 'rgba(255,255,255,0.05)', padding: '2px 6px', borderRadius: '4px', opacity: 0.6, cursor: 'help' }}>
                          {src.split(/[\\/]/).pop()}
                        </span>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="message-row">
              <div className="avatar ai">AI</div>
              <div className="message-content"><Loader2 size={16} className="spinner" /></div>
            </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar */}
        <div className="input-area">
          <div className="input-wrapper">
            <textarea
              className="chat-input"
              rows={1}
              placeholder="Ask anything about the codebase..."
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter' && !e.shiftKey) {
                  e.preventDefault();
                  handleSendQuery();
                }
              }}
              disabled={status !== 'completed' || isLoading}
            />
            <button
              className="send-btn"
              onClick={handleSendQuery}
              disabled={status !== 'completed' || isLoading || !inputValue}
            >
              <Send size={18} />
            </button>
          </div>
          <p style={{ textAlign: 'center', fontSize: '0.7rem', opacity: 0.3, marginTop: '0.75rem' }}>
            RAG Assistant may produce inaccuracies. Focus on verified grounding sources.
          </p>
        </div>
      </main>
    </div>
  );
}

export default App;
