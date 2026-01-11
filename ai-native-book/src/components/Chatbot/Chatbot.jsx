// export default Chatbot;

// import React, { useState, useEffect } from 'react';
// import styles from './Chatbot.module.css';

// const Chatbot = () => {
//   const [isOpen, setIsOpen] = useState(false);
//   const [messages, setMessages] = useState([
//     { id: 1, text: "Hello! I'm your RAG-powered chatbot. How can I help you with the book content today?", sender: 'bot' }
//   ]);
//   const [inputValue, setInputValue] = useState('');
//   const [isLoading, setIsLoading] = useState(false);
//   const [selectedText, setSelectedText] = useState(null);

//   // Track text selection
//   useEffect(() => {
//     const handleSelection = () => {
//       const selection = window.getSelection();
//       const text = selection.toString().trim();
//       setSelectedText(text.length > 0 ? text : null);
//     };
//     document.addEventListener('mouseup', handleSelection);
//     return () => document.removeEventListener('mouseup', handleSelection);
//   }, []);

//   // Toggle chat window
//   const toggleChat = () => setIsOpen(prev => !prev);

//   // Send message to backend
//   const sendMessage = async () => {
//     if (!inputValue.trim()) return;

//     const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
//     setMessages(prev => [...prev, userMessage]);
//     setInputValue('');
//     setIsLoading(true);

//     try {
//       const textToUse = selectedText || inputValue;

//       // CRA environment variable or fallback URL
//       const API_BASE_URL = process.env.REACT_APP_BACKEND_URL || 'https://book-1-3piy.onrender.com';
//       const fullUrl = `${API_BASE_URL}/chat`;

//       // POST request
//       const response = await fetch(fullUrl, {
//         method: 'POST',
//         headers: { 'Content-Type': 'application/json' },
//         body: JSON.stringify({
//           query: textToUse,
//           selected_text: selectedText || '',
//           top_k: 5,
//         })
//       });

//       if (!response.ok) throw new Error(`Server error: ${response.status}`);

//       const data = await response.json();
//       console.log("Backend /chat response:", data);

//       // Build bot message
//       let botText = data.response || "Sorry, I didn't get a response.";
//       if (data.confidence) botText += `\n\n*Confidence: ${(data.confidence * 100).toFixed(1)}%*`;
//       if (data.sources && data.sources.length) {
//         botText += `\n\n*Sources:*\n${data.sources
//           .slice(0, 3)
//           .map(s => `- ${s.title || 'Unknown'}${s.url ? ` (${s.url})` : ''}`)
//           .join('\n')}`;
//       }

//       const botMessage = { id: Date.now() + 1, sender: 'bot', text: botText };
//       setMessages(prev => [...prev, botMessage]);
//       setSelectedText(null);
//     } catch (err) {
//       console.error(err);
//       setMessages(prev => [
//         ...prev,
//         { id: Date.now() + 1, sender: 'bot', text: "Sorry, I'm having trouble connecting to the server." }
//       ]);
//     } finally {
//       setIsLoading(false);
//     }
//   };

//   // Handle Enter key
//   const handleKeyPress = e => {
//     if (e.key === 'Enter' && !e.shiftKey) {
//       e.preventDefault();
//       sendMessage();
//     }
//   };

//   return (
//     <div className={styles.chatbotContainer}>
//       {isOpen ? (
//         <div className={styles.chatWindow}>
//           <div className={styles.chatHeader}>
//             <div className={styles.chatTitle}>Book Assistant</div>
//             <button className={styles.closeButton} onClick={toggleChat} aria-label="Close chat">
//               ×
//             </button>
//           </div>

//           <div className={styles.chatMessages}>
//             {messages.map(msg => (
//               <div key={msg.id} className={`${styles.message} ${msg.sender === 'user' ? styles.userMessage : styles.botMessage}`}>
//                 {msg.text.split('\n').map((line, i) => <div key={i}>{line}</div>)}
//               </div>
//             ))}

//             {isLoading && (
//               <div className={`${styles.message} ${styles.botMessage}`}>
//                 <div className={styles.typingIndicator}><div></div><div></div><div></div></div>
//               </div>
//             )}
//           </div>

//           {selectedText && (
//             <div className={styles.selectedTextNotice}>
//               Selected text: "{selectedText.substring(0, 100)}{selectedText.length > 100 ? '...' : ''}"
//             </div>
//           )}

//           <div className={styles.chatInputArea}>
//             <textarea
//               value={inputValue}
//               onChange={e => setInputValue(e.target.value)}
//               onKeyPress={handleKeyPress}
//               placeholder="Ask about the book content..."
//               className={styles.chatInput}
//               rows={2}
//             />
//             <button onClick={sendMessage} disabled={isLoading || !inputValue.trim()} className={styles.sendButton}>
//               Send
//             </button>
//           </div>
//         </div>
//       ) : (
//         <button className={styles.floatingButton} onClick={toggleChat} aria-label="Open chat">
//           💬
//         </button>
//       )}
//     </div>
//   );
// };

// export default Chatbot;

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

  // Track text selection
  useEffect(() => {
    const handleSelection = () => {
      const selection = window.getSelection();
      const text = selection.toString().trim();
      setSelectedText(text.length > 0 ? text : null);
    };
    document.addEventListener('mouseup', handleSelection);
    return () => document.removeEventListener('mouseup', handleSelection);
  }, []);

  // Toggle chat window
  const toggleChat = () => setIsOpen(prev => !prev);

  // Send message to backend
  const sendMessage = async () => {
    if (!inputValue.trim()) return;

    const userMessage = { id: Date.now(), text: inputValue, sender: 'user' };
    setMessages(prev => [...prev, userMessage]);
    setInputValue('');
    setIsLoading(true);

    try {
      const textToUse = selectedText || inputValue;

      // ✅ Always use the production backend URL to avoid any localhost fallback
      const API_BASE_URL = 'https://book-1-3piy.onrender.com';
      const fullUrl = `${API_BASE_URL}/chat`;

      const response = await fetch(fullUrl, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          query: textToUse,
          selected_text: selectedText || '',
          top_k: 5,
        })
      });

      if (!response.ok) throw new Error(`Server error: ${response.status}`);

      const data = await response.json();

      let botText = data.response || "Sorry, I didn't get a response.";
      if (data.confidence) botText += `\n\n*Confidence: ${(data.confidence * 100).toFixed(1)}%*`;
      if (data.sources && data.sources.length) {
        botText += `\n\n*Sources:*\n${data.sources
          .slice(0, 3)
          .map(s => `- ${s.title || 'Unknown'}${s.url ? ` (${s.url})` : ''}`)
          .join('\n')}`;
      }

      const botMessage = { id: Date.now() + 1, sender: 'bot', text: botText };
      setMessages(prev => [...prev, botMessage]);
      setSelectedText(null);

    } catch (err) {
      console.error(err);
      setMessages(prev => [
        ...prev,
        { id: Date.now() + 1, sender: 'bot', text: "Sorry, I'm having trouble connecting to the server." }
      ]);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle Enter key
  const handleKeyPress = e => {
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
            <button className={styles.closeButton} onClick={toggleChat} aria-label="Close chat">×</button>
          </div>

          <div className={styles.chatMessages}>
            {messages.map(msg => (
              <div key={msg.id} className={`${styles.message} ${msg.sender === 'user' ? styles.userMessage : styles.botMessage}`}>
                {msg.text.split('\n').map((line, i) => <div key={i}>{line}</div>)}
              </div>
            ))}

            {isLoading && (
              <div className={`${styles.message} ${styles.botMessage}`}>
                <div className={styles.typingIndicator}><div></div><div></div><div></div></div>
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
              onChange={e => setInputValue(e.target.value)}
              onKeyPress={handleKeyPress}
              placeholder="Ask about the book content..."
              className={styles.chatInput}
              rows={2}
            />
            <button onClick={sendMessage} disabled={isLoading || !inputValue.trim()} className={styles.sendButton}>
              Send
            </button>
          </div>
        </div>
      ) : (
        <button className={styles.floatingButton} onClick={toggleChat} aria-label="Open chat">💬</button>
      )}
    </div>
  );
};

export default Chatbot;
