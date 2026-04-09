"""
GameGen AI - A* Pathfinding Algorithm for Maze Enemy

A* Search:
- Uses a priority queue (min-heap) ordered by f(n) = g(n) + h(n)
- g(n): cost from start to current node
- h(n): Manhattan distance heuristic (admissible for grid mazes)
- Returns the shortest path, or empty list if no path exists

The maze enemy follows the path returned by A* with a configurable
speed multiplier for adaptive difficulty.
"""

import heapq
from typing import Optional


def heuristic(a: tuple[int, int], b: tuple[int, int]) -> int:
    """
    Manhattan distance heuristic.
    Perfect for grid mazes where diagonal moves are not allowed.
    """
    return abs(a[0] - b[0]) + abs(a[1] - b[1])


def astar(
    grid: list[list[int]],
    start: tuple[int, int],
    goal: tuple[int, int],
) -> list[tuple[int, int]]:
    """
    A* pathfinding on a 2-D grid.

    Args:
        grid  : 2-D list where 0 = passable, 1 = wall
        start : (row, col) of the enemy
        goal  : (row, col) of the player

    Returns:
        List of (row, col) tuples from start to goal (inclusive),
        or an empty list if no path exists.
    """
    rows = len(grid)
    cols = len(grid[0])

    # Min-heap element: (f_score, g_score, node)
    open_heap: list[tuple[int, int, tuple]] = []
    heapq.heappush(open_heap, (0 + heuristic(start, goal), 0, start))

    came_from: dict[tuple, Optional[tuple]] = {start: None}
    g_score: dict[tuple, int] = {start: 0}

    # Cardinal directions only (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    while open_heap:
        _, g, current = heapq.heappop(open_heap)

        # Skip if we've already found a cheaper path to this node
        if g > g_score.get(current, float("inf")):
            continue

        if current == goal:
            return _reconstruct_path(came_from, current)

        for dr, dc in directions:
            neighbor = (current[0] + dr, current[1] + dc)
            r, c = neighbor

            # Bounds check
            if not (0 <= r < rows and 0 <= c < cols):
                continue

            # Wall check
            if grid[r][c] == 1:
                continue

            tentative_g = g + 1  # uniform cost: each step costs 1

            if tentative_g < g_score.get(neighbor, float("inf")):
                g_score[neighbor] = tentative_g
                f = tentative_g + heuristic(neighbor, goal)
                heapq.heappush(open_heap, (f, tentative_g, neighbor))
                came_from[neighbor] = current

    return []  # no path found


def _reconstruct_path(
    came_from: dict, current: tuple
) -> list[tuple[int, int]]:
    """Walk back through came_from pointers to build the full path."""
    path = []
    while current is not None:
        path.append(current)
        current = came_from[current]
    path.reverse()
    return path


def next_step_toward(
    grid: list[list[int]],
    enemy_pos: tuple[int, int],
    player_pos: tuple[int, int],
) -> Optional[tuple[int, int]]:
    """
    Return the next cell the enemy should move to.
    Returns None if already adjacent or no path exists.
    """
    path = astar(grid, enemy_pos, player_pos)
    # path[0] is the enemy itself; path[1] is the next step
    if len(path) >= 2:
        return path[1]
    return None
