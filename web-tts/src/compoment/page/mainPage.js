import React, { useState } from 'react';
import '../css/mainPage.css';
import AudioRecorder from './AudioRecorder';

function MainPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if(input.trim() !== "") {
      setMessages([...messages, input]);
      setInput("");
    }
  }

  const handleInputChange = (e) => {
    setInput(e.target.value);
  }

  const [isSwitchOn, setIsSwitchOn] = useState(false);

  const toggleSwitch = () => {
    setIsSwitchOn(!isSwitchOn);
  };

  return (
    <div className="App">
      <div className="terminal-container">
        <div className='terminal-img'>
          {/* 這裡可以放置終端機的圖像或者其他裝飾 */}
        </div>
        <div className="chat-history">
          {messages.map((message, index) => (
            <div key={index} className="chat-message">{message}</div>
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
      <AudioRecorder/>
    </div>
  );
}

export default MainPage;
