import sys
import os

YOU_NODE = "you"
OUT_NODE = "out"
SERVER_RACK = "svr"
DIGITAL_ANALOG_CONVERTER = "dac"
FAST_FOURIER_TRANSFORM = "fft"

def getconnections(filename):
    connections = dict()
    with open(filename) as file:
        while True:
            line = file.readline().strip().split()
            if not line:
                break

            connections[line[0][:-1]] = tuple(line[1:])

    return connections

def _countpaths(connections, currentnode, endnode, bannednodes, visitednodes, cache):
    # print(f"CURRENT: {currentnode}")
    visitednodes[currentnode] = True

    if currentnode == endnode:
        cache[currentnode] = 1
        visitednodes[currentnode] = False
        return 1
    elif currentnode in bannednodes:
        cache[currentnode] = 0
        visitednodes[currentnode] = False
        return 0

    paths = 0
    for node in connections.get(currentnode, tuple()):
        # print(f"NEXT: {node}")
        if not visitednodes.get(node, False):
            # Node has not already been visited on current path

            # print(f"Cache Result: {cache.get(node)}")
            if cache.get(node) is None:
                # Cache entry does not exist for next node
                paths += _countpaths(connections, node, endnode, bannednodes, visitednodes, cache)
            else:
                # Cache entry exists for next node
                paths += cache[node]
            # print(f"RETURNING: {currentnode}")

    # Set cache
    cache[currentnode] = paths
    # print(f"{currentnode} CACHE SET: {cache[currentnode]}")
    visitednodes[currentnode] = False
    return paths

def countpaths(connections, startnode, endnode, bannednodes = []):
    cache = dict()
    result = _countpaths(connections, startnode, endnode, bannednodes, dict(), cache)
    # print(cache)

    return result

def partone(filename):
    connections = getconnections(filename)
    paths = countpaths(connections, YOU_NODE, OUT_NODE)
    print(f"There are {paths} different paths leading from '{YOU_NODE}' to '{OUT_NODE}'.")

def parttwo(filename):
    connections = getconnections(filename)
    paths = 0

    # Route one
    dactofft = countpaths(connections, DIGITAL_ANALOG_CONVERTER, FAST_FOURIER_TRANSFORM, [SERVER_RACK])
    if dactofft != 0:
        svrtodac = countpaths(connections, SERVER_RACK, DIGITAL_ANALOG_CONVERTER, [FAST_FOURIER_TRANSFORM])
        ffttoout = countpaths(connections, FAST_FOURIER_TRANSFORM, OUT_NODE, [SERVER_RACK, DIGITAL_ANALOG_CONVERTER])
        paths += svrtodac*dactofft*ffttoout    

    # Route two
    ffttodac = countpaths(connections, FAST_FOURIER_TRANSFORM, DIGITAL_ANALOG_CONVERTER, [SERVER_RACK])
    if ffttodac != 0:
        svrtofft = countpaths(connections, SERVER_RACK, FAST_FOURIER_TRANSFORM, [DIGITAL_ANALOG_CONVERTER])
        dactoout = countpaths(connections, DIGITAL_ANALOG_CONVERTER, OUT_NODE, [SERVER_RACK, FAST_FOURIER_TRANSFORM])
        paths += svrtofft*ffttodac*dactoout

    print(f"There are {paths} different paths leading from '{SERVER_RACK}' to '{OUT_NODE}' that visit both '{DIGITAL_ANALOG_CONVERTER}' and '{FAST_FOURIER_TRANSFORM}'.")

def test(filename):
    connections = getconnections(filename)
    dactofft = countpaths(connections, DIGITAL_ANALOG_CONVERTER, FAST_FOURIER_TRANSFORM, [SERVER_RACK])
    print(f"dactofft: {dactofft}")

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

    main(argc, sys.argv)