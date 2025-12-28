import React, { useState, useEffect } from 'react';
import styles from './Chatbot.module.css';

const Chatbot = () => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState([
    { id: 1, text: "Hello! I'm your RAG-powered chatbot. How can I help you with the book content today?", sender: 'bot' }
  ]);
  const [inputValue, setInputValue] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [selectedText, setSelectedText] = useState(null);

  // Function to handle text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const selectedTextContent = selection.toString().trim();

      // Only update if it's a meaningful selection (not just clicking around)
      if (selectedTextContent && selectedTextContent.length > 0) {
        setSelectedText(selectedTextContent);
      }
    };

    document.addEventListener('mouseup', handleSelection);
    return () => {
      document.removeEventListener('mouseup', handleSelection);
    };
  }, []);

  const toggleChat = () => {
    setIsOpen(!isOpen);
  };

  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      // Use the selected text if available
      const textToUse = selectedText || inputValue;

      // Determine the API base URL based on environment
      let API_BASE_URL = 'http://localhost:8001'; // Default to port 8001 where our backend runs

      // Check for environment variables
      if (typeof window !== 'undefined') {
        if (process.env.REACT_APP_API_BASE_URL) {
          API_BASE_URL = process.env.REACT_APP_API_BASE_URL;
        } else if (window.ENV?.REACT_APP_API_BASE_URL) {
          API_BASE_URL = window.ENV?.REACT_APP_API_BASE_URL;
        } else {
          // Check if we're on a deployed site vs localhost
          const currentOrigin = window.location.origin;
          if (currentOrigin.includes('localhost') || currentOrigin.includes('127.0.0.1')) {
            // Local development - default to our backend port
            API_BASE_URL = 'http://localhost:8001';
          } else {
            // Deployed site - use relative path to match the same origin
            API_BASE_URL = '';
          }
        }
      }

      // Construct the full URL
      const fullUrl = API_BASE_URL ? `${API_BASE_URL}/chat` : '/chat';

      const response = await fetch(fullUrl, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          query: inputValue,
          selected_text: selectedText || '',
          conversation_history: messages.filter(m => m.sender === 'user' || m.sender === 'bot').map(m => ({
            role: m.sender === 'user' ? 'user' : 'assistant',
            content: m.text
          })),
          top_k: 5,
          session_id: null
        })
      });

      if (!response.ok) {
        throw new Error(`Server error: ${response.status} ${response.statusText}`);
      }

      const data = await response.json();

      const botMessage = {
        id: Date.now() + 1,
        text: data.response + (data.confidence ? `\n\n*Confidence: ${(data.confidence * 100).toFixed(1)}%*` : '') +
              (data.sources && data.sources.length > 0 ? `\n\n*Sources:*\n${data.sources.slice(0, 3).map(s => `- ${s.title || 'Unknown source'} ${s.url ? `(${s.url})` : ''}`).join('\n')}` : ''),
        sender: 'bot'
      };

      setMessages(prev => [...prev, botMessage]);

      // Clear selected text after sending
      setSelectedText(null);
    } catch (error) {
      const errorMessage = {
        id: Date.now() + 1,
        text: "Sorry, I'm having trouble connecting to the server. Please make sure the backend is running.",
        sender: 'bot'
      };
      setMessages(prev => [...prev, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className={styles.chatbotContainer}>
      {isOpen ? (
        <div className={styles.chatWindow}>
          <div className={styles.chatHeader}>
            <div className={styles.chatTitle}>Book Assistant</div>
            <button
              className={styles.closeButton}
              onClick={toggleChat}
              aria-label="Close chat"
            >
              ×
            </button>
          </div>
          <div className={styles.chatMessages}>
            {messages.map((message) => (
              <div
                key={message.id}
                className={`${styles.message} ${
                  message.sender === 'user' ? styles.userMessage : styles.botMessage
                }`}
              >
                {message.text}
              </div>
            ))}
            {isLoading && (
              <div className={styles.message + ' ' + styles.botMessage}>
                <div className={styles.typingIndicator}>
                  <div></div>
                  <div></div>
                  <div></div>
                </div>
              </div>
            )}
          </div>
          {selectedText && (
            <div className={styles.selectedTextNotice}>
              Selected text: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
            </div>
          )}
          <div className={styles.chatInputArea}>
            <textarea
              value={inputValue}
              onChange={(e) => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the book content..."
              className={styles.chatInput}
              rows="2"
            />
            <button
              onClick={sendMessage}
              disabled={isLoading || !inputValue.trim()}
              className={styles.sendButton}
            >
              Send
            </button>
          </div>
        </div>
      ) : (
        <button
          className={styles.floatingButton}
          onClick={toggleChat}
          aria-label="Open chat"
        >
          💬
        </button>
      )}
    </div>
  );
};

export default Chatbot;