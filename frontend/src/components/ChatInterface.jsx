import React, { useState, useRef, useEffect } from 'react';
import '../styles/components.css';

const ChatInterface = ({ onQuery }) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input.trim();
    setInput('');
    setMessages(prev => [...prev, { type: 'user', text: userMessage }]);
    setLoading(true);

    try {
      const response = await fetch('http://localhost:8000/query', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ question: userMessage }),
      });

      const result = await response.json();
      setMessages(prev => [...prev, {
        type: 'assistant',
        text: result.answer,
        success: result.success
      }]);

      if (onQuery) onQuery(result);
    } catch (error) {
      setMessages(prev => [...prev, {
        type: 'error',
        text: 'Error: ' + error.message
      }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="chat-container">
      <h2>💬 Equity Insights Chat</h2>
      <div className="chat-messages">
        {messages.length === 0 && (
          <div className="empty-state">
            <p>🤖 Ask questions about your cap table:</p>
            <ul>
              <li>"Who owns the most equity?"</li>
              <li>"What's the dilution after 1000 new shares?"</li>
              <li>"Show ESOP allocation summary"</li>
              <li>"Rank shareholders by percentage"</li>
            </ul>
          </div>
        )}
        {messages.map((msg, idx) => (
          <div key={idx} className={`message message-${msg.type}`}>
            <span className="message-icon">
              {msg.type === 'user' ? '👤' : msg.type === 'error' ? '❌' : '🤖'}
            </span>
            <div className="message-content">{msg.text}</div>
          </div>
        ))}
        {loading && (
          <div className="message message-loading">
            <span className="message-icon">⏳</span>
            <div className="message-content">Processing...</div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={handleSendMessage} className="chat-form">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask about your equity..."
          disabled={loading}
          className="chat-input"
        />
        <button type="submit" disabled={loading} className="btn btn-send">
          {loading ? '⏳' : '➤'}
        </button>
      </form>
    </div>
  );
};

export default ChatInterface;
