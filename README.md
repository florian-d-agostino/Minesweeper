# 🕹️ Minesweeper: The Cyberpunk Edition

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Arcade 2.6+](https://img.shields.io/badge/library-Arcade-orange.svg)](https://api.arcade.academy/)

A modern, high-intensity reimagining of the classic Minesweeper game. Built with the **Arcade** library, this version features a unique pseud-3D perspective, cyberpunk aesthetics, and dynamic visual effects.

---

## ✨ Key Features

- **🚀 Pseud-3D Perspective**: Experience the grid like never before with a dynamic depth-of-field effect.
- **⚡ Cyberpunk Aesthetic**: CRT-style shaders, neon glitch animations, and a sleek futuristic UI.
- **💥 Dynamic Particles**: Immersive explosion effects when you hit a mine, with a ripple reveal sequence.
- **🎵 Atmospheric Audio**: Curated synthwave soundtrack ("Chrome Halo") and high-quality sound effects.
- **🏆 High Score Tracking**: Compete against your best times across three difficulty levels.
- **🎮 Responsive UI**: Smooth transitions and hover effects powered by GPU shaders.

---

## 🛠️ Installation

### Prerequisites

- **Python 3.9+**
- **pip** (Python package manager)

### Steps

1. **Clone the repository**:
   ```bash
   git clone https://github.com/YourUsername/minesweeper.git
   cd minesweeper
   ```

2. **Create a virtual environment (optional but recommended)**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

---

## 🚀 How to Run

Simply execute the `main.py` file from the root directory:

```bash
python main.py
```

---

## 🎮 How to Play

The objective remains the same: clear the board without detonating any mines!

- **Left Click**: Reveal a cell.
- **Right Click**: Place/Remove a marker on a suspected mine.
- **First Click**: Guaranteed to be safe, generating the map dynamically around you.

### Difficulty Levels
- **EASY**: 10x10 grid, 12 mines.
- **MEDIUM**: 15x15 grid, 35 mines.
- **HARD**: 20x20 grid, 75 mines.

---

## 📂 Project Structure

- `main.py`: Entry point of the application.
- `src/frontend/`: Contains UI views (Menu, Game, Particles).
- `src/backend/`: Game logic, map generation, and score management.
- `src/public/`: Assets including images, fonts, and sounds.

---

## 🧰 Technologies Used

- **[Python](https://www.python.org/)**: Core programming language.
- **[Arcade](https://api.arcade.academy/)**: Modern Python framework for creating 2D games with ease.
- **GLSL Shaders**: Custom fragment shaders for visual effects.

---

## 📝 License

This project is open-source and available under the MIT License.