"""
GameGen AI - Central Game Controller

Supports both:
  - Direct game+difficulty selection (structured UI flow)
  - Prompt-based generation (legacy)
"""

from engine.parser import parse_prompt
from engine.tictactoe import TicTacToeGame
from engine.maze import MazeGame
from ai.adaptive import AdaptiveAI


_MAZE_SIZES = {
    "easy":   (9, 9),
    "medium": (13, 13),
    "hard":   (17, 17),
}

_DESCRIPTIONS = {
    "maze": {
        "easy":   "Maze — Easy · Slow enemy, small 9×9 grid, A* pathfinding",
        "medium": "Maze — Medium · Standard enemy, 13×13 grid, A* pathfinding",
        "hard":   "Maze — Hard · Fast enemy, large 17×17 grid, A* pathfinding",
    },
    "tictactoe": {
        "easy":   "Tic Tac Toe — Easy · Random-ish AI (Minimax depth 2)",
        "medium": "Tic Tac Toe — Medium · Strategic AI (Minimax depth 5)",
        "hard":   "Tic Tac Toe — Hard · Unbeatable AI (Minimax depth 9, α-β pruning)",
    },
}


class GameController:
    """Central controller for GameGen AI."""

    def __init__(self):
        self.config: dict  = {}
        self.game          = None
        self.adaptive      = AdaptiveAI()
        self.game_type: str  = ""
        self.description: str = ""

    # ── Direct selection (new structured flow) ─────────────────────────────

    def start_game(self, game_type: str, difficulty: str) -> None:
        """
        Create a game from explicit game_type + difficulty selection.
        game_type : "tictactoe" | "maze"
        difficulty: "easy" | "medium" | "hard"
        """
        self.game_type  = game_type
        self.adaptive.difficulty = difficulty
        self.description = _DESCRIPTIONS.get(game_type, {}).get(difficulty, "")

        rows, cols = _MAZE_SIZES.get(difficulty, (13, 13))
        self.config = {
            "game": game_type,
            "difficulty": difficulty,
            "maze_size": (rows, cols),
            "description": self.description,
        }
        self._init_game()

    # ── Legacy prompt-based generation ────────────────────────────────────

    def generate_from_prompt(self, prompt: str) -> dict:
        self.config  = parse_prompt(prompt)
        self.game_type   = self.config["game"]
        self.description = self.config["description"]

        explicit = ["easy", "hard", "medium", "simple", "difficult", "expert", "beginner"]
        if not any(kw in prompt.lower() for kw in explicit):
            self.config["difficulty"] = self.adaptive.difficulty

        self._init_game()
        return self.config

    # ── Game initialisation ────────────────────────────────────────────────

    def _init_game(self):
        diff = self.config["difficulty"]
        self.adaptive.difficulty = diff

        if self.game_type == "tictactoe":
            self.game = TicTacToeGame(max_depth=self.adaptive.ttt_max_depth())

        elif self.game_type == "maze":
            rows, cols = self.config.get("maze_size", (13, 13))
            self.game = MazeGame(
                rows=rows,
                cols=cols,
                enemy_speed=self.adaptive.maze_speed(),
                enemy_bonus=self.adaptive.maze_bonus_moves(),
            )

    # ── Outcome recording ──────────────────────────────────────────────────

    def record_outcome(self, outcome: str) -> None:
        if outcome == "win":
            self.adaptive.record_win()
        elif outcome == "loss":
            self.adaptive.record_loss()
        else:
            self.adaptive.record_draw()

    # ── Convenience ───────────────────────────────────────────────────────

    def difficulty_label(self) -> str:
        return self.adaptive.difficulty.capitalize()

    def stats(self) -> dict:
        return self.adaptive.summary()

    def restart(self) -> None:
        if self.config:
            self._init_game()
