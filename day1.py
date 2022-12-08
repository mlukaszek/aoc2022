import sys
from collections import defaultdict

def main(args = ()):
    elf = 1
    sums = defaultdict(int)
    with open("day1.txt") as calories:
        for line in calories:
            line = line.strip()
            if line == "":
                elf += 1
                continue

            sums[elf] += int(line)

    print("The most calories carried by an elf is ", max(sums.values()))
    top3 = sorted(sums.values(), reverse=True)[:3]
    print("Total of top 3: ", sum(top3))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))