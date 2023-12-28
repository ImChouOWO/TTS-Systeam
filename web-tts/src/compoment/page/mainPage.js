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
      // 更新 messages 狀態
      setMessages(prevMessages => [...prevMessages, trimmedInput]);
  
      // 清空輸入欄位
      setInput("");
    }
  };
  
  // 使用 useEffect 監聽 messages 狀態的變化
  useEffect(() => {
    if (messages.length > 0) {
      // 當 messages 更新後，發送整個歷史消息
      socket.emit('user_text_input', { messages, userID });
      socket.on("response",(data)=>{
        console.log(data);
      });
    }
  }, [messages]); // 監聽 messages 的變化

 
  
  
  
  
  


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
