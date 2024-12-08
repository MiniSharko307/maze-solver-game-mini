
# Maze Solver Game

A simple and fun Python game where the player navigates through a randomly generated maze to reach the goal. Built using `pygame`, this project demonstrates basic game development concepts such as grid-based movement, collision detection, and recursive maze generation.

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [How to Play](#how-to-play)
- [Screenshots](#screenshots)
- [Ideas for Improvement](#ideas-for-improvement)
- [License](#license)

---

## Features
- **Random Maze Generation**: A unique maze is created each time using recursive backtracking.
- **Player Navigation**: Smooth, grid-based movement controlled with the arrow keys.
- **Collision Detection**: The player can only move through valid paths and stops at walls.
- **Winning Condition**: The game ends when the player reaches the red square (goal).
- **Simple and Intuitive Gameplay**: Perfect for beginners to explore game mechanics.

---

## Installation
1. **Clone the Repository**:
   ```bash
   git clone https://github.com/Briqo-org/maze-solver-game.git
   cd maze-solver-game
   ```

2. **Install Dependencies**:
   Ensure you have `pygame` installed:
   ```bash
   pip install pygame
   ```

3. **Run the Game**:
   ```bash
   python maze_solver.py
   ```

---

## How to Play
1. Use the **arrow keys** (`↑`, `↓`, `←`, `→`) to move the blue player square through the maze.
2. Reach the **red square (goal)** to win the game.
3. Avoid walls (black squares) — you can only move through open paths (white squares).

---

## Ideas for Improvement
Here are some suggestions to enhance the Maze Solver Game:
1. **Automatic Maze Solver**: Add an algorithm to solve the maze and show the solution path.
2. **Scoring System**: Implement a timer or step counter to challenge players to solve the maze efficiently.
3. **Multiple Levels**: Introduce difficulty levels with larger mazes or narrower paths.
4. **Dynamic Obstacles**: Add moving obstacles or timed traps to make the game more challenging.
5. **Enhanced Graphics**: Replace the colored squares with custom sprites or textures for a polished look.
6. **Mobile Controls**: Add support for touch-based controls for mobile devices.

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

## Acknowledgments
- Built with [pygame](https://www.pygame.org/).
- Inspired by maze-solving algorithms and classic puzzle games.

---
