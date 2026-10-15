import sys
import os

START_NODE = "you"
END_NODE = "out"

def getconnections(filename):
    connections = dict()
    with open(filename) as file:
        while True:
            line = file.readline().strip().split()
            if not line:
                break

            connections[line[0][:-1]] = tuple(line[1:])

    return connections

def _countpaths(connections, currentnode, endnode, visitednodes, cache):
    visitednodes[currentnode] = True

    if currentnode == endnode:
        if not cache.get(currentnode, False):
            cache[currentnode] = 1
        visitednodes[currentnode] = False
        return 1

    paths = 0
    for node in connections[currentnode]:
        if not visitednodes.get(node, False):
            # Node has not already been visited on current path
            if cache.get(node, False):
                # Cache entry exists for next node
                paths += cache[node]
            else:
                # Cache entry does not exist for next node
                paths += _countpaths(connections, node, endnode, visitednodes, cache)

    # Set cache
    cache[currentnode] = paths
    visitednodes[currentnode] = False
    return paths

def countpaths(connections, startnode, endnode):
    return _countpaths(connections, startnode, endnode, dict(), dict())

def partone(filename):
    connections = getconnections(filename)
    paths = countpaths(connections, START_NODE, END_NODE)
    print(f"There are {paths} different paths leading from '{START_NODE}' to '{END_NODE}'.")

def parttwo(filename):
    pass

def test():
    pass

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # test(argv[1])
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: python3 day11.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)