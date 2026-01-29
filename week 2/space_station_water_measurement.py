import heapq

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state      # (x, y)
        self.parent = parent
        self.g = g              # cost so far
        self.h = h              # heuristic
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f


def heuristic(state, target):
    x, _ = state
    return abs(target - x)


def get_successors(state, capX, capY):
    x, y = state
    successors = set()

    # Fill
    successors.add((capX, y))
    successors.add((x, capY))

    # Empty
    successors.add((0, y))
    successors.add((x, 0))

    # Transfer X -> Y
    pour = min(x, capY - y)
    successors.add((x - pour, y + pour))

    # Transfer Y -> X
    pour = min(y, capX - x)
    successors.add((x + pour, y - pour))

    return successors


def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]


def water_jug_a_star(capX, capY, target):
    start = (0, 0)

    open_list = []
    heapq.heappush(open_list, Node(start, None, 0, heuristic(start, target)))

    closed_set = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current.state[0] == target:
            return reconstruct_path(current)

        closed_set.add(current.state)

        for next_state in get_successors(current.state, capX, capY):
            if next_state in closed_set:
                continue

            g = current.g + 1
            h = heuristic(next_state, target)

            heapq.heappush(open_list, Node(next_state, current, g, h))

    return None


# --------- MAIN PROGRAM ---------

if __name__ == "__main__":
    capX = 7
    capY = 4
    target = 6

    path = water_jug_a_star(capX, capY, target)

    if path:
        print("Steps to obtain 6L in container X:\n")
        for step in path:
            print(step)
    else:
        print("No solution found.")
