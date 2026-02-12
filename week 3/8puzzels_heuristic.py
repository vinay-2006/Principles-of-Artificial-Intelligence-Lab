import heapq

# Goal State
GOAL = [[1,2,3],
        [4,5,6],
        [7,8,0]]

# Directions for movement
DIRS = [(-1,0),(1,0),(0,-1),(0,1)]


# ---------- HEURISTIC FUNCTION ----------
def manhattan(state):
    distance = 0
    for i in range(3):
        for j in range(3):
            val = state[i][j]
            if val != 0:
                goal_x = (val-1)//3
                goal_y = (val-1)%3
                distance += abs(i-goal_x) + abs(j-goal_y)
    return distance


# ---------- FIND BLANK ----------
def find_blank(state):
    for i in range(3):
        for j in range(3):
            if state[i][j] == 0:
                return i, j


# ---------- STATE TO TUPLE ----------
def to_tuple(state):
    return tuple(tuple(row) for row in state)


# ---------- GENERATE CHILDREN ----------
def get_neighbors(state):
    x, y = find_blank(state)
    neighbors = []

    for dx, dy in DIRS:
        nx, ny = x+dx, y+dy
        if 0 <= nx < 3 and 0 <= ny < 3:
            new_state = [row[:] for row in state]
            new_state[x][y], new_state[nx][ny] = new_state[nx][ny], new_state[x][y]
            neighbors.append(new_state)

    return neighbors


# ---------- A* SOLVER ----------
def a_star(start):

    pq = []
    heapq.heappush(pq, (manhattan(start), 0, start))

    visited = set()
    parent = {}

    while pq:
        f, g, state = heapq.heappop(pq)

        if state == GOAL:
            return reconstruct_path(parent, state)

        visited.add(to_tuple(state))

        for neighbor in get_neighbors(state):
            t = to_tuple(neighbor)

            if t not in visited:
                parent[t] = to_tuple(state)
                h = manhattan(neighbor)
                heapq.heappush(pq, (g+1+h, g+1, neighbor))

    return None


# ---------- PATH RECONSTRUCTION ----------
def reconstruct_path(parent, state):
    path = [state]
    s = to_tuple(state)

    while s in parent:
        s = parent[s]
        path.append([list(row) for row in s])

    path.reverse()
    return path


# ---------- DRIVER CODE ----------
start_state = [[1,2,3],
               [4,0,6],
               [7,5,8]]

solution = a_star(start_state)

if solution:
    print("Solution found in", len(solution)-1, "moves\n")
    for step in solution:
        for row in step:
            print(row)
        print()
else:
    print("No solution found")
