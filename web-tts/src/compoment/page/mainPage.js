import React, { useEffect, useState, useRef ,useLayoutEffect} from 'react';
import '../css/mainPage.css';
import AudioRecorder from './AudioRecorder';
import Live2DComponent from './live2d';
import io from 'socket.io-client';

function MainPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [socket, setSocket] = useState(null);
  const [userID, setUserID] = useState("test_1");
  const terminalImgRef = useRef(null);
  const chatHistoryRef = useRef(null);
  useLayoutEffect(() => {
    if (chatHistoryRef.current) {
      chatHistoryRef.current.scrollTop = chatHistoryRef.current.scrollHeight;
    }
  }, [messages]); // 當messages更新時觸發滾動

  
  
  useEffect(() => {
    const newSocket = io('http://127.0.0.1:5000');
    setSocket(newSocket);

    newSocket.on("text_response", (data) => {
      setMessages(prevMessages => [...prevMessages, { content: data.message.content, type: data.message.type }]);
    });
    // 接收後即關閉通道
    return () => newSocket.disconnect();
  }, []);

  const handleSend = () => {
    // input.trim()以解決react的異步特性
    const trimmedInput = input.trim();
    if (trimmedInput !== "") {
      setMessages(prevMessages => [...prevMessages, { content: trimmedInput, type: 'user' }]);
      console.log(messages);
      setInput("");
      socket.emit('user_text_input', { messages: trimmedInput, userID ,'history':messages});
    }
  };

  const handleInputChange = (e) => {
    setInput(e.target.value);
  }

  return (
    <div className="App">
      <div className="terminal-container" ref={terminalImgRef} >
        <div className='terminal-img' >
          <Live2DComponent parentRef={terminalImgRef}/>
        </div>
        <div className="chat-history" ref={chatHistoryRef}>
          {messages.map((message, index) => (
            <>
            
            <div key={index} className={`chat-message ${message.type === 'user' ? 'user-message' : 'assistant-message'}`}>
              <div className='sticker'>
                <img src={`${message.type === 'user' ? 'img/user.png' : 'img/bot.png'}`} className={`${message.type === 'user' ? 'user-sticker' : 'assistant-sticker'}`}></img>
              </div>
              {message.content}
            </div>
            </>
          ))}
        </div>
      </div>
      <div className="input-area">
        <input 
          type="text" 
          value={input} 
          onChange={handleInputChange} 
          onKeyPress={event => {
            if (event.key === 'Enter') {
              handleSend();
            }
          }}
        />
        <button className="send-button" onClick={handleSend}>Send</button>
      </div>
      <AudioRecorder data = {messages}/>
    </div>
  );
}

export default MainPage;
