import sys
from dataclasses import dataclass
from itertools import combinations
from collections import defaultdict

@dataclass
class Point3d:
    x: int
    y: int
    z: int

@dataclass
class Cube(Point3d):
    sidesVisible: int = 6

@dataclass
class Steam(Point3d):
    pass

def touching(a, b):
    return 1 == abs(a.x - b.x) + abs(a.y - b.y) + abs(a.z - b.z)

def part1(cubes):
    for a, b in combinations(cubes, 2):
        if touching(a, b):
            a.sidesVisible -= 1
            b.sidesVisible -= 1

    print("Part 1:", sum([ cube.sidesVisible for cube in cubes ]))

def part2(cubes):
    blocks = defaultdict(bool)
    for cube in cubes:
        blocks[(cube.x, cube.y, cube.z)] = True

    minx = min([ cube.x for cube in cubes ])
    miny = min([ cube.y for cube in cubes ])
    minz = min([ cube.z for cube in cubes ])
    maxx = max([ cube.x for cube in cubes ])
    maxy = max([ cube.y for cube in cubes ])
    maxz = max([ cube.z for cube in cubes ])

    air = set()
    frontier = [ Steam(0, 0, 0) ]

    while frontier:
        bubble = frontier.pop(0)
        air.add((bubble.x, bubble.y, bubble.z))

        for dx, dy, dz in ((0,0,1), (0,0,-1), (0,1,0), (0,-1,0), (1,0,0), (-1,0,0)):
            loc = (bubble.x + dx, bubble.y + dy, bubble.z + dz)
            cell = Steam(*loc)
            if loc not in air \
                and minx - 1 <= cell.x <= maxx + 1 and miny - 1 <= cell.y <= maxy + 1 and minz - 1 <= cell.z <= maxz + 1 \
                and not blocks[loc]:
                    air.add(loc)
                    frontier.append(cell)
    
    area = 0
    for loc in air:
        area += len([ cube for cube in cubes if touching(Steam(*loc), cube) ])
    print(f"Part 2: {area}")

def main(args = ()):
    cubes = []
    with open("day18.txt") as lines:
        for line in lines:
            x, y, z = map(int, line.split(","))
            cubes.append(Cube(x, y, z))

    part1(cubes)
    part2(cubes)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))