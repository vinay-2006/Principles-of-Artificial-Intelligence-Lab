"""
GameGen AI - Prompt Parser

Converts a free-text user prompt into a structured game configuration
dictionary using simple keyword-based NLP (no external dependencies).

Supported keywords
──────────────────
Game type   : maze, tictactoe / tic tac toe / ttt
Difficulty  : easy, medium, hard
Size (maze) : small (8×8), large (16×16) — default medium 12×12
AI feature  : smart / intelligent / hard → sets higher difficulty

Returns a config dict:
{
    "game":       "maze" | "tictactoe",
    "difficulty": "easy" | "medium" | "hard",
    "maze_size":  (rows, cols),          # only for maze
    "description": str,                  # human-readable summary
}
"""

import re


# ─── Keyword maps ─────────────────────────────────────────────────────────────

_GAME_KEYWORDS = {
    "maze":      ["maze", "labyrinth", "path", "dungeon"],
    "tictactoe": ["tic", "tac", "toe", "ttt", "noughts", "crosses", "xo"],
}

_DIFFICULTY_KEYWORDS = {
    "easy":   ["easy", "simple", "beginner", "noob", "basic"],
    "medium": ["medium", "normal", "moderate", "average"],
    "hard":   ["hard", "difficult", "expert", "smart", "intelligent",
               "genius", "unbeatable", "impossible", "advanced"],
}

_SIZE_KEYWORDS = {
    "small":  ["small", "tiny", "8x8", "8 x 8"],
    "large":  ["large", "big", "huge", "16x16", "16 x 16"],
    "medium": ["medium", "normal", "12x12"],
}

_MAZE_SIZES = {
    "small":  (9, 9),
    "medium": (13, 13),
    "large":  (17, 17),
}


# ─── Parser ───────────────────────────────────────────────────────────────────

def parse_prompt(prompt: str) -> dict:
    """
    Parse a natural-language game prompt into a config dict.

    Args:
        prompt : raw user input string

    Returns:
        dict with keys: game, difficulty, maze_size, description
    """
    text = prompt.lower()
    tokens = re.findall(r"[a-z0-9]+", text)
    token_set = set(tokens)

    # ── Detect game type ──────────────────────────────────────────────────
    game = _detect_game(text, token_set)

    # ── Detect difficulty ─────────────────────────────────────────────────
    difficulty = _detect_difficulty(text, token_set)

    # ── Detect maze size ──────────────────────────────────────────────────
    size_key = _detect_size(text)
    maze_size = _MAZE_SIZES[size_key]

    # ── Build human-readable description ─────────────────────────────────
    description = _build_description(game, difficulty, maze_size, size_key)

    return {
        "game": game,
        "difficulty": difficulty,
        "maze_size": maze_size,
        "description": description,
    }


def _detect_game(text: str, tokens: set) -> str:
    """Return the most likely game type based on keyword matching."""
    scores = {game: 0 for game in _GAME_KEYWORDS}
    for game, keywords in _GAME_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[game] += 1
    best = max(scores, key=lambda g: scores[g])
    # Default to tictactoe if scores are tied at 0
    return best if scores[best] > 0 else "tictactoe"


def _detect_difficulty(text: str, tokens: set) -> str:
    """Return difficulty level based on keyword matching."""
    scores = {d: 0 for d in _DIFFICULTY_KEYWORDS}
    for diff, keywords in _DIFFICULTY_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                scores[diff] += 1
    best = max(scores, key=lambda d: scores[d])
    return best if scores[best] > 0 else "medium"


def _detect_size(text: str) -> str:
    """Return maze size key: small | medium | large."""
    for size_key, keywords in _SIZE_KEYWORDS.items():
        for kw in keywords:
            if kw in text:
                return size_key
    return "medium"


def _build_description(
    game: str, difficulty: str, maze_size: tuple, size_key: str
) -> str:
    game_name = "Maze" if game == "maze" else "Tic Tac Toe"
    extra = (
        f" ({size_key.capitalize()} {maze_size[0]}×{maze_size[1]} grid)"
        if game == "maze"
        else ""
    )
    ai_desc = {
        "maze": {
            "easy": "slow enemy (A* pathfinding, easy mode)",
            "medium": "standard enemy (A* pathfinding)",
            "hard": "fast intelligent enemy (A* pathfinding, hard mode)",
        },
        "tictactoe": {
            "easy": "random-ish AI (Minimax depth 2)",
            "medium": "strategic AI (Minimax depth 5)",
            "hard": "unbeatable AI (Minimax depth 9, Alpha-Beta pruning)",
        },
    }
    return (
        f"{game_name}{extra} — {difficulty.capitalize()} difficulty — "
        f"{ai_desc[game][difficulty]}"
    )
