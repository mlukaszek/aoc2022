import sys
from dataclasses import dataclass, astuple

@dataclass
class Point:
    x: int = 0
    y: int = 0

def snap(follower, leader):
    if abs(leader.x - follower.x) > 1 and abs(leader.y - follower.y) > 1:
        return Point(follower.x + 1 if leader.x - follower.x > 0 else follower.x - 1, follower.y + 1 if leader.y - follower.y > 0 else follower.y - 1)
    elif abs(leader.x - follower.x) > 1:
        return Point(follower.x + 1 if leader.x - follower.x > 0 else follower.x - 1, leader.y)
    elif abs(leader.y - follower.y) > 1:
        return Point(leader.x, follower.y + 1 if leader.y - follower.y > 0 else follower.y - 1)

def show(knots):
    xmin = min([ knot.x for knot in knots ])
    xmax = max([ knot.x for knot in knots ])
    ymin = min([ knot.y for knot in knots ])
    ymax = max([ knot.y for knot in knots ])
    for y in range(ymax+1, min(0, ymin) - 1, -1):
        for x in range(min(0, xmin), xmax+1):
            here = [ i for i, knot in enumerate(knots) if knot.x == x and knot.y == y ]
            show = '.' if len(here) == 0 else str(min(here))
            print(show if show != "0" else "H", end='')
        print()
    print(knots)
    print()

def main(args = ()):
    moves = { "U": (0,1), "D": (0,-1), "L": (-1,0), "R": (1,0) }

    for part in (1, 2):
        locations = set()
        knots = []
        for _ in range(2 if part == 1 else 10):
            knots.append(Point())
        locations.add(astuple(knots[-1]))

        with open("day9.txt") as lines:
            for line in lines:
                direction, steps = line.split()
                move = moves[direction]
                length = int(steps)

                #print("Making move:", line)

                for _ in range(length):
                    knots[0].x += move[0]
                    knots[0].y += move[1]
                    for i, knot in enumerate(knots):
                        previous = knots[i-1]
                        if i > 0 and (abs(knot.x - previous.x) > 1 or abs(knot.y - previous.y) > 1):
                            knots[i] = snap(knot, previous)
                    locations.add(astuple(knots[-1]))
                    #show(knots)
        print(f"Part {part}: the tail visited {len(locations)} positions.")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))