import sys, re

def rearrange(part):

    # Don't have time to invent parsing logic for this...
    stacks = ["",
        "WPGZVSB",
        "FZCBVJ",
        "CDZNHMLV",
        "BJFPZMDL",
        "HQBJGCFV",
        "BLSTQFG",
        "VZCGL",
        "GLN",
        "CHFJ"
    ]

    with open("day5.txt") as lines:
        for line in lines:
            line = line.strip()
            if "move" not in line:
                continue

            count, source, destination = [ int(v) for v in re.findall(r"move (\d+) from (\d) to (\d)", line)[0] ]
            selection = stacks[source][:count]
            stacks[source] = stacks[source].removeprefix(selection)
            stacks[destination] = (selection[::-1] if part == 1 else selection) + stacks[destination]

    print(f'Part {part}: ' + ''.join([ stack[0] for stack in stacks[1:] ]))


def main(args = ()):

#         [C] [B] [H]                
# [W]     [D] [J] [Q] [B]            
# [P] [F] [Z] [F] [B] [L]            
# [G] [Z] [N] [P] [J] [S] [V]        
# [Z] [C] [H] [Z] [G] [T] [Z]     [C]
# [V] [B] [M] [M] [C] [Q] [C] [G] [H]
# [S] [V] [L] [D] [F] [F] [G] [L] [F]
# [B] [J] [V] [L] [V] [G] [L] [N] [J]
#  1   2   3   4   5   6   7   8   9 

    for part in (1, 2):
        rearrange(part)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))