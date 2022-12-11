import sys
from functools import reduce
from operator import mul
import math

class Monkey:
    def __init__(self) -> None:
        self.items = []
        self.operation = ""
        self.inspect = lambda item: item
        self.test = 0
        self.on_test_passed = 0
        self.on_test_failed = 0
        self.inspections = 0

def read_input(lines):
    monkeys = []

    for line in lines:
        line = line.strip()
        if "Monkey" in line:
            monkeys.append(Monkey())
        elif "Starting items" in line:
            monkeys[-1].items = [ int(v) for v in line.split(": ")[1].split(",") ]
        elif "Operation" in line:
            monkeys[-1].operation = line.split(" = ")[1]
            if monkeys[-1].operation == "old + old":
                monkeys[-1].inspect = lambda _, item: item + item
            elif monkeys[-1].operation == "old * old":
                monkeys[-1].inspect = lambda _, item: item * item
            elif "*" in monkeys[-1].operation:
                monkeys[-1].inspect = lambda self, item: item * int(self.operation.split(" * ")[1])
            elif "+" in monkeys[-1].operation:
                monkeys[-1].inspect = lambda self, item: item + int(self.operation.split(" + ")[1])
        elif "Test" in line:
            monkeys[-1].test = int(line.split()[-1])
        elif "If true" in line:
            monkeys[-1].on_test_passed = int(line.split()[-1])
        elif "If false" in line:
            monkeys[-1].on_test_failed = int(line.split()[-1])
    return monkeys

def main(args = ()):
    for part in (1, 2):
        monkeys = {}
        with open("day11.txt") as lines:
            monkeys = read_input(lines)
        
        lcm = 1
        for monkey in monkeys:
            lcm = math.lcm(lcm, monkey.test)

        for round in range(20 if part == 1 else 10000):
            for number in range(len(monkeys)):
                monkey = monkeys[number]
                while monkey.items:
                    item = monkey.items.pop(0)
                    item = monkey.inspect(monkey, item)
                    monkey.inspections += 1
                    if part == 1:
                        item //= 3
                    recipient = monkey.on_test_passed if item % monkey.test == 0 else monkey.on_test_failed
                    monkeys[recipient].items.append(item % lcm)
                    
        print(f"Part {part}: Level of monkey bussiness:", reduce(mul, sorted([ monkey.inspections for monkey in monkeys ], reverse=True)[:2]))

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))