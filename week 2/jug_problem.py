import heapq

class Node:
    def __init__(self, state, parent=None, g=0, h=0):
        self.state = state
        self.parent = parent
        self.g = g
        self.h = h
        self.f = g + h

    def __lt__(self, other):
        return self.f < other.f


def heuristic(state, target):
    x, y = state
    return min(abs(target - x), abs(target - y))


def get_successors(state, capA, capB):
    x, y = state
    successors = set()

    # Fill jugs
    successors.add((capA, y))
    successors.add((x, capB))

    # Empty jugs
    successors.add((0, y))
    successors.add((x, 0))

    # Pour A -> B
    pour = min(x, capB - y)
    successors.add((x - pour, y + pour))

    # Pour B -> A
    pour = min(y, capA - x)
    successors.add((x + pour, y - pour))

    return successors


def reconstruct_path(node):
    path = []
    while node:
        path.append(node.state)
        node = node.parent
    return path[::-1]


def water_jug_a_star(capA, capB, target):
    start = (0, 0)

    open_list = []
    heapq.heappush(open_list, Node(start, None, 0, heuristic(start, target)))

    closed_set = set()

    while open_list:
        current = heapq.heappop(open_list)

        if current.state[0] == target or current.state[1] == target:
            return reconstruct_path(current)

        closed_set.add(current.state)

        for next_state in get_successors(current.state, capA, capB):
            if next_state in closed_set:
                continue

            g = current.g + 1
            h = heuristic(next_state, target)

            heapq.heappush(open_list, Node(next_state, current, g, h))

    return None


# Example
if __name__ == "__main__":
    capA = 10
    capB = 3
    target = 1

    path = water_jug_a_star(capA, capB, target)

    if path:
        print("Solution steps:")
        for step in path:
            print(step)
    else:
        print("No solution found")
