import sys
from collections import defaultdict
from heapq import heappush, heappop

def in_bounds(location, bounds):
    i, j = location
    return i >= 0 and j >= 0 and i <= bounds[0] and j <= bounds[1]

def adjacent(location, bounds):
    i, j = location
    return (
        (i+di, j+dj) for (di,dj) in ((1,0),(-1,0),(0,1),(0,-1))
        if in_bounds((i+di, j+dj), bounds)
    )

# Heuristic for A* - using Manhattan distance
def heuristic(node, goal):
    return sum(abs(goal[i] - node[i]) for i in (0,1))

def a_star(graph, start, goal, bounds):
    frontier = [ (0, start) ]
    cameFrom = { start: None }
    costSoFar = { start: 0 }

    while frontier:
        cost, current = heappop(frontier)
        if current == goal:
            i = 0
            while current != start:
                current = cameFrom[current]
                i += 1
            return i

        for next in adjacent(current, bounds):
            if graph.getCost(next) - graph.getCost(current) > 1:
                continue # too steep
            newCost = costSoFar[current] + graph.getCost(next)
            if next not in costSoFar or newCost < costSoFar[next]:
                costSoFar[next] = newCost
                priority = newCost + heuristic(next, goal)
                heappush(frontier, (priority, next))
                cameFrom[next] = current

class Graph(object):
    def __init__(self) -> None:
        self.costs = defaultdict(int)

    def setSize(self, i, j):
        self.size = (i, j)

    def setCost(self, i, j, value):
        self.costs[(i,j)] = value

    def getCost(self, node):
        return self.costs[node]

def main(args = ()):
    graph = Graph()
    start = None
    end = None
    maxi = 0
    maxj = 0

    with open("day12.txt") as lines:
        for j, row in enumerate(lines):
            for i, value in enumerate(row.strip()):
                maxi = max(maxi, i)
                maxj = max(maxj, j)
                if value not in ("S", "E"):
                    graph.setCost(i, j, ord(value))
                elif value == "S":
                    start = (i, j)
                    graph.setCost(*start, ord('a'))
                elif value == "E":
                    end = (i, j)
                    graph.setCost(*end, ord('z'))
    
    for part in (1, 2):
        possibleStarts = [ node for node in graph.costs.keys() if graph.getCost(node) == ord('a') ] if part == 2 else [ start ]
    
        steps = {}
        for start in possibleStarts:
            cost = a_star(graph, start, end, (maxi, maxj))
            if cost is not None:
                steps[start] = cost
        print(f"Part {part}:", min(steps.values()))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))