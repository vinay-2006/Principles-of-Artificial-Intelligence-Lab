"""
GameGen AI - Tic Tac Toe Game Logic

Manages the full game state for a Tic Tac Toe session:
  - Board representation (3×3 list of strings)
  - Player / AI move application
  - Win / draw detection
  - Integration with Minimax AI (ai/minimax.py)
  - Move explanation for the "Explain AI" feature
"""

import random
from ai.minimax import best_move, check_winner, is_board_full, winning_line


class TicTacToeGame:
    """
    Full Tic Tac Toe game state and controller.

    Attributes:
        board         : 3×3 list, each cell is "X", "O", or ""
        player_marker : human player symbol (default "X")
        ai_marker     : AI symbol (default "O")
        current_turn  : whose turn it is ("player" or "ai")
        status        : "ongoing" | "player_win" | "ai_win" | "draw"
        last_ai_move  : (row, col) of last AI move, or None
        last_explanation : natural-language explanation of the AI's move
        max_depth     : Minimax depth limit (set by AdaptiveAI)
    """

    MARKER_PLAYER = "X"
    MARKER_AI = "O"

    def __init__(self, max_depth: int = 9):
        self.board: list[list[str]] = [[""] * 3 for _ in range(3)]
        self.player_marker = self.MARKER_PLAYER
        self.ai_marker = self.MARKER_AI
        self.current_turn = "player"   # player always goes first
        self.status = "ongoing"
        self.last_ai_move: tuple | None = None
        self.last_explanation: str = ""
        self.max_depth = max_depth

    # ── Public API ────────────────────────────────────────────────────────

    def player_move(self, row: int, col: int) -> bool:
        """
        Apply a player move at (row, col).

        Returns True if the move was valid and applied, False otherwise.
        """
        if self.status != "ongoing":
            return False
        if self.current_turn != "player":
            return False
        if self.board[row][col] != "":
            return False

        self.board[row][col] = self.player_marker
        self._update_status()
        if self.status == "ongoing":
            self.current_turn = "ai"
        return True

    def ai_move(self) -> tuple | None:
        """
        Let the AI pick and apply the best move.

        Returns the (row, col) chosen, or None if game is over.
        """
        if self.status != "ongoing" or self.current_turn != "ai":
            return None

        move = best_move(
            self.board,
            ai_marker=self.ai_marker,
            player_marker=self.player_marker,
            max_depth=self.max_depth,
        )

        if move is None:
            return None  # no moves left (should not happen if status == ongoing)

        r, c = move
        self.board[r][c] = self.ai_marker
        self.last_ai_move = move
        self.last_explanation = self._explain_move(r, c)
        self._update_status()
        if self.status == "ongoing":
            self.current_turn = "player"
        return move

    def get_winning_cells(self) -> list[tuple] | None:
        """Return winning cells (list of (row,col)) or None."""
        return winning_line(self.board)

    def is_cell_empty(self, row: int, col: int) -> bool:
        return self.board[row][col] == ""

    def reset(self, max_depth: int | None = None) -> None:
        """Restart the game, optionally with a new depth limit."""
        self.__init__(max_depth=max_depth if max_depth is not None else self.max_depth)

    # ── Internal helpers ──────────────────────────────────────────────────

    def _update_status(self) -> None:
        winner = check_winner(self.board)
        if winner == self.player_marker:
            self.status = "player_win"
        elif winner == self.ai_marker:
            self.status = "ai_win"
        elif is_board_full(self.board):
            self.status = "draw"

    def _explain_move(self, row: int, col: int) -> str:
        """Generate a human-readable explanation of the AI's chosen move."""
        # Check if this move wins the game
        test_board = [r[:] for r in self.board]
        if check_winner(test_board) == self.ai_marker:
            return f"🏆 AI played ({row},{col}) — Winning move detected by Minimax!"

        # Check if this move blocks a player win
        test_board2 = [r[:] for r in self.board]
        test_board2[row][col] = self.player_marker  # hypothetical player move
        if check_winner(test_board2) == self.player_marker:
            return f"🛡️ AI played ({row},{col}) — Blocking your winning move (Minimax defense)."

        # Center preference
        if (row, col) == (1, 1):
            return f"⭐ AI played ({row},{col}) — Center is the strongest opening position."

        # Corner preference
        if (row, col) in [(0, 0), (0, 2), (2, 0), (2, 2)]:
            return f"🔷 AI played ({row},{col}) — Corner move: maximises future branching (Minimax depth={self.max_depth})."

        return f"🤖 AI played ({row},{col}) — Best available move according to Minimax search (depth={self.max_depth})."
