"""
GameGen AI - Tic Tac Toe UI

Layout:
  TOP    → Beautiful custom HTML 3×3 visual board (display-only)
  BOTTOM → Small coordinate buttons [1,1]…[3,3] for clicking
"""

import streamlit as st
from engine.tictactoe import TicTacToeGame
from ui.tips import ttt_tips
from ui.tip_renderer import render_tips

SYMBOLS = {"X": "X", "O": "O", "": "·"}


# ─── Public renderer ──────────────────────────────────────────────────────────

def render_ttt(game: TicTacToeGame, show_explain: bool = True) -> None:
    winning_cells = set(map(tuple, game.get_winning_cells() or []))

    st.markdown('<div class="section-header">🎮 Tic Tac Toe Board</div>',
                unsafe_allow_html=True)

    # 1. Visual board (HTML display, no click events)
    _render_visual_board(game, winning_cells)

    # 2. Coordinate click buttons below
    _render_click_buttons(game)

    # 3. Status
    _render_status(game)

    # 4. Tips
    tips = ttt_tips(game)
    if tips:
        st.markdown("<br>", unsafe_allow_html=True)
        render_tips(tips)

    # 5. AI explanation
    if show_explain and game.last_explanation:
        st.markdown(
            '<div class="explain-box">🧠 <strong>AI Reasoning:</strong><br>'
            + str(game.last_explanation) + '</div>',
            unsafe_allow_html=True,
        )


# ─── Visual board (HTML) ──────────────────────────────────────────────────────

def _cell_html(val: str, is_win: bool) -> str:
    """Return a styled <div> for one cell — no f-strings to avoid brace issues."""
    sym = SYMBOLS.get(val, "·")
    if is_win and val:
        sym = "★ " + sym

    if is_win:
        bg     = "rgba(74,222,128,0.16)"
        border = "2px solid #4ADE80"
        color  = "#4ADE80"
        shadow = "0 0 22px rgba(74,222,128,0.52)"
        anim   = "animation:cellGlow 1.1s ease infinite alternate;"
    elif val == "X":
        bg     = "rgba(255,101,132,0.13)"
        border = "2px solid rgba(255,101,132,0.62)"
        color  = "#FF6584"
        shadow = "0 0 18px rgba(255,101,132,0.42)"
        anim   = ""
    elif val == "O":
        bg     = "rgba(67,232,216,0.13)"
        border = "2px solid rgba(67,232,216,0.62)"
        color  = "#43E8D8"
        shadow = "0 0 18px rgba(67,232,216,0.42)"
        anim   = ""
    else:
        bg     = "#1a2035"
        border = "2px solid rgba(108,99,255,0.28)"
        color  = "rgba(255,255,255,0.10)"
        shadow = "inset 0 1px 0 rgba(255,255,255,0.04)"
        anim   = ""

    style = (
        "background:" + bg + ";"
        "border:" + border + ";"
        "border-radius:14px;"
        "min-height:112px;"
        "display:flex;"
        "align-items:center;"
        "justify-content:center;"
        "font-family:'Orbitron',sans-serif;"
        "font-size:2.8rem;"
        "font-weight:900;"
        "color:" + color + ";"
        "box-shadow:" + shadow + ";"
        "user-select:none;"
        "transition:transform 0.15s ease,box-shadow 0.18s ease;"
        + anim
    )
    return '<div style="' + style + '">' + sym + '</div>'


def _render_visual_board(game: TicTacToeGame, winning_cells: set) -> None:
    """Build the full 9-cell HTML grid and render it once."""
    cells = ""
    for r in range(3):
        for c in range(3):
            cells = cells + _cell_html(game.board[r][c], (r, c) in winning_cells)

    # Keyframes and grid wrapper — all built as plain strings, no f-strings
    css = (
        "<style>"
        "@keyframes cellGlow{"
        "from{box-shadow:0 0 10px rgba(74,222,128,0.3);}"
        "to{box-shadow:0 0 26px rgba(74,222,128,0.72);}"
        "}"
        ".ttt-grid{"
        "display:grid;"
        "grid-template-columns:repeat(3,1fr);"
        "gap:10px;"
        "max-width:460px;"
        "margin-bottom:0.5rem;"
        "}"
        "</style>"
    )

    html = css + '<div class="ttt-grid">' + cells + "</div>"
    st.markdown(html, unsafe_allow_html=True)


# ─── Coordinate click buttons ─────────────────────────────────────────────────

def _render_click_buttons(game: TicTacToeGame) -> None:
    """Compact styled rows of [row,col] buttons below the visual board."""
    st.markdown(
        "<style>"
        ".btn-row .stButton>button{"
        "height:32px!important;"
        "min-height:0!important;"
        "padding:0 6px!important;"
        "font-size:0.72rem!important;"
        "font-weight:600!important;"
        "border-radius:8px!important;"
        "letter-spacing:0.3px!important;"
        "box-shadow:none!important;"
        "}"
        ".btn-row .stButton>button:disabled{"
        "opacity:0.28!important;"
        "cursor:not-allowed!important;"
        "}"
        ".btn-row [data-testid=column]{padding:0 3px!important;}"
        "</style>",
        unsafe_allow_html=True,
    )

    st.markdown(
        '<div style="font-size:0.68rem;color:#4A5468;'
        'letter-spacing:0.8px;margin-bottom:3px;">↓ SELECT A CELL</div>',
        unsafe_allow_html=True,
    )

    for r in range(3):
        st.markdown('<div class="btn-row">', unsafe_allow_html=True)
        cols = st.columns([1, 1, 1], gap="small")
        for c in range(3):
            val = game.board[r][c]
            disabled = (
                val != ""
                or game.status != "ongoing"
                or game.current_turn != "player"
            )
            label = "[" + str(r + 1) + "," + str(c + 1) + "]"
            with cols[c]:
                if st.button(label, key="ttt_" + str(r) + "_" + str(c),
                             disabled=disabled, use_container_width=True):
                    moved = game.player_move(r, c)
                    if moved and game.status == "ongoing":
                        game.ai_move()
                    st.rerun()
        st.markdown("</div>", unsafe_allow_html=True)


# ─── Status banner ────────────────────────────────────────────────────────────

def _render_status(game: TicTacToeGame) -> None:
    st.markdown("<br>", unsafe_allow_html=True)
    s = game.status
    if s == "player_win":
        st.markdown('<div class="status-win">🏆 You Win! Congratulations!</div>',
                    unsafe_allow_html=True)
    elif s == "ai_win":
        st.markdown('<div class="status-lose">🤖 AI Wins! Better luck next time.</div>',
                    unsafe_allow_html=True)
    elif s == "draw":
        st.markdown('<div class="status-draw">🤝 It\'s a Draw!</div>',
                    unsafe_allow_html=True)
    else:
        turn = game.current_turn
        icon = "🕹️" if turn == "player" else "🤖"
        msg  = "Your turn (X)" if turn == "player" else "AI thinking… (O)"
        st.info(icon + " " + msg)
