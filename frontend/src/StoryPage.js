import React, { useState } from 'react';
import loadingImage from './api/placeholder/loading.png';

const StoryPage = () => {
  const [currentStory, setCurrentStory] = useState("Tiny snowflakes dance in the moonlight as you sprinkle your morning pixie dust on the toy-making machines. But something magical is missing... Santa's workshop isn't glowing with its usual golden warmth. His special chair sits empty, his magical compass lies silent on his desk, and the bells on his hat aren't tinkling their morning melody. You flutter your pointy ears, sensing that something isn't right. As Santa's most trusted elf, keeper of special Christmas secrets, you know in your heart that he needs your help. Christmas magic sparkles around you as you consider where to look...");
  const [currentDisplay, setCurrentDisplay] = useState(currentStory);

  const [choices, setChoices] = useState([
    "Visit The Reindeer Stables. Dasher and Blitzen are acting strange, staring at the Frozen Forest. They might know something...",
    "Visit The Magical Map Room. Santa's enchanted atlas is glowing under his door...",
    "Visit The Workshop's Secret Tower. In the distance you can hear the sound of Christmas bells calling your name..."
  ]);

  return (
    <div className="min-h-screen bg-gray-900 py-8 px-4">
        <div className="max-w-4xl mx-auto space-y-8">
            <div className="relative w-80 h-80 mx-auto rounded-lg overflow-hidden shadow-2xl">
                <img 
                    src={loadingImage}
                    alt="Christmas Story" 
                    className="w-full h-full object-cover"
                />
            </div>
            <div className="bg-gray-800 bg-opacity-90 rounded-2xl p-8 shadow-xl relative">
                <p className="text-gray-300 text-lg leading-relaxed font-serif">
                    {currentStory}
                </p>
            </div>
        
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4 relative">
                {choices.map((choice, index) => (
                    <button
                    key={index}
                    className="bg-red-900 bg-opacity-50 hover:bg-red-900 text-white font-small py-4 px-2 rounded-xl shadow-lg transition-all hover:transform hover:scale-105 active:scale-95"
                    onClick={() => setCurrentStory(`You chose to ${choice.toLowerCase()}...`)}
                    >
                    {choice}
                    </button>
                ))}
            </div>
      </div>
    </div>
  );
};

export default StoryPage;