"""
GameGen AI - Maze UI Component

Renders the maze as a coloured HTML table for crisp, flicker-free display.
All state management is done via Streamlit session state.

Cell colour scheme:
  Wall       : dark navy  (#1a1a2e)
  Open path  : mid-dark   (#16213e)
  Player     : purple     (#6C63FF)
  Enemy      : red        (#F87171)
  Exit       : green      (#4ADE80)
  A* Path    : highlighted trail (subtle teal)
"""

import streamlit as st
from engine.maze import MazeGame
from ui.tips import maze_tips
from ui.tip_renderer import render_tips


# ── Colour palette ────────────────────────────────────────────────────────────
COLORS = {
    "wall":    "#111125",
    "open":    "#1C1E35",
    "player":  "#6C63FF",
    "enemy":   "#F87171",
    "exit":    "#4ADE80",
    "path":    "#1E3A4A",   # subtle A* path highlight
}

CELL_SIZE = 28  # px per cell


def render_maze(game: MazeGame, show_path: bool = False) -> None:
    """
    Full Maze UI:
      - HTML table maze grid
      - WASD / arrow key controls (button-based)
      - Status banner
      - Legend

    Args:
        game      : active MazeGame instance
        show_path : overlay the A* path from enemy to player
    """
    st.markdown('<div class="section-header">🌀 Maze Game</div>', unsafe_allow_html=True)

    # ── Grid rendering ─────────────────────────────────────────────────────
    _render_grid(game, show_path)

    # ── Legend ──────────────────────────────────────────────────────────────
    _render_legend()

    # ── Live tips ──────────────────────────────────────────────────────────
    tips = maze_tips(game)
    if tips:
        render_tips(tips)

    # ── Status ──────────────────────────────────────────────────────────────
    _render_status(game)

    # ── Movement controls ────────────────────────────────────────────────
    if game.status == "ongoing":
        _render_controls(game)


def _render_grid(game: MazeGame, show_path: bool) -> None:
    """Build and display the maze as an HTML table."""
    path_set = set(map(tuple, game.last_path[1:-1])) if show_path else set()

    rows_html = []
    for r in range(game.rows):
        cells_html = []
        for c in range(game.cols):
            pos = (r, c)

            if pos == game.player_pos:
                bg = COLORS["player"]
                icon = "🧑"
            elif pos == game.enemy_pos:
                bg = COLORS["enemy"]
                icon = "👾"
            elif pos == game.exit_pos:
                bg = COLORS["exit"]
                icon = "🚪"
            elif game.grid[r][c] == 1:
                bg = COLORS["wall"]
                icon = ""
            elif pos in path_set:
                bg = COLORS["path"]
                icon = "·"
            else:
                bg = COLORS["open"]
                icon = ""

            border_radius = "4px"
            cells_html.append(
                f'<td style="width:{CELL_SIZE}px;height:{CELL_SIZE}px;'
                f'background:{bg};border-radius:{border_radius};'
                f'text-align:center;vertical-align:middle;'
                f'font-size:{CELL_SIZE * 0.55}px;line-height:1;'
                f'border:1px solid rgba(255,255,255,0.03);">'
                f'{icon}</td>'
            )
        rows_html.append(f"<tr>{''.join(cells_html)}</tr>")

    table_html = (
        f'<div style="overflow-x:auto;margin-bottom:0.5rem;">'
        f'<table style="border-collapse:collapse;border-spacing:0;'
        f'background:#0D0E1A;border-radius:12px;padding:4px;'
        f'box-shadow:0 0 30px rgba(108,99,255,0.3);">'
        f"{''.join(rows_html)}"
        f"</table></div>"
    )
    st.markdown(table_html, unsafe_allow_html=True)


def _render_legend() -> None:
    legend = (
        f'<div style="margin:0.4rem 0 0.6rem;">'
        f'<span class="legend-item"><span class="legend-dot" style="background:{COLORS["player"]};"></span> You</span>'
        f'<span class="legend-item"><span class="legend-dot" style="background:{COLORS["enemy"]};"></span> Enemy (A*)</span>'
        f'<span class="legend-item"><span class="legend-dot" style="background:{COLORS["exit"]};"></span> Exit</span>'
        f'<span class="legend-item"><span class="legend-dot" style="background:{COLORS["wall"]};"></span> Wall</span>'
        f'</div>'
    )
    st.markdown(legend, unsafe_allow_html=True)


def _render_status(game: MazeGame) -> None:
    if game.status == "player_win":
        st.markdown('<div class="status-win">🏆 You reached the exit! You Win!</div>', unsafe_allow_html=True)
    elif game.status == "player_loss":
        st.markdown('<div class="status-lose">💀 The enemy caught you! Game Over.</div>', unsafe_allow_html=True)


def _render_controls(game: MazeGame) -> None:
    """Render WASD-style directional buttons."""
    st.markdown('<div class="maze-instructions">⌨️ Use the buttons below to move (or arrow keys are simulated):</div>',
                unsafe_allow_html=True)

    # Up
    _, mid, _ = st.columns([2, 1, 2])
    with mid:
        if st.button("▲", key="move_up", use_container_width=True):
            game.move_player("up")
            st.rerun()

    # Left / Down / Right
    left_col, mid_col, right_col = st.columns([1, 1, 1])
    with left_col:
        if st.button("◄", key="move_left", use_container_width=True):
            game.move_player("left")
            st.rerun()
    with mid_col:
        if st.button("▼", key="move_down", use_container_width=True):
            game.move_player("down")
            st.rerun()
    with right_col:
        if st.button("►", key="move_right", use_container_width=True):
            game.move_player("right")
            st.rerun()
