import React from 'react';
import { createRoot } from 'react-dom/client';
import App from './App.jsx';
import StoryPage from './StoryPage.js'
import './styles.css';

const container = document.getElementById('root');
const root = createRoot(container);
root.render(
  <React.StrictMode>
    <StoryPage />
  </React.StrictMode>
);