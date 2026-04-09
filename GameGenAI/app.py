"""
GameGen AI — Production-Ready Game Platform
============================================

UX Flow:
  Home  → Prompt input (parses game + difficulty → jumps straight to game)
          OR card/chip buttons → difficulty page → game
  Game  → play with adaptive AI

Session state keys:
  page          : "select" | "difficulty" | "game"
  selected_game : "tictactoe" | "maze"
  selected_diff : "easy" | "medium" | "hard"
  controller    : GameController singleton
  show_explain  : bool
  show_path     : bool
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import streamlit as st
from ui.styles  import inject_css
from ui.ttt_ui  import render_ttt
from ui.maze_ui import render_maze
from engine.controller import GameController

# ── Page config ───────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="GameGen AI",
    page_icon="🎮",
    layout="wide",
    initial_sidebar_state="expanded",
)
inject_css()

# ── Session state bootstrap ───────────────────────────────────────────────────
def _init_state():
    defaults = {
        "page":          "select",
        "selected_game": "",
        "selected_diff": "",
        "controller":    GameController(),
        "show_explain":  True,
        "show_path":     False,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

_init_state()
ctrl: GameController = st.session_state.controller


# ══════════════════════════════════════════════════════════════════════════════
# SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown(
        '<div style="font-family:Orbitron,sans-serif;font-size:1.05rem;'
        'font-weight:900;background:linear-gradient(135deg,#6C63FF,#43E8D8);'
        '-webkit-background-clip:text;-webkit-text-fill-color:transparent;'
        'background-clip:text;letter-spacing:2px;margin-bottom:1.2rem;">🎮 GameGen AI</div>',
        unsafe_allow_html=True,
    )

    page = st.session_state.page
    if page != "select":
        if st.button("🏠 Back to Home", use_container_width=True):
            st.session_state.page = "select"
            st.session_state.selected_game = ""
            st.session_state.selected_diff = ""
            st.rerun()

    st.markdown("---")

    st.markdown(
        '<div style="font-family:Orbitron,sans-serif;font-size:0.7rem;'
        'font-weight:700;color:#43E8D8;letter-spacing:2px;margin-bottom:0.7rem;">'
        'SETTINGS</div>',
        unsafe_allow_html=True,
    )
    st.session_state.show_explain = st.toggle("🧠 Explain AI Move",  value=st.session_state.show_explain)
    st.session_state.show_path    = st.toggle("🗺️ Show A* Path (Maze)", value=st.session_state.show_path)

    st.markdown("---")

    st.markdown(
        '<div style="font-family:Orbitron,sans-serif;font-size:0.7rem;'
        'font-weight:700;color:#43E8D8;letter-spacing:2px;margin-bottom:0.9rem;">'
        'STATS</div>',
        unsafe_allow_html=True,
    )
    s = ctrl.stats()
    c1, c2 = st.columns(2)
    with c1:
        st.markdown(
            '<div class="stat-card"><div class="stat-number" style="color:#4ADE80;">'
            + str(s["wins"]) + '</div><div class="stat-label">Wins</div></div>',
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="stat-card"><div class="stat-number" style="color:#FBBF24;">'
            + str(s["draws"]) + '</div><div class="stat-label">Draws</div></div>',
            unsafe_allow_html=True)
    with c2:
        st.markdown(
            '<div class="stat-card"><div class="stat-number" style="color:#F87171;">'
            + str(s["losses"]) + '</div><div class="stat-label">Losses</div></div>',
            unsafe_allow_html=True)
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(
            '<div class="stat-card"><div class="stat-number" style="color:#6C63FF;">'
            + str(s["win_rate"]) + '</div><div class="stat-label">Win Rate</div></div>',
            unsafe_allow_html=True)

    st.markdown("---")
    diff     = ctrl.difficulty_label()
    diff_clr = {"Easy": "#4ADE80", "Medium": "#FBBF24", "Hard": "#F87171"}.get(diff, "#6C63FF")
    st.markdown(
        '<div style="font-size:0.78rem;color:#8892AA;">🎯 Adaptive Difficulty<br>'
        '<span style="font-family:Orbitron,sans-serif;font-size:0.85rem;'
        'font-weight:700;color:' + diff_clr + ';">' + diff + '</span></div>',
        unsafe_allow_html=True,
    )
    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.7rem;color:#4A5468;line-height:1.7;">'
        '🤖 Tic Tac Toe → Minimax + α-β<br>'
        '🌀 Maze → A* pathfinding<br>'
        '📈 Adaptive AI → rolling win-rate<br>'
        '</div>',
        unsafe_allow_html=True,
    )


# ══════════════════════════════════════════════════════════════════════════════
# HELPER: launch from parsed prompt
# ══════════════════════════════════════════════════════════════════════════════

def _launch_from_prompt(raw: str) -> None:
    """Parse raw text → start game → navigate to game page."""
    config = ctrl.generate_from_prompt(raw)
    st.session_state.selected_game = config["game"]
    st.session_state.selected_diff = config["difficulty"]
    st.session_state.page = "game"
    st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: HOME / GAME SELECTION
# ══════════════════════════════════════════════════════════════════════════════

def page_select():
    # Hero
    st.markdown(
        '<div style="text-align:center;margin-bottom:1.8rem;">'
        '<h1 class="brand-title">🎮 GameGen AI</h1>'
        '<p class="brand-sub">Build &amp; Play Games with Smart AI Opponents</p>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Prompt section ────────────────────────────────────────────────────────
    st.markdown(
        '<div class="page-title" style="text-align:center;">Describe Your Game</div>'
        '<p class="page-sub" style="text-align:center;">'
        'Type what you want — the AI parser detects the game &amp; difficulty and launches instantly</p>',
        unsafe_allow_html=True,
    )

    p_col, b_col = st.columns([5, 1], gap="small")
    with p_col:
        prompt = st.text_input(
            "prompt",
            label_visibility="collapsed",
            placeholder='e.g.  "Hard tic tac toe"  or  "Easy maze with enemies"  or  "Unbeatable AI"',
            key="home_prompt",
        )
    with b_col:
        go = st.button("🚀 Generate", use_container_width=True, key="generate_btn")

    if go and prompt.strip():
        _launch_from_prompt(prompt.strip())

    # ── Quick-pick chips ──────────────────────────────────────────────────────
    st.markdown(
        '<div style="font-size:0.76rem;color:#4A5468;margin:0.5rem 0 0.4rem;">'
        '💡 Try one of these:</div>',
        unsafe_allow_html=True,
    )
    chips = [
        ("✕ Hard TTT",          "hard tic tac toe"),
        ("✕ Easy TTT",          "easy tic tac toe"),
        ("🌀 Easy Maze",         "easy maze"),
        ("🌀 Large Hard Maze",   "large hard maze"),
        ("✕ Medium TTT",        "medium tic tac toe"),
    ]
    chip_cols = st.columns(len(chips), gap="small")
    for col, (lbl, chip) in zip(chip_cols, chips):
        with col:
            if st.button(lbl, key="chip_" + chip.replace(" ", "_"),
                         use_container_width=True):
                _launch_from_prompt(chip)

    # ── Divider ───────────────────────────────────────────────────────────────
    st.markdown(
        '<div style="display:flex;align-items:center;gap:1rem;margin:1.6rem 0;">'
        '<div style="flex:1;height:1px;background:rgba(255,255,255,0.06);"></div>'
        '<div style="font-size:0.72rem;color:#4A5468;letter-spacing:1px;">OR PICK MANUALLY</div>'
        '<div style="flex:1;height:1px;background:rgba(255,255,255,0.06);"></div>'
        '</div>',
        unsafe_allow_html=True,
    )

    # ── Game cards ────────────────────────────────────────────────────────────
    col1, col2 = st.columns(2, gap="large")

    with col1:
        st.markdown(
            '<div class="game-card game-card-maze">'
            '<span class="game-card-icon">🌀</span>'
            '<div class="game-card-name">MAZE GAME</div>'
            '<div class="game-card-desc">'
            'Navigate a procedurally generated labyrinth to reach the exit '
            'before the AI enemy hunts you down using A* pathfinding.'
            '</div>'
            '<div class="game-card-tags">'
            '<span class="tag">🗺️ A* Search</span>'
            '<span class="tag">🎲 Procedural</span>'
            '<span class="tag">⚡ Adaptive AI</span>'
            '<span class="tag">🚪 Escape</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        if st.button("🌀 Play Maze Game", key="sel_maze", use_container_width=True):
            st.session_state.selected_game = "maze"
            st.session_state.page = "difficulty"
            st.rerun()

    with col2:
        st.markdown(
            '<div class="game-card game-card-ttt">'
            '<span class="game-card-icon">✕</span>'
            '<div class="game-card-name">TIC TAC TOE</div>'
            '<div class="game-card-desc">'
            'Classic 3x3 strategy game against an AI that uses Minimax '
            'with Alpha-Beta pruning — provably optimal at Hard difficulty.'
            '</div>'
            '<div class="game-card-tags">'
            '<span class="tag">🤖 Minimax</span>'
            '<span class="tag">✂️ α-β Pruning</span>'
            '<span class="tag">🧠 Depth Search</span>'
            '<span class="tag">♟️ Strategy</span>'
            '</div>'
            '</div>',
            unsafe_allow_html=True,
        )
        if st.button("✕ Play Tic Tac Toe", key="sel_ttt", use_container_width=True):
            st.session_state.selected_game = "tictactoe"
            st.session_state.page = "difficulty"
            st.rerun()

    # ── Feature strip ─────────────────────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    _feature_strip()


def _feature_strip():
    features = [
        ("🤖", "AI Opponents",   "Minimax & A* powered enemies"),
        ("📈", "Adaptive Diff.", "AI adjusts to your skill level"),
        ("💡", "AI Explain",     "Understand every AI move"),
        ("📊", "Session Stats",  "Track wins, losses, draws"),
    ]
    cols = st.columns(len(features))
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(
                '<div style="background:#161B27;border:1px solid rgba(255,255,255,0.06);'
                'border-radius:14px;padding:1.2rem;text-align:center;">'
                '<div style="font-size:2rem;margin-bottom:0.5rem;">' + icon + '</div>'
                '<div style="font-family:Orbitron,sans-serif;font-size:0.78rem;font-weight:700;'
                'color:#43E8D8;letter-spacing:1px;margin-bottom:0.3rem;">' + title + '</div>'
                '<div style="font-size:0.76rem;color:#4A5468;">' + desc + '</div>'
                '</div>',
                unsafe_allow_html=True,
            )


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: DIFFICULTY SELECTION
# ══════════════════════════════════════════════════════════════════════════════

def page_difficulty():
    game       = st.session_state.selected_game
    game_label = "Maze Game" if game == "maze" else "Tic Tac Toe"
    game_icon  = "🌀" if game == "maze" else "✕"

    st.markdown(
        '<div style="text-align:center;margin-bottom:2rem;">'
        '<div style="font-size:3.5rem;margin-bottom:0.5rem;">' + game_icon + '</div>'
        '<h1 class="brand-title" style="font-size:2rem;">' + game_label + '</h1>'
        '</div>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div class="page-title" style="text-align:center;">Select Difficulty</div>'
        '<p class="page-sub" style="text-align:center;">'
        'Your performance will dynamically adjust difficulty over time</p>',
        unsafe_allow_html=True,
    )

    difficulties = [
        {
            "key":       "easy",
            "icon":      "🟢",
            "name":      "EASY",
            "color":     "#4ADE80",
            "maze_desc": "Small 9x9 maze · Slow enemy · Forgiving path",
            "ttt_desc":  "Depth 2 Minimax · Makes mistakes · Great for practice",
            "cls":       "diff-easy",
        },
        {
            "key":       "medium",
            "icon":      "🟡",
            "name":      "MEDIUM",
            "color":     "#FBBF24",
            "maze_desc": "Medium 13x13 maze · Standard A* enemy speed",
            "ttt_desc":  "Depth 5 Minimax · Strategic play · Good challenge",
            "cls":       "diff-medium",
        },
        {
            "key":       "hard",
            "icon":      "🔴",
            "name":      "HARD",
            "color":     "#F87171",
            "maze_desc": "Large 17x17 maze · Fast enemy · Bonus moves",
            "ttt_desc":  "Depth 9 Minimax + α-β · Provably unbeatable",
            "cls":       "diff-hard",
        },
    ]

    c1, c2, c3 = st.columns(3, gap="medium")
    for col, d in zip([c1, c2, c3], difficulties):
        desc = d["maze_desc"] if game == "maze" else d["ttt_desc"]
        with col:
            st.markdown(
                '<div class="diff-card ' + d["cls"] + '">'
                '<div class="diff-icon">' + d["icon"] + '</div>'
                '<div class="diff-name" style="color:' + d["color"] + ';">' + d["name"] + '</div>'
                '<div class="diff-desc">' + desc + '</div>'
                '</div>',
                unsafe_allow_html=True,
            )
            if st.button(d["icon"] + " " + d["name"],
                         key="diff_" + d["key"], use_container_width=True):
                st.session_state.selected_diff = d["key"]
                ctrl.start_game(game, d["key"])
                st.session_state.page = "game"
                st.rerun()


# ══════════════════════════════════════════════════════════════════════════════
# PAGE: ACTIVE GAME
# ══════════════════════════════════════════════════════════════════════════════

def page_game():
    game_obj = ctrl.game
    if game_obj is None:
        st.error("No game loaded. Please go back and select a game.")
        if st.button("Back to Home"):
            st.session_state.page = "select"
            st.rerun()
        return

    # Info bar
    diff       = st.session_state.selected_diff
    diff_badge = {
        "easy":   '<span class="badge badge-easy">🟢 Easy</span>',
        "medium": '<span class="badge badge-medium">🟡 Medium</span>',
        "hard":   '<span class="badge badge-hard">🔴 Hard</span>',
    }.get(diff, "")
    game_badge = (
        '<span class="badge badge-cyan">🌀 MAZE</span>'
        if ctrl.game_type == "maze"
        else '<span class="badge badge-pink">✕ TIC TAC TOE</span>'
    )
    st.markdown(
        '<div class="game-info-bar">'
        + game_badge + " " + diff_badge
        + '<span class="game-info-desc">' + ctrl.description + '</span>'
        '</div>',
        unsafe_allow_html=True,
    )

    # Main layout
    game_col, ctrl_col = st.columns([3, 1], gap="medium")

    with game_col:
        if ctrl.game_type == "tictactoe":
            render_ttt(game_obj, show_explain=st.session_state.show_explain)
        elif ctrl.game_type == "maze":
            render_maze(game_obj, show_path=st.session_state.show_path)

    with ctrl_col:
        st.markdown('<div class="section-header">🎛️ Controls</div>', unsafe_allow_html=True)

        if ctrl.game_type == "tictactoe" and game_obj.status != "ongoing":
            outcome_map = {"player_win": "win", "ai_win": "loss", "draw": "draw"}
            ctrl.record_outcome(outcome_map.get(game_obj.status, "draw"))
            if st.button("🔄 Play Again", use_container_width=True, key="play_again"):
                ctrl.restart()
                st.rerun()

        elif ctrl.game_type == "maze" and game_obj.status != "ongoing":
            ctrl.record_outcome("win" if game_obj.status == "player_win" else "loss")
            if st.button("🔄 New Maze", use_container_width=True, key="new_maze"):
                ctrl.restart()
                st.rerun()

        if st.button("⚡ Restart", use_container_width=True, key="restart"):
            ctrl.restart()
            st.rerun()

        if st.button("🎮 Change Game", use_container_width=True, key="change_game"):
            st.session_state.page = "select"
            st.session_state.selected_game = ""
            st.session_state.selected_diff = ""
            st.rerun()

        if st.button("⚙️ Change Difficulty", use_container_width=True, key="change_diff"):
            st.session_state.page = "difficulty"
            st.session_state.selected_diff = ""
            st.rerun()

        st.markdown("<br>", unsafe_allow_html=True)

        # AI info
        st.markdown('<div class="section-header">🤖 AI Info</div>', unsafe_allow_html=True)
        if ctrl.game_type == "tictactoe":
            depth = game_obj.max_depth
            st.markdown(
                '<div class="info-box">'
                'Algorithm: <strong style="color:#43E8D8;">Minimax</strong><br>'
                'α-β Pruning: <strong style="color:#43E8D8;">✓ Enabled</strong><br>'
                'Search Depth: <strong style="color:#FBBF24;">' + str(depth) + '</strong><br>'
                'AI Marker: <strong style="color:#43E8D8;">◎ (O)</strong>'
                '</div>',
                unsafe_allow_html=True,
            )
        elif ctrl.game_type == "maze":
            st.markdown(
                '<div class="info-box">'
                'Algorithm: <strong style="color:#43E8D8;">A* Search</strong><br>'
                'Heuristic: <strong style="color:#43E8D8;">Manhattan</strong><br>'
                'Enemy Speed: <strong style="color:#FBBF24;">1/' + str(game_obj.enemy_speed) + ' moves</strong><br>'
                'Bonus Moves: <strong style="color:#F87171;">' + str(game_obj.enemy_bonus) + '</strong>'
                '</div>',
                unsafe_allow_html=True,
            )

        st.markdown("<br>", unsafe_allow_html=True)

        # Session stats
        st.markdown('<div class="section-header">📊 Session</div>', unsafe_allow_html=True)
        sv = ctrl.stats()
        st.markdown(
            '<div class="info-box">'
            'Wins: <strong style="color:#4ADE80;">' + str(sv["wins"]) + '</strong><br>'
            'Losses: <strong style="color:#F87171;">' + str(sv["losses"]) + '</strong><br>'
            'Draws: <strong style="color:#FBBF24;">' + str(sv["draws"]) + '</strong><br>'
            'Rate: <strong style="color:#6C63FF;">' + str(sv["win_rate"]) + '</strong>'
            '</div>',
            unsafe_allow_html=True,
        )


# ══════════════════════════════════════════════════════════════════════════════
# ROUTER
# ══════════════════════════════════════════════════════════════════════════════

page = st.session_state.page

if page == "select":
    page_select()
elif page == "difficulty":
    page_difficulty()
elif page == "game":
    page_game()
else:
    st.session_state.page = "select"
    st.rerun()
