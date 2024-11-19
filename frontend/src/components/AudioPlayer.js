import React, { useState, useRef } from 'react';

const AudioPlayer = ({ audioSource }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const audioRef = useRef(null);

  const togglePlay = () => {
    if (audioRef.current.paused) {
      audioRef.current.play();
      setIsPlaying(true);
    } else {
      audioRef.current.pause();
      setIsPlaying(false);
    }
  };

  return (
    <div className="absolute top-4 right-4">
      <button
        onClick={togglePlay}
        className="bg-red-900 hover:bg-red-800 text-white w-10 h-10 rounded-full flex items-center justify-center transition-colors"
        aria-label={isPlaying ? 'Pause' : 'Play'}
      >
        {isPlaying ? (
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <rect x="6" y="4" width="4" height="16"/>
            <rect x="14" y="4" width="4" height="16"/>
          </svg>
        ) : (
          <svg className="w-4 h-4" viewBox="0 0 24 24" fill="currentColor">
            <path d="M8 5v14l11-7z"/>
          </svg>
        )}
      </button>
      <audio
        ref={audioRef}
        loop
        preload="auto"
        className="hidden"
      >
        <source src={audioSource} type="audio/mp3" />
      </audio>
    </div>
  );
};

export default AudioPlayer;