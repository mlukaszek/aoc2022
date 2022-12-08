import sys
from collections import defaultdict

prio = " abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ"

def main(args = ()):
    
    prios = 0
    with open("day3.txt") as lines:
        for line in lines:
            line = line.strip()
            middle = int(len(line) / 2)
            left = set(line[:middle])
            right = set(line[middle:])
            common = list(left.intersection(right))[0]
            prios += prio.find(common)
    print(f"Sum of priorities for part 1 is {prios}")

    prios = 0
    with open("day3.txt") as lines:
        group = []
        for line in lines:
            group.append(set(line.strip()))
            if len(group) == 3:
                common = list(group[0].intersection(group[1]).intersection(group[2]))[0]
                prios += prio.find(common)
                group.clear()
    print(f"Sum of priorities for part 2 is {prios}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))