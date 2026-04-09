"""
GameGen AI - Maze Game Logic

Generates a random maze using Recursive Backtracking (DFS), then:
  - Places the player at the top-left open cell
  - Places the enemy at a random far corner
  - Uses A* pathfinding (ai/astar.py) to move the enemy toward the player
  - Detects win (player reaches exit) and loss (enemy catches player)

Grid cell values:
  0 = open path
  1 = wall

Special positions tracked separately:
  player_pos : (row, col)
  enemy_pos  : (row, col)
  exit_pos   : (row, col) — bottom-right area
"""

import random
from ai.astar import next_step_toward


class MazeGame:
    """
    Full maze game state and controller.

    Attributes:
        grid        : 2-D list (0=open, 1=wall)
        rows, cols  : grid dimensions
        player_pos  : (row, col)
        enemy_pos   : (row, col)
        exit_pos    : (row, col)
        enemy_speed : player moves before enemy advances (adaptive)
        enemy_bonus : extra enemy moves per turn on Hard
        move_counter: tracks player moves to throttle enemy
        status      : "ongoing" | "player_win" | "player_loss"
        last_path   : current A* path from enemy → player (for visualisation)
    """

    OPEN = 0
    WALL = 1

    def __init__(self, rows: int = 13, cols: int = 13,
                 enemy_speed: int = 1, enemy_bonus: int = 0):
        # Ensure odd dimensions for the maze generator
        self.rows = rows if rows % 2 == 1 else rows + 1
        self.cols = cols if cols % 2 == 1 else cols + 1
        self.enemy_speed = enemy_speed    # enemy moves every N player moves
        self.enemy_bonus = enemy_bonus    # bonus moves on Hard
        self.move_counter = 0
        self.status = "ongoing"
        self.last_path: list[tuple] = []

        self.grid = self._generate_maze()
        self.player_pos = self._find_start()
        self.exit_pos = self._find_exit()
        self.enemy_pos = self._find_enemy_start()

    # ── Maze generation (Recursive Backtracking / DFS) ────────────────────

    def _generate_maze(self) -> list[list[int]]:
        """
        Recursive backtracking maze generation:
          1. Start with an all-wall grid.
          2. DFS from (1,1), carving passages between walls.
          3. Guarantees a connected, solvable maze.
        """
        grid = [[self.WALL] * self.cols for _ in range(self.rows)]

        def carve(r: int, c: int):
            grid[r][c] = self.OPEN
            directions = [(0, 2), (0, -2), (2, 0), (-2, 0)]
            random.shuffle(directions)
            for dr, dc in directions:
                nr, nc = r + dr, c + dc
                if 0 < nr < self.rows - 1 and 0 < nc < self.cols - 1:
                    if grid[nr][nc] == self.WALL:
                        grid[r + dr // 2][c + dc // 2] = self.OPEN  # knock wall
                        carve(nr, nc)

        carve(1, 1)

        # Ensure the exit cell is open
        self._open_cell(grid, self.rows - 2, self.cols - 2)
        return grid

    def _open_cell(self, grid, r, c):
        grid[r][c] = self.OPEN

    def _find_start(self) -> tuple[int, int]:
        return (1, 1)

    def _find_exit(self) -> tuple[int, int]:
        return (self.rows - 2, self.cols - 2)

    def _find_enemy_start(self) -> tuple[int, int]:
        """Place enemy at the farthest open cell from player start."""
        candidates = [
            (self.rows - 2, self.cols - 2),
            (self.rows - 2, 1),
            (1, self.cols - 2),
        ]
        for pos in candidates:
            if self.grid[pos[0]][pos[1]] == self.OPEN and pos != self.player_pos:
                return pos
        # Fallback: scan from bottom-right
        for r in range(self.rows - 1, 0, -1):
            for c in range(self.cols - 1, 0, -1):
                if self.grid[r][c] == self.OPEN and (r, c) != self.player_pos:
                    return (r, c)
        return (self.rows - 2, self.cols - 2)

    # ── Player movement ───────────────────────────────────────────────────

    def move_player(self, direction: str) -> bool:
        """
        Move player in the given direction if the cell is open.

        direction: 'up' | 'down' | 'left' | 'right'
        Returns True if the move was applied.
        """
        if self.status != "ongoing":
            return False

        r, c = self.player_pos
        deltas = {"up": (-1, 0), "down": (1, 0), "left": (0, -1), "right": (0, 1)}
        dr, dc = deltas.get(direction, (0, 0))
        nr, nc = r + dr, c + dc

        # Bounds + wall check
        if not (0 <= nr < self.rows and 0 <= nc < self.cols):
            return False
        if self.grid[nr][nc] == self.WALL:
            return False

        self.player_pos = (nr, nc)
        self.move_counter += 1

        # Check win condition
        if self.player_pos == self.exit_pos:
            self.status = "player_win"
            return True

        # Advance enemy based on speed setting
        if self.move_counter % self.enemy_speed == 0:
            self._advance_enemy()
            for _ in range(self.enemy_bonus):  # extra moves on Hard
                if self.status == "ongoing":
                    self._advance_enemy()

        return True

    # ── Enemy AI (A*) ─────────────────────────────────────────────────────

    def _advance_enemy(self) -> None:
        """Move enemy one step toward the player using A* pathfinding."""
        step = next_step_toward(self.grid, self.enemy_pos, self.player_pos)
        if step is not None:
            self.enemy_pos = step

        # Recompute path for visualisation
        from ai.astar import astar
        self.last_path = astar(self.grid, self.enemy_pos, self.player_pos)

        # Loss condition: enemy reaches player
        if self.enemy_pos == self.player_pos:
            self.status = "player_loss"

    # ── Utility ───────────────────────────────────────────────────────────

    def reset(self, rows: int | None = None, cols: int | None = None,
              enemy_speed: int | None = None, enemy_bonus: int | None = None):
        """Regenerate the maze with same or new parameters."""
        self.__init__(
            rows=rows or self.rows,
            cols=cols or self.cols,
            enemy_speed=enemy_speed if enemy_speed is not None else self.enemy_speed,
            enemy_bonus=enemy_bonus if enemy_bonus is not None else self.enemy_bonus,
        )
