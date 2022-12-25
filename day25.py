import sys

BASE = 5

def main(args = ()):
    numbers = []
    with open("day25.txt") as lines:
        for line in lines:
            numbers.append(sum([ BASE ** position * ("=-0123".find(ch) - 2) for position, ch in enumerate(reversed(line.strip())) ]))

    result = sum(numbers)
    print("Sum in decimal:", result)

    lookup = {1: "1", 2: "2", 3: "=", 4: "-", 0: "0"}
    snafu = ""
    while result > 0:
        print(f"{result} % {BASE} = ", end="")
        digit = result % BASE
        print(digit)
        snafu = lookup[digit] + snafu        
        result //= BASE
        if lookup[digit] in "-=":
            result += 1
    print(snafu)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))