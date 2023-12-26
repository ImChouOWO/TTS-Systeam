import React, { useState } from 'react';

const AudioRecorder = () => {
    const [recording, setRecording] = useState(false);
    const [mediaRecorder, setMediaRecorder] = useState(null);
    const [audioURL, setAudioURL] = useState('');

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

            fetch('http://localhost:5000/upload', { // Flask伺服器的URL
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
