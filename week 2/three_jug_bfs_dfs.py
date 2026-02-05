from collections import deque

# ---------- POUR FUNCTION ----------

def pour(from_amt, to_amt, to_cap):
    transfer = min(from_amt, to_cap - to_amt)
    return from_amt - transfer, to_amt + transfer


# ---------- SUCCESSORS ----------

def get_successors(state, caps):
    x, y, z = state
    capA, capB, capC = caps

    states = set()

    # Fill
    states.add((capA, y, z))
    states.add((x, capB, z))
    states.add((x, y, capC))

    # Empty
    states.add((0, y, z))
    states.add((x, 0, z))
    states.add((x, y, 0))

    # Pour
    a, b = pour(x, y, capB)
    states.add((a, b, z))

    a, c = pour(x, z, capC)
    states.add((a, y, c))

    b, a = pour(y, x, capA)
    states.add((a, b, z))

    b, c = pour(y, z, capC)
    states.add((x, b, c))

    c, a = pour(z, x, capA)
    states.add((a, y, c))

    c, b = pour(z, y, capB)
    states.add((x, b, c))

    return states


# ---------- BFS ----------

def bfs_three_jug(caps, target):
    start = (0, 0, 0)

    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        state, path = queue.popleft()

        if target in state:
            return path

        for nxt in get_successors(state, caps):
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))

    return None


# ---------- IMPROVED DFS ----------

def dfs_three_jug(caps, target):
    start = (0, 0, 0)

    stack = [(start, [start])]
    visited = {start}

    while stack:
        state, path = stack.pop()

        if target in state:
            return path

        # Get successors
        successors = list(get_successors(state, caps))

        # ---------- ORDERING FIX ----------
        # Sort by closeness to target
        successors.sort(
            key=lambda s: min(abs(target - s[0]),
                              abs(target - s[1]),
                              abs(target - s[2]))
        )

        # Push in reverse (stack LIFO)
        for nxt in reversed(successors):
            if nxt not in visited:
                visited.add(nxt)
                stack.append((nxt, path + [nxt]))

    return None


# ---------- MAIN ----------

if __name__ == "__main__":

    caps = (8, 5, 3)
    target = 7

    print("----- BFS (Shortest Path) -----")
    bfs_path = bfs_three_jug(caps, target)

    if bfs_path:
        for step in bfs_path:
            print(step)
        print("Steps:", len(bfs_path) - 1)
    else:
        print("No solution")

    print("\n----- DFS (Optimized Order) -----")
    dfs_path = dfs_three_jug(caps, target)

    if dfs_path:
        for step in dfs_path:
            print(step)
        print("Steps:", len(dfs_path) - 1)
    else:
        print("No solution")
