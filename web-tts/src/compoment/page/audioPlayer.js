import React, { useEffect, useRef, useState } from 'react';

function AudioPlayer() {
    const audioRef = useRef(null);
    const [audioSource, setSource] = useState('/voice/main_video.wav');

    useEffect(() => {
        if (audioRef.current && audioSource) {
            audioRef.current.play()
                .then(() => {
                    console.log("Audio is now playing");
                })
                .catch(error => {
                    console.error("Audio playback failed:", error);
                });
        }
    }, [audioSource]);

    return (
        <audio ref={audioRef} preload="auto">
            <source src={audioSource} type="audio/mpeg" />
        </audio>
    );
}

export default AudioPlayer;
