import sys
from collections import defaultdict
from dataclasses import dataclass, astuple
from copy import copy


@dataclass
class Point:
    x: int = 0
    y: int = 0


def connect(cave, points):
    for i, start in enumerate(points[:-1]):
        end = points[i+1]
        dx = end.x - start.x
        dy = end.y - start.y
        divider = max(abs(dx), abs(dy))
        ix = dx * 1.0 / divider
        iy = dy * 1.0 / divider
        while abs(end.x - start.x) != 0 or abs(end.y - start.y) != 0:
            cave[( round(start.x), round(start.y) )] = "#"
            start.x += ix
            start.y += iy
        cave[astuple(end)] = "#"


def produce_sand(cave, source, bottom, part):
    place = copy(source)

    if part == 2:
        bottom += 1

    while True:
        while cave[astuple(place)] not in ("#", "o"):
            place.y += 1

            # lower than the lowest rock?
            if place.y > bottom:
                if part == 1: # can't produce more
                    return False
                elif part == 2: # hit the floor
                    break

        # Can fall further, left or right?
        if cave[(place.x - 1, place.y)] not in ("#", "o") and place.y <= bottom:
            place.x -= 1
        elif cave[(place.x + 1, place.y)] not in ("#", "o") and place.y <= bottom:
            place.x += 1
        else:
            place.y -= 1
            cave[astuple(place)] = "o"
            break

    # Can keep producing until the source becomes blocked
    return place.y != source.y


def scan_cave(source):
    cave = defaultdict(lambda: ".")
    bottom = source.y

    with open("day14.txt") as lines:
        for line in lines:
            vertices = []
            for point in line.split(" -> "):
                x, y = [ int(v) for v in point.split(",") ]
                bottom = max(bottom, y)
                vertices.append(Point(x, y))
            connect(cave, vertices)
    return cave, bottom


def main(args = ()):
    source = Point(500, 0)

    for part in (1, 2):
        cave, bottom = scan_cave(source)

        units = 0
        while produce_sand(cave, source, bottom, part):
            units += 1
        
        if part == 2:
            units += 1
        
        print(f"Part {part}: produced {units} units of sand")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))