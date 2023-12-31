import React from 'react';
import ReactDOM from 'react-dom/client';
import './index.css';
import MainPage from './compoment/page/mainPage';
import reportWebVitals from './reportWebVitals';
import AudioRecorder from './compoment/page/AudioRecorder';
import Live2DComponent from './compoment/page/live2d';
import AudioPlayer from './compoment/page/audioPlayer';



const root = ReactDOM.createRoot(document.getElementById('root'));

root.render(
  <React.StrictMode>
    {/* <AudioRecorder /> */}
    {/* <AudioPlayer/> */}
    <MainPage/>
    {/* <Live2DComponent /> */}
  </React.StrictMode>
);

// If you want to start measuring performance in your app, pass a function
// to log results (for example: reportWebVitals(console.log))
// or send to an analytics endpoint. Learn more: https://bit.ly/CRA-vitals
reportWebVitals();
