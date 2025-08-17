# AutoFlap 🐦🤖

An AI-powered Flappy Bird game where the bird learns to play automatically using Reinforcement Learning and Neural Networks.


🚀 Features

● AI agent learns to play Flappy Bird without human intervention

● Uses Reinforcement Learning (RL) for decision-making

● Neural Network based game-playing strategy

● Python implementation


🛠️ Tech Stack

● Python 🐍

● Pygame 🎮 – for game environment

● TensorFlow / Keras 🧠 – for building the Neural Network

● Pickle 📦 – for saving and loading trained models


📂 Project Structure
├── best.pickle        # Saved trained model  
├── game.py            # Main game file  
├── train.py           # Training script for the AI agent  
├── README.md          # Project documentation  

⚡ How to Run

● Clone the repository

git clone https://github.com/your-username/AutoFlap.git
cd AutoFlap

● Install dependencies

● pip install -r requirements.txt

● Run the game with AI
python game.py


📖 How it Works

● The bird is controlled by a Neural Network

● The AI improves using Reinforcement Learning (trial & error)

● The best model is stored in best.pickle
