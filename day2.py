import sys

DRAW = 3
VICTORY = 6

stronger = {
    "A": "Y",
    "B": "Z",
    "C": "X",
}

weaker = {
    "A": "Z",
    "B": "X",
    "C": "Y",
}

matching = {
    "A": "X",
    "B": "Y",
    "C": "Z",
}

def main(args = ()):

    for part in (1,2):
        score = 0

        with open("day2.txt") as strategy:
            for line in strategy:
                line = line.strip()

                response = ""
                if part == 1:
                    if line in ("A X", "B Y", "C Z"):
                        score += DRAW
                    elif line in ("A Y", "B Z", "C X"):
                        score += VICTORY
                    response = line[-1]
                else:
                    if "X" in line:
                        response = weaker[line[0]]
                    elif "Y" in line:
                        score += DRAW
                        response = matching[line[0]]
                    else:
                        score += VICTORY
                        response = stronger[line[0]]
                
                score += " XYZ".find(response)
            print(f"Total player score in part {part}: {score}")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))