"""
GameGen AI - Complete CSS Theme System
Dark-first, production-ready styling.
"""

GLOBAL_CSS = """
<style>
/* ── Google Fonts ──────────────────────────────────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Design tokens ────────────────────────────────────────────────────── */
:root {
    --primary:      #6C63FF;
    --primary-dim:  rgba(108,99,255,0.15);
    --secondary:    #FF6584;
    --accent:       #43E8D8;
    --success:      #4ADE80;
    --warning:      #FBBF24;
    --danger:       #F87171;

    --bg:           #0F1117;
    --bg-card:      #161B27;
    --bg-card2:     #1E2435;
    --bg-input:     #1A1F2E;
    --border:       rgba(255,255,255,0.07);
    --border-accent:rgba(108,99,255,0.35);

    --text:         #E8EAF0;
    --text-dim:     #8892AA;
    --text-muted:   #4A5468;

    --radius-sm:    8px;
    --radius-md:    14px;
    --radius-lg:    20px;
    --radius-pill:  999px;

    --glow-purple:  0 0 24px rgba(108,99,255,0.4);
    --glow-cyan:    0 0 24px rgba(67,232,216,0.35);
    --shadow-card:  0 4px 32px rgba(0,0,0,0.4);
}

/* ── Reset & base ─────────────────────────────────────────────────────── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background-color: var(--bg) !important;
    color: var(--text) !important;
}

/* ── Kill Streamlit chrome completely ────────────────────────────────── */
#MainMenu, footer, .stDeployButton { display: none !important; }

/* Collapse the header fully — removes the blank bar */
header[data-testid="stHeader"] {
    display: none !important;
    height: 0 !important;
    min-height: 0 !important;
    max-height: 0 !important;
    padding: 0 !important;
    margin: 0 !important;
    overflow: hidden !important;
    visibility: hidden !important;
}

/* ── Main layout ──────────────────────────────────────────────────────── */
.main .block-container {
    padding-top: 2rem !important;
    padding-bottom: 3rem !important;
    max-width: 1140px !important;
}

section[data-testid="stSidebar"] > div:first-child {
    background: var(--bg-card) !important;
    border-right: 1px solid var(--border) !important;
}

/* ── Scrollbar ────────────────────────────────────────────────────────── */
::-webkit-scrollbar { width: 5px; height: 5px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--primary); border-radius: 4px; }

/* ════════════════════════════════════════════════════════════════════════
   TYPOGRAPHY
   ════════════════════════════════════════════════════════════════════════ */

.brand-title {
    font-family: 'Orbitron', sans-serif;
    font-size: clamp(2rem, 5vw, 3.4rem);
    font-weight: 900;
    background: linear-gradient(135deg, #6C63FF, #43E8D8, #FF6584);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: 3px;
    animation: brandGlow 4s ease-in-out infinite;
    margin: 0;
    line-height: 1.1;
}
@keyframes brandGlow {
    0%,100% { filter: brightness(1); }
    50%      { filter: brightness(1.25); }
}

.brand-sub {
    font-size: 0.9rem;
    color: var(--text-dim);
    letter-spacing: 4px;
    text-transform: uppercase;
    margin-top: 0.4rem;
}

.page-title {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.5rem;
    font-weight: 700;
    color: var(--accent);
    letter-spacing: 2px;
    margin-bottom: 0.3rem;
}

.page-sub {
    font-size: 0.9rem;
    color: var(--text-dim);
    margin-bottom: 1.8rem;
}

.section-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.85rem;
    font-weight: 700;
    letter-spacing: 2.5px;
    color: var(--accent);
    text-transform: uppercase;
    margin-bottom: 0.8rem;
    padding-bottom: 0.4rem;
    border-bottom: 1px solid rgba(67,232,216,0.18);
}

/* ════════════════════════════════════════════════════════════════════════
   CARD COMPONENTS
   ════════════════════════════════════════════════════════════════════════ */

.game-card {
    background: var(--bg-card);
    border: 1px solid var(--border-accent);
    border-radius: var(--radius-lg);
    padding: 2rem 1.8rem;
    height: 100%;
    transition: transform 0.22s ease, box-shadow 0.22s ease, border-color 0.22s ease;
    cursor: pointer;
    position: relative;
    overflow: hidden;
}
.game-card::before {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(135deg, rgba(108,99,255,0.06), transparent 60%);
    border-radius: var(--radius-lg);
    pointer-events: none;
}
.game-card:hover {
    transform: translateY(-5px);
    box-shadow: var(--glow-purple), var(--shadow-card);
    border-color: var(--primary);
}

.game-card-maze::before {
    background: linear-gradient(135deg, rgba(67,232,216,0.07), transparent 60%);
}
.game-card-maze:hover { border-color: var(--accent); box-shadow: var(--glow-cyan), var(--shadow-card); }

.game-card-ttt::before {
    background: linear-gradient(135deg, rgba(255,101,132,0.07), transparent 60%);
}
.game-card-ttt:hover { border-color: var(--secondary); box-shadow: 0 0 24px rgba(255,101,132,0.35), var(--shadow-card); }

.game-card-icon {
    font-size: 3.2rem;
    margin-bottom: 1rem;
    line-height: 1;
    display: block;
}
.game-card-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.15rem;
    font-weight: 700;
    color: var(--text);
    letter-spacing: 1.5px;
    margin-bottom: 0.6rem;
}
.game-card-desc {
    font-size: 0.85rem;
    color: var(--text-dim);
    line-height: 1.65;
    margin-bottom: 1.2rem;
}
.game-card-tags {
    display: flex;
    flex-wrap: wrap;
    gap: 0.4rem;
    margin-bottom: 1.4rem;
}
.tag {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    background: rgba(255,255,255,0.05);
    border: 1px solid var(--border);
    border-radius: var(--radius-pill);
    padding: 0.2rem 0.65rem;
    font-size: 0.72rem;
    color: var(--text-dim);
    letter-spacing: 0.5px;
}

/* Stats mini card */
.stat-card {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.85rem 1rem;
    text-align: center;
    transition: transform 0.2s;
}
.stat-card:hover { transform: translateY(-2px); }
.stat-number {
    font-family: 'Orbitron', sans-serif;
    font-size: 1.6rem;
    font-weight: 700;
    line-height: 1;
}
.stat-label {
    font-size: 0.65rem;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1.5px;
    margin-top: 0.25rem;
}

/* Info box */
.info-box {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    padding: 0.85rem 1.1rem;
    font-size: 0.82rem;
    color: var(--text-dim);
    line-height: 1.8;
}

/* Explain box */
.explain-box {
    background: linear-gradient(135deg, rgba(108,99,255,0.08), rgba(67,232,216,0.04));
    border: 1px solid rgba(67,232,216,0.25);
    border-radius: var(--radius-md);
    padding: 0.9rem 1.2rem;
    margin-top: 0.8rem;
    font-size: 0.88rem;
    line-height: 1.65;
    animation: fadeUp 0.35s ease;
}
@keyframes fadeUp {
    from { opacity: 0; transform: translateY(6px); }
    to   { opacity: 1; transform: translateY(0); }
}

/* ════════════════════════════════════════════════════════════════════════
   DIFFICULTY SELECTOR CARDS
   ════════════════════════════════════════════════════════════════════════ */

.diff-card {
    background: var(--bg-card);
    border: 2px solid var(--border);
    border-radius: var(--radius-md);
    padding: 1.4rem 1.2rem;
    text-align: center;
    cursor: pointer;
    transition: all 0.2s ease;
    position: relative;
    overflow: hidden;
}
.diff-card:hover { transform: translateY(-3px); }

.diff-easy   { border-color: rgba(74,222,128,0.4); }
.diff-easy:hover   { border-color: var(--success);  box-shadow: 0 0 20px rgba(74,222,128,0.3); }
.diff-medium { border-color: rgba(251,191,36,0.4); }
.diff-medium:hover { border-color: var(--warning); box-shadow: 0 0 20px rgba(251,191,36,0.3); }
.diff-hard   { border-color: rgba(248,113,113,0.4); }
.diff-hard:hover   { border-color: var(--danger);  box-shadow: 0 0 20px rgba(248,113,113,0.3); }

.diff-icon { font-size: 2.4rem; margin-bottom: 0.5rem; line-height: 1; }
.diff-name {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 1.5px;
    margin-bottom: 0.4rem;
}
.diff-desc { font-size: 0.78rem; color: var(--text-dim); line-height: 1.5; }

/* ════════════════════════════════════════════════════════════════════════
   BADGES & PILLS
   ════════════════════════════════════════════════════════════════════════ */

.badge {
    display: inline-flex;
    align-items: center;
    gap: 0.4rem;
    border-radius: var(--radius-pill);
    padding: 0.35rem 0.9rem;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 0.5px;
    border: 1px solid;
}
.badge-primary { background: rgba(108,99,255,0.15); border-color: rgba(108,99,255,0.5); color: #A5A0FF; }
.badge-cyan    { background: rgba(67,232,216,0.12);  border-color: rgba(67,232,216,0.4); color: var(--accent); }
.badge-pink    { background: rgba(255,101,132,0.12); border-color: rgba(255,101,132,0.4); color: var(--secondary); }
.badge-easy    { background: rgba(74,222,128,0.12); border-color: rgba(74,222,128,0.4); color: var(--success); }
.badge-medium  { background: rgba(251,191,36,0.12); border-color: rgba(251,191,36,0.4); color: var(--warning); }
.badge-hard    { background: rgba(248,113,113,0.12);border-color: rgba(248,113,113,0.4); color: var(--danger); }

/* ════════════════════════════════════════════════════════════════════════
   STREAMLIT BUTTON OVERRIDES
   ════════════════════════════════════════════════════════════════════════ */

/* Primary action buttons */
.stButton > button {
    background: linear-gradient(135deg, var(--primary) 0%, #8B5CF6 100%) !important;
    color: #fff !important;
    border: none !important;
    border-radius: var(--radius-md) !important;
    padding: 0.65rem 1.6rem !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.4px !important;
    transition: filter 0.18s, transform 0.15s, box-shadow 0.18s !important;
    box-shadow: 0 2px 12px rgba(108,99,255,0.3) !important;
}
.stButton > button:hover {
    filter: brightness(1.12) !important;
    transform: translateY(-2px) !important;
    box-shadow: 0 6px 20px rgba(108,99,255,0.5) !important;
}
.stButton > button:active { transform: translateY(0) scale(0.98) !important; }
.stButton > button:disabled {
    background: var(--bg-card2) !important;
    box-shadow: none !important;
    color: var(--text-muted) !important;
    cursor: not-allowed !important;
    opacity: 0.6 !important;
}

/* ════════════════════════════════════════════════════════════════════════
   TTT BOARD — Square cells via fixed height
   ════════════════════════════════════════════════════════════════════════ */

/* Visual board renders via custom HTML — see ttt_ui.py */
.ttt-grid {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 10px;
    width: 100%;
    max-width: 420px;
}
.ttt-cell {
    background: var(--bg-card2);
    border: 2px solid var(--border-accent);
    border-radius: var(--radius-md);
    aspect-ratio: 1;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 2.6rem;
    font-weight: 900;
    cursor: pointer;
    transition: background 0.18s, border-color 0.18s, transform 0.14s, box-shadow 0.18s;
    user-select: none;
    color: rgba(255,255,255,0.15);
    min-height: 105px;
}
.ttt-cell:hover { background: rgba(108,99,255,0.18); border-color: var(--primary); transform: scale(1.05); }
.ttt-cell-x   { color: var(--secondary);  background: rgba(255,101,132,0.12); border-color: rgba(255,101,132,0.55); box-shadow: 0 0 18px rgba(255,101,132,0.4); }
.ttt-cell-o   { color: var(--accent);     background: rgba(67,232,216,0.12);  border-color: rgba(67,232,216,0.55);  box-shadow: 0 0 18px rgba(67,232,216,0.4); }
.ttt-cell-win { background: rgba(74,222,128,0.16) !important; border-color: var(--success) !important; box-shadow: 0 0 22px rgba(74,222,128,0.55) !important; animation: cellGlow 1s ease infinite alternate; }
@keyframes cellGlow {
    from { box-shadow: 0 0 10px rgba(74,222,128,0.3); }
    to   { box-shadow: 0 0 24px rgba(74,222,128,0.7); }
}

/* ════════════════════════════════════════════════════════════════════════
   STATUS BANNERS
   ════════════════════════════════════════════════════════════════════════ */

.status-win, .status-lose, .status-draw {
    border-radius: var(--radius-md);
    padding: 1rem 1.4rem;
    text-align: center;
    font-family: 'Orbitron', sans-serif;
    font-size: 1.1rem;
    font-weight: 700;
    letter-spacing: 1px;
}
.status-win  { background: rgba(74,222,128,0.12); border: 1px solid var(--success); color: var(--success); animation: celebrate 0.5s ease; }
.status-lose { background: rgba(248,113,113,0.12);border: 1px solid var(--danger);  color: var(--danger);  animation: shake 0.4s ease; }
.status-draw { background: rgba(251,191,36,0.12); border: 1px solid var(--warning); color: var(--warning); }

@keyframes celebrate {
    0% { transform: scale(0.85); opacity: 0; }
    60% { transform: scale(1.04); }
    100% { transform: scale(1); opacity: 1; }
}
@keyframes shake {
    0%,100% { transform: translateX(0); }
    25%     { transform: translateX(-6px); }
    75%     { transform: translateX(6px); }
}

/* ════════════════════════════════════════════════════════════════════════
   GAME INFO BAR
   ════════════════════════════════════════════════════════════════════════ */

.game-info-bar {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-wrap: wrap;
    background: rgba(108,99,255,0.06);
    border: 1px solid var(--border-accent);
    border-radius: var(--radius-md);
    padding: 0.7rem 1.1rem;
    margin-bottom: 1.2rem;
}
.game-info-desc {
    font-size: 0.8rem;
    color: var(--text-dim);
    margin-left: 0.3rem;
}

/* ════════════════════════════════════════════════════════════════════════
   TIPS PANEL
   ════════════════════════════════════════════════════════════════════════ */

.tips-header {
    font-family: 'Orbitron', sans-serif;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--warning);
    margin-bottom: 0.5rem;
}
.tip-card {
    border-radius: 8px;
    padding: 0.55rem 0.85rem;
    margin-bottom: 0.4rem;
    font-size: 0.82rem;
    line-height: 1.55;
    border-left: 3px solid transparent;
    animation: tipSlide 0.3s ease;
}
@keyframes tipSlide { from { opacity:0; transform:translateX(-5px); } to { opacity:1; transform:translateX(0); } }
.tip-critical { background: rgba(248,113,113,0.1);  border-color: var(--danger);  color: #FECACA; animation: tipSlide 0.3s ease, critPulse 2s ease infinite; }
.tip-warning  { background: rgba(251,191,36,0.09);  border-color: var(--warning); color: #FDE68A; }
.tip-info     { background: rgba(67,232,216,0.08);  border-color: var(--accent);  color: #A7F3F0; }
.tip-tip      { background: rgba(108,99,255,0.08);  border-color: var(--primary); color: #C4B5FD; }
@keyframes critPulse {
    0%,100% { box-shadow: none; }
    50%     { box-shadow: 0 0 8px rgba(248,113,113,0.3); }
}

/* ════════════════════════════════════════════════════════════════════════
   MAZE LEGEND & CONTROLS
   ════════════════════════════════════════════════════════════════════════ */

.legend-item {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    margin-right: 0.9rem;
    font-size: 0.78rem;
    color: var(--text-dim);
}
.legend-dot {
    width: 12px; height: 12px;
    border-radius: 50%;
    display: inline-block;
    flex-shrink: 0;
}
.maze-instructions {
    background: var(--bg-card2);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.7rem 1rem;
    font-size: 0.82rem;
    color: var(--text-dim);
    margin-bottom: 0.6rem;
}

/* ════════════════════════════════════════════════════════════════════════
   DARK MODE TOGGLE (sidebar)
   ════════════════════════════════════════════════════════════════════════ */

.stToggle span { font-size: 0.83rem !important; }

/* ════════════════════════════════════════════════════════════════════════
   STREAMLIT WIDGET CLEANUPS
   ════════════════════════════════════════════════════════════════════════ */

/* Input fields */
.stTextInput > div > div > input {
    background: var(--bg-input) !important;
    border: 1.5px solid var(--border-accent) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 0.95rem !important;
    padding: 0.7rem 1rem !important;
}
.stTextInput > div > div > input:focus {
    border-color: var(--primary) !important;
    box-shadow: 0 0 10px rgba(108,99,255,0.35) !important;
    outline: none !important;
}
.stTextInput > div > div > input::placeholder { color: var(--text-muted) !important; }

/* Selectbox */
.stSelectbox > div > div {
    background: var(--bg-input) !important;
    border-color: var(--border-accent) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
}

/* Alert / info boxes */
.stAlert { border-radius: var(--radius-sm) !important; border: 1px solid var(--border) !important; }

/* Expander */
.streamlit-expanderHeader {
    background: var(--bg-card2) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text) !important;
    font-weight: 600 !important;
}

/* Divider */
hr { border-color: var(--border) !important; }

/* Column gap */
[data-testid="column"] { padding: 0 0.4rem !important; }
</style>
"""


def inject_css():
    """Inject global styles. Call once at the top of app.py."""
    import streamlit as st
    st.markdown(GLOBAL_CSS, unsafe_allow_html=True)
