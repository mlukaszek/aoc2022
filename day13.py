import sys
from functools import cmp_to_key


def compare(left, right):
    if type(left) is list and type(right) is not list:
        return compare(left, [ right ])
    elif type(left) is not list and type(right) is list:
        return compare([ left ], right)

    for i in range(max(len(left), len(right))):
        try:
            leftItem = left[i]
        except IndexError:
            return True # Right side is smaller
        try:
            rightItem = right[i]
        except IndexError:
            return False # Right side is smaller

        if not all([ type(item) is int for item in (leftItem, rightItem) ]):
            res = compare(leftItem, rightItem)
            if res is None:
                continue
            else:
                return res
        
        # Both values are integers
        if leftItem > rightItem:
            return False
        elif leftItem < rightItem:
            return True
    # May return None if not determined

def part1():
    left, right = None, None
    ordered = 0
    pair = 0
    indices = 0

    with open("day13.txt") as lines:
        for line in lines:
            line = line.strip()
            if line == "":
                left = right = None
                continue
            if left is None:
                left = eval(line)
            else:
                right = eval(line)
            if left is not None and right is not None:
                pair += 1
                if compare(left, right):
                    ordered += 1
                    indices += pair

    print(f"\nOrdered pairs: {ordered}, sum of indices {indices}")


def part2():
    packets = []
    with open("day13.txt") as lines:
        for line in lines:
            if line == "\n":
                continue
            packets.append(eval(line))

    dividers = ( [[2]], [[6]] )
    packets.extend(dividers)

    decoder = 1
    for num, packet in enumerate(sorted(packets, key=cmp_to_key(lambda x, y: -1 if compare(x, y) else 1))):
        if packet in dividers:
            decoder *= (num + 1)

    print(f"Decoder key: {decoder}")


def main(args = ()):
    part1()
    part2()        


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))