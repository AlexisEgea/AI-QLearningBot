# AI-QLearning Bot

## Description

This project is currently under development. 
In this version, you will find the implementation of a bot that uses the **Q-Learning** algorithm.  
The Q-Learning algorithm, a reinforcement learning technique, to make optimal decisions in a game. 
The bot learns to maximize its score by exploring different actions and exploiting the best-known strategies over multiple rounds of the game.

A game is being developed to integrate the QLearnerBot, allowing us to demonstrate the effectiveness of this algorithm.

In the future, this project will include a fully developed game, as well as additional features to enhance the bot's learning process and performance.

### Key Concepts of Q-Learning
- **State Representation:** The state is represented by the current configuration of the game.
- **Action Selection:** The bot can take different actions based on its learned Q-values.
- **Reward System:** The bot updates its knowledge by learning from rewards obtained after each action. The goal is to maximize cumulative rewards over time.

The bot leverages Q-Learning to adapt and improve its strategy based on experiences from previous games.

### Project Objectives
The main goal of this project is to develop a **Q-Learning Bot** that:
1. Learns optimal strategies to win the game over time.
2. Improves its performance by balancing exploration (random actions) and exploitation (best-known actions).
3. Adapts its behavior based on the rewards obtained during gameplay, learning from each experience.

---

## Features

- **Customizable Configuration:** 
  - Define the rules and parameters of the game (e.g., number of attempts, possible actions).
- **Reinforcement Learning Bot (QLearnerBot):**
  - Uses Q-Learning to decide on the best actions based on the current game state.
  - Implements an epsilon-greedy policy for action selection (balancing exploration and exploitation).
  - Tracks and visualizes its learning progress.
- **Random Bot:** A baseline bot that takes random actions for comparison.
- **Performance Visualization:** Plots learning progress and performance evaluations to track improvements over time (`evaluation_plot.png`).

---

## Results

This part will be written when the game is selected and developed.

---

## Requirement

- Python 3.x
- Required Python libraries: 
  - `matplotlib`

---

## Execution 🔧

To get the project running on your machine, follow these steps:

1. Clone the repository:
   ```sh
   git clone https://github.com/AlexisEgea/AI-QLearningBot.git


## Requirement

- Having Python3 and Pip installed on your machine.

## Execution 

To get the project running on your machine, you can run the `installation-requirements.sh` script to install the `venv` environment.  

Once the prerequisites are installed, you can run the `launcher.sh` script to execute the project.  
Follow the project instructions and have fun :)  

### On Ubuntu:

To execute a `.sh` Script:  
   1. Open a terminal.  
   2. Run the command `chmod +x script_name.sh` to make the script executable.  
   3. Execute the script by running `./script_name.sh`.  

Commands to run to make the project work:
1. Cloning the project to your machine
```sh
git clone https://github.com/AlexisEgea/AI-Policy.git
```
2. Installing the prerequisites
```sh
chmod +x installation-requirements.sh
```
```sh
./installation-requirements.sh
```
3. Run the project
```sh
chmod +x launcher.sh
```
```sh
./launcher.sh
```

### On Windows:

Double-click on the `installation-requirements.sh` script, preferably with `Git Bash`, to install the prerequisites:
```
installation-requirements.sh
```

Double-click on the `launcher.sh` script, preferably with `Git Bash`, to run the project:
```
launcher.sh
```
---

Note that the current version of the project has been tested on both Linux and Windows (Git Bash). If you encounter difficulties running the project, feel free to use an IDE (PyCharm, VS Code, or another), create a `venv` environment and execute the one of the `launcher_bot.py` file depending on the player you want to use.

## Contact Information

For inquiries or feedback, please contact me at [alexisegea@outlook.com](mailto:alexisegea@outlook.com).

## Copyright

© 2024 Alexis EGEA. All Rights Reserved.

