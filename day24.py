import sys
from dataclasses import dataclass
from heapq import heappop, heappush
from copy import deepcopy
from functools import lru_cache


class Move:
    RIGHT = ">"
    LEFT = "<"
    UP = "^"
    DOWN = "v"


@dataclass(frozen=True, eq=True)
class Blizzard:
    x: int
    y: int
    move: str


def movedBlizzards(blizzards, bounds):
    for blizzard in blizzards:
        x, y = blizzard.x, blizzard.y
        if blizzard.move == Move.RIGHT:
            x += 1
        elif blizzard.move == Move.LEFT:
            x -= 1
        elif blizzard.move == Move.UP:
            y -= 1
        elif blizzard.move == Move.DOWN:
            y += 1

        if x == 0:
            x = bounds[0] - 1
        elif x == bounds[0]:
            x = 1

        if y == 0:
            y = bounds[1] - 1
        elif y == bounds[1]:
            y = 1
        
        yield Blizzard(x, y, blizzard.move)


@lru_cache
def possibleNextPositions(here, blizzardsAfter, bounds, start, goal):
    inaccessible = set([ (blizzard.x, blizzard.y) for blizzard in blizzardsAfter])

    options = [ (here[0] + dx, here[1] + dy) for (dx, dy) in ((0,0),(1,0),(0,1),(0,-1),(-1,0)) ]
    for option in options:
        if option == goal:
            yield option
        elif option not in inaccessible \
            and option[0] > 0 and option[0] < bounds[0] \
            and option[1] > 0 and option[1] < bounds[1]:
                yield option
        elif option == start:
            yield option

def print_map(current, blizzards, start, goal, bounds):
    for y in range(bounds[1] + 1):
        if current is None:
            print(" ", end="")
        for x in range(bounds[0] + 1):
            blizzardsHere = [ blizzard for blizzard in blizzards if (blizzard.x, blizzard.y) == (x,y) ]
            if (x,y) == current:
                print("E", end="")
            elif x == 0 or x == bounds[0] or y == 0 or y == bounds[1]:
                print("#" if (x, y) not in (start, goal) else ".", end="")
            elif len(blizzardsHere) > 1:
                print(len(blizzardsHere), end="")
            elif len(blizzardsHere) != 0:
                print(blizzardsHere[0].move, end="")
            else:
                print(".", end="")
        print()

def shortest_path(blizzards_at, start, goal, bounds, timerStart=0):
    possibleNextPositions.cache_clear()
    frontier = [ (timerStart, start, blizzards_at(timerStart)) ]
    costSoFar = { (start, blizzards_at(timerStart)): timerStart }

    while frontier:
        cost, currentPosition, blizzards = heappop(frontier)
        #print(f"at {currentPosition}")
        #print_map(currentPosition, blizzards, start, goal, bounds)

        if currentPosition == goal:
            return cost

        blizzardsAfter = blizzards_at(cost + 1)
        for nextPosition in possibleNextPositions(currentPosition, blizzardsAfter, bounds, start, goal):
            newCost = cost + 1
            # print(f"considering at {newCost}:")
            # print_map(None, blizzardsAfter, start, goal, bounds)
            nextState = (nextPosition, blizzardsAfter)
            wasHereBefore = nextPosition in costSoFar
            if wasHereBefore:
                cheaperToGetHere = newCost < costSoFar[nextState]
            if not wasHereBefore or cheaperToGetHere:
                costSoFar[nextState] = newCost
                heappush(frontier, (newCost, nextPosition, blizzardsAfter))


def main(args = ()):
    start = None
    goal = None
    blizzards = []

    with open("day24.txt") as lines:
        for y, line in enumerate(lines):
            line = line.strip()
            if "<" not in line and ">" not in line:
                if y == 0:
                    start = (line.find("."), 0)
                else:
                    goal = (line.find("."), y)
            else:
                for x, ch in enumerate(line):
                    if ch in (Move.UP, Move.DOWN, Move.LEFT, Move.RIGHT):
                        blizzards.append(Blizzard(x, y, ch))
        bounds = (x, y)

    print(f"bounds {bounds}")

    # Precalculate all possible positions of blizzards
    unique = [ frozenset(blizzards) ]
    while True:
        next = frozenset(movedBlizzards(deepcopy(unique[-1]), bounds))
        if next in unique:
            break
        unique.append(next)

    print(f"{len(unique)} unique positions")
    blizzards_at = lambda minute: unique[minute % len(unique)]

    part1 = shortest_path(blizzards_at, start, goal, bounds)
    print(f"Part 1: {part1}")

    part2a = shortest_path(blizzards_at, goal, start, bounds, part1)
    print(f"Part 2A: {part2a - part1}")
    part2b = shortest_path(blizzards_at, start, goal, bounds, part2a)
    print(f"Part 2B: {part2b - part2a}")

    print(f"Total time needed: { part2b }")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))