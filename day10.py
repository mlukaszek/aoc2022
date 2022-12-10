import sys

# I was expecting multi-core processing necessary in part 2 :)

def execute(cores, cycle, reg):
    for i, core in enumerate(cores):
        due, operation = core
        if cycle == due:
            cores[i] = None
            operand = operation[0]
            if operand == "addx":
                reg["X"] += int(operation[-1])

def main(args = ()):

    reg = {
        "X": 1,
    }

    cycle = 0
    cores = [ None ]
    strength = 0

    screen = {}
    WIDTH = 40
    HEIGHT = 6

    with open("day10.txt") as lines:
        for line in lines:
            # Fetch
            if "addx" in line:
                cores[0] = cycle + 2, ["addx", int(line.split()[-1])]
            elif "noop" in line:
                cores[0] = cycle + 1, ["noop"]
            
            while cores[0] != None:
                # Draw pixel?
                x = cycle % WIDTH
                y = cycle // WIDTH
                screen[(x, y)] = '#' if abs(reg["X"] - x) < 2 else '.'

                cycle += 1

                # Inspect value of X during certain cycles
                if cycle in (20, 60, 100, 140, 180, 220):
                    strength += cycle * reg["X"]

                execute(cores, cycle, reg)
        
    print(f"Sum of signal strengths: {strength}")

    for y in range(HEIGHT):
        for x in range(WIDTH):
            print(screen[x,y], end='')
        print()

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))