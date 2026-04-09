"""
GameGen AI - Adaptive Difficulty Tracker

Tracks player wins and losses across sessions and adjusts the AI 
difficulty dynamically:

Tic Tac Toe
  - Difficulty controls Minimax search depth (max_depth).
  - Easy:   max_depth = 2   (AI plays randomly-ish)
  - Medium: max_depth = 4
  - Hard:   max_depth = 9   (perfect play)

Maze
  - Difficulty controls enemy move frequency (moves per player move).
  - Easy:   enemy moves every 2 player moves
  - Medium: enemy moves every player move
  - Hard:   enemy moves with one look-ahead bonus move

The tracker shifts difficulty based on a rolling win-rate window.
"""

from dataclasses import dataclass, field


# ─── Difficulty presets ───────────────────────────────────────────────────────

TTT_DEPTH = {"easy": 2, "medium": 5, "hard": 9}   # minimax max depths
MAZE_SPEED = {"easy": 2, "medium": 1, "hard": 1}  # enemy moves per N player moves
MAZE_BONUS = {"easy": 0, "medium": 0, "hard": 1}  # extra bonus moves on Hard


# ─── Adaptive tracker ────────────────────────────────────────────────────────

@dataclass
class AdaptiveAI:
    """
    Maintains a rolling window of game outcomes and adjusts difficulty.

    Attributes:
        wins      : total player wins recorded
        losses    : total player losses recorded
        draws     : total draws recorded
        window    : recent results ('W', 'L', 'D') for rolling analysis
        window_size: how many recent games to consider
        difficulty : current level ('easy', 'medium', 'hard')
    """
    wins: int = 0
    losses: int = 0
    draws: int = 0
    window: list = field(default_factory=list)
    window_size: int = 5
    difficulty: str = "medium"

    # ── Recording outcomes ────────────────────────────────────────────────

    def record_win(self) -> None:
        """Player won — AI should get harder."""
        self.wins += 1
        self._push("W")
        self._adjust()

    def record_loss(self) -> None:
        """Player lost — AI should get easier."""
        self.losses += 1
        self._push("L")
        self._adjust()

    def record_draw(self) -> None:
        """Draw — keep current difficulty."""
        self.draws += 1
        self._push("D")

    # ── Internal rolling window ───────────────────────────────────────────

    def _push(self, outcome: str) -> None:
        self.window.append(outcome)
        if len(self.window) > self.window_size:
            self.window.pop(0)

    def _adjust(self) -> None:
        """
        Shift difficulty by one level based on recent win-rate.
        - win_rate > 0.6  → increase difficulty
        - win_rate < 0.3  → decrease difficulty
        """
        if len(self.window) < 3:
            return  # not enough data yet

        wins_in_window = self.window.count("W")
        win_rate = wins_in_window / len(self.window)

        levels = ["easy", "medium", "hard"]
        idx = levels.index(self.difficulty)

        if win_rate > 0.6 and idx < 2:
            self.difficulty = levels[idx + 1]
        elif win_rate < 0.3 and idx > 0:
            self.difficulty = levels[idx - 1]

    # ── Game-specific helpers ─────────────────────────────────────────────

    def ttt_max_depth(self) -> int:
        """Return minimax depth limit for current difficulty."""
        return TTT_DEPTH[self.difficulty]

    def maze_speed(self) -> int:
        """Return how many player moves before enemy makes one move."""
        return MAZE_SPEED[self.difficulty]

    def maze_bonus_moves(self) -> int:
        """Return extra bonus enemy moves on Hard difficulty."""
        return MAZE_BONUS[self.difficulty]

    # ── Display helpers ───────────────────────────────────────────────────

    def summary(self) -> dict:
        total = self.wins + self.losses + self.draws
        return {
            "difficulty": self.difficulty.capitalize(),
            "wins": self.wins,
            "losses": self.losses,
            "draws": self.draws,
            "total_games": total,
            "win_rate": f"{(self.wins/total*100):.0f}%" if total else "N/A",
        }
