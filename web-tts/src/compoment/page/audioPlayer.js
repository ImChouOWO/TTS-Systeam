import React, { useEffect, useRef, useState } from 'react';

function AudioPlayer(props) {
    const { data } = props;
    const audioRef = useRef(null);

    useEffect(() => {
        if (audioRef.current && data) {
            audioRef.current.src = `/voice/${data}`; // 直接更新源
            audioRef.current.play()
                .then(() => {
                    console.log("Audio is now playing");
                })
                .catch(error => {
                    console.error("Audio playback failed:", error);
                });
        }
    }, [data]); // 依赖于 data

    return (
        <audio ref={audioRef} preload="auto" />
    );
}



export default AudioPlayer;
