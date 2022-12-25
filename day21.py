import sys
from tqdm import trange

def value(monkeys, monkey, humn = None):
    if monkey == "humn" and humn is not None:
        return humn
    elif monkeys[monkey].isnumeric():
        return int(monkeys[monkey])
    else:
        lhs, operator, rhs = monkeys[monkey].split(" ")
        leftValue = value(monkeys, lhs, humn)
        rightValue = value(monkeys, rhs, humn)
        if operator == "+":
            return leftValue + rightValue
        elif operator == "-":
            return leftValue - rightValue
        elif operator == "*":
            return leftValue * rightValue
        elif operator == "/":
            return leftValue // rightValue
        elif operator == "=":
            return leftValue == rightValue

def main(args = ()):
    monkeys = {}
    with open("day21.txt") as lines:
        for line in lines:
            monkey, job = line.strip().split(": ")
            monkeys[monkey] = job

    # Part 1
    print("root: ", value(monkeys, "root", None))

    # Part 2
    # binary search, possible if the root monkey subtracts rather than compares
    monkeys["root"] = monkeys["root"].replace("+", "-")

    left = -1_000_000_000_000_000
    right = 1_000_000_000_000_000
    root = value(monkeys, "root", left)
    if root > 0:
        left, right = right, left

    while True:
        guess = left + (right - left) / 2
        root = value(monkeys, "root", int(guess))
        if root < 0:
            left = guess
        elif root > 0:
            right = guess
        else:
            print("humn:", int(guess))
            break

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))