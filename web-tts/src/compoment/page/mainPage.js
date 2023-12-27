import React, { useEffect ,useState,useRef} from 'react';
import '../css/mainPage.css';
import AudioRecorder from './AudioRecorder';
import Live2DComponent from './live2d';
import Cookies from 'js-cookie';
import io from 'socket.io-client';
function MainPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [socket, setSocket] = useState("");
  const [userID,setUserID] = useState("test_1")
  const handleSend = () => {
    const trimmedInput = input.trim();
    if (trimmedInput !== "") {
      // 首先更新 messages 状态
      setMessages(prevMessages => {
        // 新的 messages 数组
        const historyMessages = [...prevMessages, trimmedInput];
  
        // 然后发送这个更新后的 messages 数组
        socket.emit('user_text_input', { messages: historyMessages, userID });
  
        // 返回更新后的 messages 数组以更新状态
        return historyMessages;
      });
  
      // 清空输入字段
      setInput("");
    }
  };
  
  


  const handleInputChange = (e) => {
    setInput(e.target.value);
  }

  const [isSwitchOn, setIsSwitchOn] = useState(false);

  const toggleSwitch = () => {
    setIsSwitchOn(!isSwitchOn);
  };

  const terminalImgRef = useRef(null);

  useEffect(() => {
    const newSocket = io('http://127.0.0.1:5000');
      setSocket(newSocket);

      return () => {
        newSocket.disconnect();
      };
    }, []);

  return (
    <div className="App">
      <div className="terminal-container" ref={terminalImgRef} >
        <div className='terminal-img' >
          <Live2DComponent parentRef={terminalImgRef}/>
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
