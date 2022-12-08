import sys
from dataclasses import dataclass, field
from enum import Enum

class NodeType(Enum):
    FILE = "f"
    DIR = "d"

@dataclass
class Node:
    name: str
    parent: str
    type: NodeType = NodeType.DIR
    children: list = field(default_factory=list)
    size: int = 0

def update_parents(fs, cwd, size):
    fs[cwd].size += size
    if fs[cwd].parent is not None:
        update_parents(fs, fs[cwd].parent, size)

def walk(fs, root, filter):
    ret = set()
    if filter(fs[root]):
        ret.add(root)
    for node in fs[root].children:
        if filter(fs[node]):
            ret.add(node)
        if fs[node].type == NodeType.DIR:
            ret.update(walk(fs, node, filter))
    return ret

def main(args = ()):
    
    cwd = None
    fs =  { "/": Node("/", parent=None) }

    with open("day7.txt") as lines:
        for line in lines:
            if line.startswith('$ cd'):
                destination = line.split()[2]
                if destination == ".." and cwd != "/": # FIXME - why need the 2nd condition?
                    cwd = fs[cwd].parent
                else:
                    target = destination if destination.startswith('/') else cwd.rstrip('/') + '/' + destination
                    cwd = target
            elif line.startswith("$ ls"):
                pass
            elif line.startswith("dir"):
                _, name = line.split()
                target = '/' + name if cwd == '/' else cwd + '/' + name
                fs[target] = Node(name=target, parent=cwd)
                fs[cwd].children.append(target)
            else: # file
                size, name = line.split()
                target = '/' + name if cwd == '/' else cwd + '/' + name
                fs[target] = Node(name=target, parent=cwd, type=NodeType.FILE, size=int(size))
                fs[cwd].children.append(target)
                update_parents(fs, target, int(size))
    
    # Part One
    matching = walk(fs, "/", lambda node: node.type == NodeType.DIR and node.size <= 100000)
    print("Sum of total sizes of directories <= 100000: ", sum([ fs[node].size for node in matching ]))

    # Part Two
    total = 70000000
    needed = 30000000
    used = fs["/"].size
    free = total - used
    print(f"Used {used} of total {total} - {free} free")

    toFree = needed - free
    print(f"Need to free at least {toFree}")

    dirs = [ (node, fs[node].size) for node in sorted(walk(fs, "/", lambda node: node.type == NodeType.DIR and node.size >= toFree), key=lambda node: fs[node].size) ]
    print("Best to delete: ", dirs[0], "leaving", dirs[0][1] + free, "free.")

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))