import React from 'react';
import { createRoot } from 'react-dom/client';
import StoryPage from './StoryPage.js'
import './styles.css';
import Snowfall from 'react-snowfall';
import BackgroundMusic from './static/audio/christmas-background.mp3';
import AudioPlayer from './components/AudioPlayer.js';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <Snowfall /> 
    <StoryPage />
    <AudioPlayer audioSource={BackgroundMusic} />
  </React.StrictMode>
);