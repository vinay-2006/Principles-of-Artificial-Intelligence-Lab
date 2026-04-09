"""
GameGen AI - Real-Time Gameplay Tips Engine

Generates contextual, state-aware tips for each game at every step.
Tips are ranked by urgency (critical > tactical > strategic > general)
and help the player make winning decisions.

Tic Tac Toe tips analyse:
  - Immediate win opportunities (player can win now)
  - Immediate threats (AI can win next move — must block)
  - Strategic positioning (center, corners, edges)
  - Fork opportunities (create two simultaneous threats)

Maze tips analyse:
  - Enemy proximity (danger level)
  - Distance to exit
  - Dead-end detection (limited open neighbours)
  - Safe direction recommendations
"""

from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from engine.tictactoe import TicTacToeGame
    from engine.maze import MazeGame


# ═══════════════════════════════════════════════════════════════════════════════
#  TIC TAC TOE TIPS
# ═══════════════════════════════════════════════════════════════════════════════

def ttt_tips(game: "TicTacToeGame") -> list[dict]:
    """
    Return a prioritised list of tip dicts for the current TTT state.
    Each dict: { "icon": str, "level": "critical|warning|info|tip", "text": str }

    Tips are generated fresh every call so they always reflect the live board.
    """
    if game.status != "ongoing" or game.current_turn != "player":
        return []

    tips = []
    board = game.board
    pm = game.player_marker   # "X"
    am = game.ai_marker       # "O"

    # ── 1. Can PLAYER win in one move? (highest priority) ─────────────────
    win_cell = _find_winning_move(board, pm)
    if win_cell:
        r, c = win_cell
        tips.append({
            "icon": "🏆",
            "level": "critical",
            "text": f"WIN NOW! Play row {r+1}, col {c+1} to win the game immediately!",
        })
        return tips   # nothing more important

    # ── 2. Must BLOCK AI from winning? ────────────────────────────────────
    block_cell = _find_winning_move(board, am)
    if block_cell:
        r, c = block_cell
        tips.append({
            "icon": "🛡️",
            "level": "critical",
            "text": f"BLOCK the AI! Play row {r+1}, col {c+1} — the AI wins next move if you don't!",
        })
        return tips

    # ── 3. Fork opportunity (create two simultaneous threats) ─────────────
    fork = _find_fork(board, pm, am)
    if fork:
        r, c = fork
        tips.append({
            "icon": "⚔️",
            "level": "warning",
            "text": f"Create a FORK at row {r+1}, col {c+1} — sets up two winning threats at once!",
        })

    # ── 4. Center advice ──────────────────────────────────────────────────
    if board[1][1] == "":
        tips.append({
            "icon": "⭐",
            "level": "info",
            "text": "Take the CENTER (row 2, col 2) — it's involved in 4 winning lines, the strongest opening move.",
        })

    # ── 5. Corner advice ──────────────────────────────────────────────────
    corners = [(0, 0), (0, 2), (2, 0), (2, 2)]
    empty_corners = [c for c in corners if board[c[0]][c[1]] == ""]
    player_corners = [c for c in corners if board[c[0]][c[1]] == pm]

    if empty_corners and board[1][1] == pm:
        r, c = empty_corners[0]
        tips.append({
            "icon": "🔷",
            "level": "info",
            "text": f"Play a CORNER (e.g. row {r+1}, col {c+1}) — corners create double-threat setups.",
        })

    # ── 6. Opposite corner trap ───────────────────────────────────────────
    opp_corners = {(0,0):(2,2), (2,2):(0,0), (0,2):(2,0), (2,0):(0,2)}
    for corner, opposite in opp_corners.items():
        if board[corner[0]][corner[1]] == am and board[opposite[0]][opposite[1]] == "" :
            tips.append({
                "icon": "🎯",
                "level": "tip",
                "text": f"AI has a corner — take the OPPOSITE corner (row {opposite[0]+1}, col {opposite[1]+1}) to neutralise a fork threat.",
            })
            break

    # ── 7. Edge warning ───────────────────────────────────────────────────
    edges = [(0,1),(1,0),(1,2),(2,1)]
    if not tips:
        tips.append({
            "icon": "💡",
            "level": "tip",
            "text": "Avoid EDGES (middle of sides) — they are the weakest positions. Prefer corners or center.",
        })

    # ── 8. General depth note ─────────────────────────────────────────────
    depth = game.max_depth
    if depth < 9:
        tips.append({
            "icon": "📊",
            "level": "tip",
            "text": f"AI is running at depth {depth} (not perfect) — force it into a bad position with aggressive play.",
        })
    else:
        tips.append({
            "icon": "🤖",
            "level": "tip",
            "text": "AI is UNBEATABLE at this depth — your best outcome is a draw. Play for it!",
        })

    return tips[:3]   # show top 3 most relevant


def _find_winning_move(board: list, marker: str):
    """Return (row, col) of a move that wins for `marker`, or None."""
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = marker
                from ai.minimax import check_winner
                won = check_winner(board) == marker
                board[r][c] = ""
                if won:
                    return (r, c)
    return None


def _find_fork(board: list, marker: str, opponent: str):
    """Return a cell where `marker` can create two winning threats at once."""
    for r in range(3):
        for c in range(3):
            if board[r][c] == "":
                board[r][c] = marker
                threats = sum(
                    1 for rr in range(3) for cc in range(3)
                    if board[rr][cc] == "" and _would_win(board, rr, cc, marker)
                )
                board[r][c] = ""
                if threats >= 2:
                    return (r, c)
    return None


def _would_win(board: list, r: int, c: int, marker: str) -> bool:
    board[r][c] = marker
    from ai.minimax import check_winner
    result = check_winner(board) == marker
    board[r][c] = ""
    return result


# ═══════════════════════════════════════════════════════════════════════════════
#  MAZE TIPS
# ═══════════════════════════════════════════════════════════════════════════════

def maze_tips(game: "MazeGame") -> list[dict]:
    """
    Return up to 3 prioritised tips for the current maze state.
    Each dict: { "icon": str, "level": str, "text": str }
    """
    if game.status != "ongoing":
        return []

    tips = []
    pr, pc   = game.player_pos
    er, ec   = game.enemy_pos
    xr, xc   = game.exit_pos

    enemy_dist  = abs(pr - er) + abs(pc - ec)   # Manhattan
    exit_dist   = abs(pr - xr) + abs(pc - xc)
    total_cells = (game.rows * game.cols) // 2   # rough open cells

    # ── 1. Enemy is VERY close (≤ 3 steps) ────────────────────────────────
    if enemy_dist <= 3:
        safe_dir = _safest_direction(game)
        tips.append({
            "icon": "🚨",
            "level": "critical",
            "text": (
                f"DANGER! Enemy is only {enemy_dist} step(s) away! "
                f"Move {safe_dir} — put walls between you and the enemy NOW."
            ),
        })

    # ── 2. Enemy is moderately close (4–6 steps) ──────────────────────────
    elif enemy_dist <= 6:
        tips.append({
            "icon": "⚠️",
            "level": "warning",
            "text": (
                f"Enemy is {enemy_dist} steps away and closing! "
                f"Head toward the exit (🚪 {'below' if xr > pr else 'above'} and "
                f"{'right' if xc > pc else 'left'}) before it cuts you off."
            ),
        })

    # ── 3. Very close to exit ─────────────────────────────────────────────
    if exit_dist <= 4:
        tips.append({
            "icon": "🏁",
            "level": "critical" if exit_dist <= 2 else "warning",
            "text": (
                f"EXIT is just {exit_dist} step(s) away! "
                f"Push {'down' if xr > pr else 'up'} and {'right' if xc > pc else 'left'} to win!"
            ),
        })

    # ── 4. Dead-end detection ─────────────────────────────────────────────
    open_neighbours = _count_open_neighbours(game, pr, pc)
    if open_neighbours == 1 and exit_dist > 4:
        tips.append({
            "icon": "🔄",
            "level": "warning",
            "text": "You're in a DEAD END! Backtrack immediately — only one way out from here.",
        })

    # ── 5. General direction tip ──────────────────────────────────────────
    vert  = "⬇️ Down"  if xr > pr else "⬆️ Up"
    horiz = "➡️ Right" if xc > pc else "⬅️ Left"
    tips.append({
        "icon": "🧭",
        "level": "info",
        "text": (
            f"Exit is at bottom-right corner. General direction: {vert} then {horiz}. "
            f"({exit_dist} steps by Manhattan distance)"
        ),
    })

    # ── 6. A* awareness tip ───────────────────────────────────────────────
    if enemy_dist > 6:
        tips.append({
            "icon": "🤖",
            "level": "tip",
            "text": (
                "The enemy uses A* pathfinding — it always finds the shortest route to you. "
                "Use WALLS as shields and keep moving toward the exit."
            ),
        })

    # ── 7. Speed tip based on difficulty ──────────────────────────────────
    if game.enemy_speed == 1 and game.enemy_bonus == 0:
        tips.append({
            "icon": "⚡",
            "level": "tip",
            "text": "Medium difficulty: enemy moves every step you take. Don't waste time in dead ends!",
        })
    elif game.enemy_bonus > 0:
        tips.append({
            "icon": "🔥",
            "level": "tip",
            "text": "Hard mode: enemy gets BONUS moves! Plan 2–3 steps ahead and hug walls to slow it down.",
        })
    elif game.enemy_speed >= 2:
        tips.append({
            "icon": "😌",
            "level": "tip",
            "text": f"Easy mode: enemy moves once every {game.enemy_speed} of your steps. Take your time to plan the route.",
        })

    return tips[:3]


def _safest_direction(game: "MazeGame") -> str:
    """Return the cardinal direction that maximises distance from enemy."""
    pr, pc = game.player_pos
    er, ec = game.enemy_pos
    best_dir, best_dist = "away", -1

    moves = {"Up": (-1,0), "Down": (1,0), "Left": (0,-1), "Right": (0,1)}
    for name, (dr, dc) in moves.items():
        nr, nc = pr + dr, pc + dc
        if 0 <= nr < game.rows and 0 <= nc < game.cols and game.grid[nr][nc] == 0:
            dist = abs(nr - er) + abs(nc - ec)
            if dist > best_dist:
                best_dist = dist
                best_dir  = name
    return best_dir


def _count_open_neighbours(game: "MazeGame", r: int, c: int) -> int:
    """Count how many of the 4 cardinal neighbours are open cells."""
    count = 0
    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < game.rows and 0 <= nc < game.cols and game.grid[nr][nc] == 0:
            count += 1
    return count
