"""
GameGen AI - Minimax Algorithm for Tic Tac Toe
Implements Minimax with Alpha-Beta pruning.

Minimax concept:
  - Maximiser (AI) picks the move with the highest score.
  - Minimiser (Player) picks the move with the lowest score.
  - Alpha-Beta pruning skips branches that cannot influence the result,
    dramatically reducing the search tree size.

Scores:
  +10  = AI wins   (adjusted by depth for faster wins)
  -10  = Player wins
   0   = Draw
"""

from typing import Optional


def minimax(
    board: list[list[str]],
    depth: int,
    is_maximizing: bool,
    alpha: float,
    beta: float,
    ai_marker: str = "O",
    player_marker: str = "X",
    max_depth: int = 9,
) -> int:
    """
    Minimax with Alpha-Beta pruning.

    Args:
        board          : 3×3 list of strings ("X", "O", or "")
        depth          : current recursion depth
        is_maximizing  : True when it's the AI's turn
        alpha          : best score maximiser can guarantee (starts -inf)
        beta           : best score minimiser can guarantee (starts +inf)
        ai_marker      : symbol used by AI
        player_marker  : symbol used by human player
        max_depth      : limits search depth for adaptive difficulty

    Returns:
        Integer score of the best achievable outcome.
    """
    winner = check_winner(board)

    # Terminal state checks
    if winner == ai_marker:
        return 10 - depth          # prefer faster wins
    if winner == player_marker:
        return depth - 10          # prefer losing later
    if is_board_full(board):
        return 0                   # draw

    # Depth limit for adaptive difficulty (easy/medium modes)
    if depth >= max_depth:
        return 0

    if is_maximizing:
        best = float("-inf")
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = ai_marker
                    score = minimax(board, depth + 1, False, alpha, beta,
                                    ai_marker, player_marker, max_depth)
                    board[r][c] = ""
                    best  = max(best, score)
                    alpha = max(alpha, best)
                    if beta <= alpha:
                        return best  # Beta cut-off
        return best
    else:
        best = float("inf")
        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = player_marker
                    score = minimax(board, depth + 1, True, alpha, beta,
                                    ai_marker, player_marker, max_depth)
                    board[r][c] = ""
                    best = min(best, score)
                    beta = min(beta, best)
                    if beta <= alpha:
                        return best  # Alpha cut-off
        return best


def best_move(
    board: list[list[str]],
    ai_marker: str = "O",
    player_marker: str = "X",
    max_depth: int = 9,
) -> Optional[tuple[int, int]]:
    """
    Find and return the best (row, col) move for the AI.
    Returns None if no moves are available.
    """
    best_score = float("-inf")
    move: Optional[tuple] = None

    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = ai_marker
                score = minimax(board, 0, False, float("-inf"), float("inf"),
                                ai_marker, player_marker, max_depth)
                board[r][c] = ""
                if score > best_score:
                    best_score = score
                    move = (r, c)

    return move


def check_winner(board: list[list[str]]) -> Optional[str]:
    """
    Check all winning lines and return the winning marker, or None.
    Lines: 3 rows + 3 cols + 2 diagonals.
    """
    lines = [
        # Rows
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        # Columns
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        # Diagonals
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]
    for line in lines:
        values = [board[r][c] for r, c in line]
        if values[0] != "" and len(set(values)) == 1:
            return values[0]
    return None


def is_board_full(board: list[list[str]]) -> bool:
    """Return True if no empty cells remain."""
    return all(board[r][c] != "" for r in range(3) for c in range(3))


def winning_line(board: list[list[str]]) -> Optional[list[tuple]]:
    """Return the winning line as list of (row, col) tuples, or None."""
    lines = [
        [(0, 0), (0, 1), (0, 2)],
        [(1, 0), (1, 1), (1, 2)],
        [(2, 0), (2, 1), (2, 2)],
        [(0, 0), (1, 0), (2, 0)],
        [(0, 1), (1, 1), (2, 1)],
        [(0, 2), (1, 2), (2, 2)],
        [(0, 0), (1, 1), (2, 2)],
        [(0, 2), (1, 1), (2, 0)],
    ]
    for line in lines:
        values = [board[r][c] for r, c in line]
        if values[0] != "" and len(set(values)) == 1:
            return line
    return None
