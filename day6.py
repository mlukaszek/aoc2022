import sys
from collections import Counter

def detect(blocklen):
    counter = Counter()

    buffer = ""
    with open("day6.txt") as lines:
        buffer = lines.readline().strip()

    marker = ""
    for ch in buffer:
        counter[ch] += 1
        marker += ch
        if len(marker) > blocklen:
            marker = marker[1:]
        if len(marker) == blocklen:
            counts = Counter(marker)
            if len(list(counts.elements())) == len(set(counts.elements())):
                print(f"Found {marker} after processing:", blocklen + buffer.index(marker))
                break

def main(args = ()):
    detect(4)
    detect(14)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))