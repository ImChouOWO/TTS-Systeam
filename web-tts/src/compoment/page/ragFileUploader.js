import React, { useState, useEffect } from 'react';
import io from 'socket.io-client';
import '../css/mainPage.css';  // 确保导入了正确的 CSS 文件

const FileUploader = (props) => {
  const dataFromParent = props.data;
  const [selectedFile, setSelectedFile] = useState(null);
  const [uploadStatus, setUploadStatus] = useState('');
  const [fileLabel, setFileLabel] = useState('選擇RAG相關文件');
  const [socket, setSocket] = useState(null);
  const [userID, setID] = useState("test_1");

  useEffect(() => {
    const newSocket = io('http://127.0.0.1:5000');
    setSocket(newSocket);
    return () => newSocket.disconnect();
  }, []);

  const handleFileChange = (event) => {
    const file = event.target.files[0];
    setSelectedFile(file);
    if (file) {
      setFileLabel('準備上傳: ' + file.name);
    } else {
      setFileLabel('選擇RAG相關文件');
    }
  };

  const handleFileUpload = () => {
    if (!selectedFile) {
      setUploadStatus('No file selected');
      setFileLabel('選擇失败');
      return;
    }

    const formData = new FormData();
    formData.append('file', selectedFile);
    formData.append('userID', userID);
    formData.append('chatHistory', JSON.stringify(dataFromParent));

    fetch('http://127.0.0.1:5000/txt_upload', {
      method: 'POST',
      body: formData,
    })
    .then(response => {
      if (!response.ok) {
        console.log('Response not OK:', response);  // 调试信息
        throw new Error('Network response was not ok');
      }
      return response.json();
    })
    .then(data => {
      console.log('Server response data:', data);  // 调试信息
      if (data.error) {
        throw new Error(data.error);
      }
      setUploadStatus('File uploaded successfully');
      setFileLabel('選擇RAG相關文件');
    })
    .catch(error => {
      console.error('Upload error:', error);  // 调试信息
      setUploadStatus('File upload failed');
      
    });
  };

  return (
    <div className='file-uploader'>
      <input 
        type='file' 
        accept='.txt' 
        id='file-input'
        className='input-file'
        onChange={handleFileChange} 
      />

      <label htmlFor='file-input' className='input-label'>{fileLabel}</label>
      <button className='button' onClick={handleFileUpload}>Upload TXT File</button>
    </div>
  );
};

export default FileUploader;
