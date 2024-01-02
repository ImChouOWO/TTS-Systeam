import React, { useState,useEffect } from 'react';
import io from 'socket.io-client';
const AudioRecorder = (props) => {
    const dataFromParent = props.data;
    const [recording, setRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [audioURL, setAudioURL] = useState('');
    const [socket, setSocket] = useState(null);
    const [audioPath,setPath] = useState(null);
    const [userID,setID] = useState("test_1");
    useEffect(()=>{
        const newSocket = io('http://127.0.0.1:5000'); 
        setSocket(newSocket);
        newSocket.on("voice_response", (data) => {
            setPath(data);
        });
        // 接收後即關閉通道
        return () => newSocket.disconnect();


    },[]);

    const startRecording = async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        const recorder = new MediaRecorder(stream);

        // 將 recorder 設置為 mediaRecorder 狀態，以便其他地方可以訪問
        setMediaRecorder(recorder);

        recorder.onstart = () => setRecording(true);
        recorder.onstop = () => setRecording(false);
        recorder.ondataavailable = async (e) => {
            const audioBlob = e.data;
            const formData = new FormData();
            formData.append('file', audioBlob, 'recording.wav');
            formData.append('userID', userID);
            formData.append('chatHistory', JSON.stringify(dataFromParent));
            fetch('http://127.0.0.1:5000/upload', { // Flask伺服器的URL
                method: 'POST',
                body: formData,
            })
            .then(response => response.json())
            .then(data => {
                console.log(data);
                // 處理伺服器回應
            })
            .catch(error => {
                console.error('錯誤:', error);
            });

            const url = URL.createObjectURL(e.data);
            setAudioURL(url);
        };

        recorder.start();
    };

    const stopRecording = () => {
        mediaRecorder && mediaRecorder.stop();
        socket.emit("user_voice_input",{
            status:"not_done",
            user_ID:'test_1'
        })
        console.log(dataFromParent);
    };

    return (
        <div className='audio'>
            
            <div className="audio-control">
                {audioURL && <audio className='audioUrl' src={audioURL} controls />}
            </div>
            <button className='audioBtn' onClick={recording ? stopRecording : startRecording}>
                {recording ? '停止錄音' : '開始錄音'}
            </button>
        </div>

    );
};

export default AudioRecorder;
