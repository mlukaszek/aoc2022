import sys
from functools import reduce
from operator import mul

def is_visible(location, trees, maxX, maxY):
    x, y = location
    if x == 0 or y == 0 or x == maxX or y == maxY:
        return True
    height = trees[location]
    if all([ trees[(column, y)] < height for column in range(0, x) ]) \
    or all([ trees[(column, y)] < height for column in range(maxX, x, -1) ]) \
    or all([ trees[(x, row)] < height for row in range(0, y) ]) \
    or all([ trees[(x, row)] < height for row in range(maxY, y, -1) ]):
        return True
    return False

def scenic_score(trees, maxX, maxY):
    scores = {}
    for location in trees.keys():
        height = trees[location]
        
        scores[location] = []
        for dx, dy in ((0,1), (1,0), (0,-1), (-1,0)):
            x, y = location
            score = 0
            while 0 <= x <= maxX and 0 <= y <= maxY:
                x += dx
                y += dy
                if x < 0 or y < 0 or x > maxX or y > maxY:
                    continue
                if trees[(x,y)] <= height:
                    score += 1
                if trees[(x,y)] == height:
                    break
            scores[location].append(score)
        scores[location] = reduce(mul, scores[location])
    return scores

def main(args = ()):
    trees = {}
    maxX, maxY = 0, 0
    with open("day8.txt") as lines:
        for y, line in enumerate(lines):
            for x, number in enumerate(line.strip()):
                trees[(x,y)] = int(number)
                maxX = max(maxX, x)
                maxY = max(maxY, y)

    print("Visible trees:", len([ height for location, height in trees.items() if is_visible(location, trees, maxX, maxY) ]))

    scores = scenic_score(trees, maxX, maxY)
    print("Maximum scenic score:", max(scores.values()))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))