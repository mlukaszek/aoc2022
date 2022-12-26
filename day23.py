import sys
from collections import defaultdict, Counter
from dataclasses import dataclass, field, astuple


@dataclass
class Position:
    x: int
    y: int


class Direction:
    N = (0,-1)
    NE = (1,-1)
    E = (1,0)
    SE = (1,1)
    S = (0,1)
    SW = (-1,1)
    W = (-1,0)
    NW = (-1,-1)
    NONE = (0,0)
    COUNT = 4
    ALL = (N, NE, E, SE, S, SW, W, NW)

moveOrder = [Direction.N, Direction.S, Direction.W, Direction.E]

directionsToCheck = {
    Direction.N: (Direction.N, Direction.NE, Direction.NW),
    Direction.S: (Direction.S, Direction.SE, Direction.SW),
    Direction.W: (Direction.W, Direction.NW, Direction.SW),
    Direction.E: (Direction.E, Direction.NE, Direction.SE),
}


@dataclass
class Elf:
    position: Position
    move: Direction = field(default=Direction.NONE)


def occupied(location, deltas, positions):
    neigbouring = set([ (location.x + dx, location.y + dy) for (dx, dy) in deltas ])
    return len(positions.intersection(neigbouring)) != 0

def round(elves, roundNumber=1):
    positions = set([ astuple(elf.position) for elf in elves ])

    proposing = [ elf for elf in elves if occupied(elf.position, Direction.ALL, positions) ]    
    if len(proposing) == 0:
        return False

    counter = Counter()
    for elf in proposing:
        elf.move = Direction.NONE
        for attempt in range(Direction.COUNT):
            attemptedMove = moveOrder[(roundNumber - 1 + attempt) % Direction.COUNT]
            if not occupied(elf.position, directionsToCheck[attemptedMove], positions):
                elf.move = attemptedMove
                counter[( elf.position.x + attemptedMove[0], elf.position.y + attemptedMove[1])] += 1
                break

    movingElves = [ candidate for candidate in proposing if candidate.move != Direction.NONE ]
    if len(movingElves) == 0:
        return False

    for elf in movingElves:
        target = (elf.position.x + elf.move[0], elf.position.y + elf.move[1])
        if counter[target] == 1:
            elf.position = Position(*target)
    
    return True


def bounds(elves):
    minx = min([ elf.position.x for elf in elves ])
    miny = min([ elf.position.y for elf in elves ])
    maxx = max([ elf.position.x for elf in elves ])
    maxy = max([ elf.position.y for elf in elves ])
    return minx, miny, maxx, maxy

def print_elves(elves):
    minx, miny, maxx, maxy = bounds(elves)
    positions = set([ astuple(elf.position) for elf in elves ])

    for y in range(miny, maxy+1):
        for x in range(minx, maxx+1):
            print("#" if (x,y) in positions else ".", end="")
        print()

def main(args = ()):
    elves = []
    with open("day23.txt") as lines:
        for y, line in enumerate(lines):
            for x, ch in enumerate(line.strip()):
                if ch == "#":
                    elves.append(Elf(Position(x,y)))

    for number in range(10):
        round(elves, number + 1)

    # Find bounds
    minx, miny, maxx, maxy = bounds(elves)
    print("Part 1: Empty tiles:", (maxx-minx+1) * (maxy-miny+1) - len(elves))

    number = 10
    while round(elves, number + 1):
        number += 1

    print(f"Part 2: Round when no elf moves: {number + 1}")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
