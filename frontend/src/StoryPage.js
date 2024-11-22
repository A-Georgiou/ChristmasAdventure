import React, { useState } from 'react';
import InitialImage from './static/initial/workshop.webp';
import { storyApi } from './api/storyAPI.js';

const StoryPage = () => {
  const [nodeCount, setNodeCount] = useState(0);
  const [loading, setLoading] = useState(false);
  const [currentStory, setCurrentStory] = useState("Tiny snowflakes dance in the moonlight as you sprinkle your morning pixie dust on the toy-making machines. But something magical is missing... Santa's workshop isn't glowing with its usual golden warmth. His special chair sits empty, his magical compass lies silent on his desk, and the bells on his hat aren't tinkling their morning melody. You flutter your pointy ears, sensing that something isn't right. As Santa's most trusted elf, keeper of special Christmas secrets, you know in your heart that he needs your help. Christmas magic sparkles around you as you consider where to look...");
  const [currentDisplay, setCurrentDisplay] = useState(currentStory);
  const [currentImage, setCurrentImage] = useState(InitialImage);
  const [isConclusion, setIsConclusion] = useState(false);

  const [choices, setChoices] = useState([
    "Visit The Reindeer Stables. Dasher and Blitzen are acting strange, staring at the Frozen Forest. They might know something...",
    "Investigate Santa's desk, where his magical compass lies silent...",
    "Visit The Workshop's Secret Tower. In the distance you can hear the sound of Christmas bells calling your name..."
  ]);

  const handleChoice = async (choice) => {
    setLoading(true);
    setCurrentDisplay(`You chose to ${choice.toLowerCase()}...`)
    try {
      const response = await storyApi.continueStory({
        currentStory,
        choice,
        nodeCount
      });

      let newStory = currentStory + "\n\nYou chose to " + choice + ".\n\n" + response.story;
      setCurrentStory(newStory);
      setCurrentDisplay(response.story);
      if (response.is_conslusion)
        setChoices([]);
      else
        setChoices(response.choices);
      setNodeCount(response.node_count);
      setCurrentImage(response.image_url);
      setIsConclusion(response.is_conclusion);
    } catch (error) {
        console.error('Story API Error:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-gray-900 py-8 px-4">
      <div className="max-w-4xl mx-auto space-y-6 page-story-container">
        <div className="story-image-container">
          <img 
            src={currentImage}
            alt="Christmas Story" 
            className="w-full h-full object-cover"
            onError={(e) => {
              e.target.src = InitialImage;
              console.warn('Image not found, using default image instead.');
            }}
          />
        </div>
        
        <div className="bg-gray-800 bg-opacity-90 rounded-2xl p-8 shadow-xl relative">
          <p className="text-gray-300 story-text leading-relaxed font-serif">
            {currentDisplay}
          </p>
        </div>
        
        {isConclusion ? (
          <div className="space-y-2">
            <div className="bg-red-900 bg-opacity-50 rounded-2xl p-8 shadow-xl relative text-left">
              <p className="text-gray-300 story-text leading-relaxed font-serif font-bold">
                You found Santa Clause! Christmas is saved! 🎅🎄🎁
              </p>
            </div>
            <div className="bg-red-900 bg-opacity-50 rounded-2xl p-8 shadow-xl relative text-left">
              <div className="text-gray-300 story-text leading-relaxed font-serif white-spaced-text">
                <b>View your full story below:&nbsp;</b><br/>
                {currentStory}
              </div>
            </div>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 relative">
            {choices.map((choice, index) => (
              <button
                key={index}
                className="bg-red-900 bg-opacity-50 hover:bg-red-900 text-gray-300 font-serif story-text py-4 px-2 rounded-xl shadow-lg transition-all hover:transform hover:scale-105 active:scale-95"
                onClick={() => handleChoice(choice)}>
                {choice}
              </button>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};

export default StoryPage;