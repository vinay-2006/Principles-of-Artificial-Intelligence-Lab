# 🎮 GameGen AI — Build & Play Games with Smart Opponents

An AI-powered game generator where you describe a game in plain English and play it
instantly against an intelligent opponent.

---

## 🚀 Quick Start

```bash
# 1. Navigate to the project folder
cd "C:\game Genai"

# 2. Install dependencies (only Streamlit needed!)
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

The app will open at **http://localhost:8501** in your browser.

---

## 📁 Project Structure

```
C:\game Genai\
│
├── app.py                  # Main Streamlit application (entry point)
├── requirements.txt        # pip dependencies
│
├── ai/                     # AI Algorithms
│   ├── __init__.py
│   ├── astar.py            # A* Search (maze enemy pathfinding)
│   ├── minimax.py          # Minimax + Alpha-Beta pruning (Tic Tac Toe)
│   └── adaptive.py         # Adaptive difficulty tracker (rolling win-rate)
│
├── engine/                 # Game Logic & Controller
│   ├── __init__.py
│   ├── parser.py           # Prompt → game config (keyword NLP)
│   ├── controller.py       # Central GameController (bridges all layers)
│   ├── tictactoe.py        # Tic Tac Toe game state & logic
│   └── maze.py             # Maze generation (DFS backtracking) + game state
│
└── ui/                     # Streamlit UI Components
    ├── __init__.py
    ├── styles.py            # CSS theme (dark/cyberpunk, animations)
    ├── ttt_ui.py            # Tic Tac Toe board renderer + controls
    └── maze_ui.py           # Maze HTML-table renderer + D-pad controls
```

---

## 🎮 Supported Games

### 🌀 Maze Game
- Procedurally generated maze using **Recursive Backtracking (DFS)**
- Enemy navigates toward you using **A\* Search** with Manhattan heuristic
- Adaptive enemy speed based on your win rate
- Goal: reach the 🚪 exit before the 👾 enemy catches you

### ✕ Tic Tac Toe
- Classic 3×3 game against an AI opponent
- AI uses **Minimax with Alpha-Beta pruning**
- Depth-limited search for Easy/Medium difficulty
- Unbeatable at Hard (depth 9 = perfect play)
- "Explain AI Move" toggles human-readable reasoning

---

## 🧠 AI Algorithms

| Algorithm | Used In | How |
|-----------|---------|-----|
| **A\* Search** | Maze enemy | `ai/astar.py` — priority queue, Manhattan heuristic |
| **Minimax** | Tic Tac Toe AI | `ai/minimax.py` — recursive game tree search |
| **Alpha-Beta Pruning** | Minimax optimisation | Cuts irrelevant branches, speeds up search |
| **Adaptive AI** | Both games | `ai/adaptive.py` — rolling win-rate window adjusts difficulty |

---

## 🔮 Prompt Examples

| Prompt | Game Generated |
|--------|---------------|
| `"Create a maze game with enemies"` | Maze, Medium |
| `"Make tic tac toe but smarter"` | TTT, Hard |
| `"Easy maze small grid"` | Maze, Easy, 9×9 |
| `"Hard tic tac toe unbeatable AI"` | TTT, Hard |
| `"Large maze with hard enemy"` | Maze, Hard, 17×17 |

---

## ⚡ Features

- ✅ **Prompt-driven game generation** — no menus, just describe it
- ✅ **A\* pathfinding** — optimal enemy routing through the maze
- ✅ **Minimax + α-β pruning** — provably optimal Tic Tac Toe AI
- ✅ **Adaptive difficulty** — gets harder/easier based on your performance
- ✅ **AI move explanations** — know *why* the AI played each move
- ✅ **Win/loss/draw stats** — session tracking in the sidebar
- ✅ **Dark cyberpunk UI** — Orbitron font, gradients, animations
- ✅ **No external AI dependencies** — runs 100% offline

---

## 🎓 For Viva / Lab Presentation

Key talking points:

1. **A\* Search**: Uses `f(n) = g(n) + h(n)` where `h` is Manhattan distance. Priority queue ensures the shortest path is always found first.

2. **Minimax**: Recursively evaluates all possible game states. AI (maximiser) picks the highest score; player (minimiser) is assumed to pick the lowest.

3. **Alpha-Beta Pruning**: Skips branches where `beta ≤ alpha`. Reduces average branching factor from O(b^d) to O(b^(d/2)).

4. **Adaptive AI**: Observes a rolling window of 5 recent games. If win-rate > 60% → harder; if < 30% → easier.

5. **Prompt Parsing**: Keyword-based NLP — no heavy libraries. Scores each game type and difficulty by keyword frequency.
