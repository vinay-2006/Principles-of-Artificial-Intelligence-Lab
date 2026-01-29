import heapq

class Node:
    def __init__(self, a, b, cost, parent=None):
        self.a = a              # amount of fuel A
        self.b = b              # amount of fuel B
        self.cost = cost
        self.parent = parent

    def octane(self):
        total = self.a + self.b
        if total == 0:
            return 0
        return (self.a * 90 + self.b * 110) / total

    def state(self):
        return (self.a, self.b)

    def __lt__(self, other):
        return self.cost < other.cost


TANK_CAPACITY = 10
TARGET_OCTANE = 100
FUEL_A_COST = 5
FUEL_B_COST = 8
STEP = 1


def heuristic(node):
    return abs(TARGET_OCTANE - node.octane())


def get_successors(node):
    successors = []

    a, b = node.a, node.b
    total = a + b

    if total + STEP <= TANK_CAPACITY:
        successors.append(Node(a + STEP, b, node.cost + FUEL_A_COST, node))
        successors.append(Node(a, b + STEP, node.cost + FUEL_B_COST, node))

    if a >= STEP:
        successors.append(Node(a - STEP, b, node.cost, node))

    if b >= STEP:
        successors.append(Node(a, b - STEP, node.cost, node))

    return successors


def reconstruct(node):
    path = []
    while node:
        path.append(node)
        node = node.parent
    return path[::-1]


def fuel_blending_astar():
    start = Node(0, 0, 0)
    open_list = []
    heapq.heappush(open_list, start)

    visited = set()

    while open_list:
        current = heapq.heappop(open_list)

        if abs(current.octane() - TARGET_OCTANE) < 0.01 and current.a + current.b > 0:
            return reconstruct(current)

        if current.state() in visited:
            continue

        visited.add(current.state())

        for nxt in get_successors(current):
            heapq.heappush(open_list, nxt)

    return None


if __name__ == "__main__":
    solution = fuel_blending_astar()

    if solution:
        print("Fuel Blending Solution:\n")
        for n in solution:
            print(f"A={n.a}, B={n.b}, Octane={n.octane():.2f}, Cost={n.cost}")
    else:
        print("No solution found.")

