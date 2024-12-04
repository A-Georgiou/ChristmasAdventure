# The Night Before Crisis 🎅

The Night Before Crisis is a web-based game where players take on the role of one of Santa’s trusted elves. Santa has mysteriously disappeared just days before Christmas, and it’s up to the player to find him through a series of choices and adventures. Each scene is uniquely generated using AI, this includes an AI generated story fragment, AI generated choices extracted from the story and an AI generated illustration of the current scene. This in total creates the key elements of our completely AI generated choose-your-adventure Christmas game.

## 🎮 Play Now

Visit [christmas.AndrewGeorgiou.co.uk](https://christmas.AndrewGeorgiou.co.uk) to play the game!

## 📖 Read About This Project

I wrote a Medium article about the creation of this project, [check it out!](https://medium.com/@andrewgeorgiou98/making-the-night-before-crisis-the-ai-generated-christmas-adventure-game-45e50439249a)

## ✨ Features

- Interactive storytelling with player choices affecting the narrative
- AI-generated story segments using Google's Gemini 1.5 Flash
- AI-generated illustrations for each scene using Replicate's Flux-Schnell model
- Responsive design that works on both desktop and mobile
- Background Christmas music
- Story state management to ensure coherent narrative progression
- Rate limiting to manage API usage

## 🛠️ Tech Stack

- **Frontend**: React with Tailwind CSS
- **Backend**: Python with Flask
- **AI Models**:
  - Text Generation: Google Gemini 1.5 Flash
  - Image Generation: Replicate's Flux-Schnell

## 🚀 Getting Started

### Prerequisites

- Python 3.x
- Node.js and npm
- Google Gemini API key
- Replicate API key

### Installation

1. Clone the repository
```bash
git clone https://github.com/A-Georgiou/ChristmasAdventure.git
cd ChristmasAdventure
```

2. Install backend dependencies
```bash
cd backend
pip install -r requirements.txt
```

3. Install frontend dependencies
```bash
cd frontend
npm install
```

4. Set up environment variables
```bash
# Create .env file in backend directory
GOOGLE_API_KEY=your_gemini_api_key
REPLICATE_API_KEY=your_replicate_api_key
```

5. Start the development servers
```bash
# Start backend server
cd backend
flask app.py
```

## 📖 How It Works

The game uses a state machine to track three distinct story phases:
- Beginning
- Middle
- Conclusion

Each phase influences how the AI generates the next part of the story, ensuring a coherent narrative arc with proper build-up and resolution.

## 🔒 Rate Limiting

The application implements rate limiting to manage API costs:
- 30 requests per day per user
- Approximately 5-6 complete stories per day

## 🎨 Customization

You can modify the prompts in the backend to create different types of adventures. The core system can be adapted for various themes beyond Christmas.

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Fork the repository
- Create a feature branch
- Submit a pull request

## 👨‍💻 Author

Andrew Georgiou
- [LinkedIn](https://linkedin.com/in/andrew-georgiou)
- [Medium](https://medium.com/@andrewgeorgiou98)

## 🌟 Acknowledgments

- Google's Gemini API for text generation
- Replicate's Flux-Schnell model for image generation
- The open-source community for inspirational Christmas-themed projects
