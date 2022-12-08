import sys
import re

def main(args = ()):
    
    contained = 0
    overlapping = 0

    with open("day4.txt") as lines:
        for line in lines:
            line = line.strip()
            l1,r1,l2,r2 = [ int(v) for v in re.findall(r"(\d+)-(\d+),(\d+)-(\d+)", line)[0] ]

            if (l1 <= l2 and r1 >= r2) or (l1 >= l2 and r1 <= r2):
                contained += 1

            if (l2 <= r1 and r2 >= l1):
                overlapping +=1

    print("Assignment pairs fully contained in the other:", contained)
    print("Overlapping assignments:", overlapping)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))