import sys
import os

START = "S"
EMPTY = "."
SPLITTER = "^"
BEAM = "|"

def printgrid(grid):
    for i in range(len(grid)):
        line = ""
        for j in range(len(grid[i])):
            line += str(grid[i][j])
        print(line)

def getgrid(filename):
    grid = list()
    with open(filename) as file:
        row = list()
        while True:
            char = file.read(1)
            if not char:
                break
            elif char == "\n":
                grid.append(row)
                row = list()
            else:
                row.append(char)

    return grid

def propagatebeam(grid):
    splits = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == START or grid[i][j] == BEAM:
                if i+1 < len(grid):
                    if grid[i+1][j] == EMPTY:
                        # Propagate beam
                        grid[i+1][j] = BEAM
                    elif grid[i+1][j] == SPLITTER:
                        # Split beam
                        hasSplit = False
                        if j-1 > -1 and grid[i+1][j-1] == EMPTY:
                            grid[i+1][j-1] = BEAM
                            hasSplit = True
                        if j+1 < len(grid[i]) and grid[i+1][j+1] == EMPTY:
                            grid[i+1][j+1] = BEAM
                            hasSplit = True
                        if hasSplit:
                            splits += 1

    return splits

def partone(filename):
    grid = getgrid(filename)
    splits = propagatebeam(grid)
    # printgrid(grid)
    print(f"The beam will be split {splits} times.")

def _counttimelines(grid, cache):
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == START or grid[i][j] == BEAM:
                if i+1 < len(grid):
                    if grid[i+1][j] == BEAM:
                        # Propagate timeline
                        cache[i+1][j] += cache[i][j]
                    elif grid[i+1][j] == SPLITTER:
                        # Split timeline
                        if j-1 > -1 and grid[i+1][j-1] == BEAM:
                            cache[i+1][j-1] += cache[i][j]
                        if j+1 < len(grid[i]) and grid[i+1][j+1] == BEAM:
                            cache[i+1][j+1] += cache[i][j]

def counttimelines(grid):
    startcol = 0
    while True:
        if grid[0][startcol] == START:
            break
        else:
            startcol += 1
    
    cache = list()
    for i in range(len(grid)):
        cache.append([0]*len(grid[i]))
    cache[0][startcol] = 1

    _counttimelines(grid, cache)

    return sum(cache[-1])

def parttwo(filename):
    grid = getgrid(filename)
    propagatebeam(grid)
    timelines = counttimelines(grid)
    print(f"A single tachyon particle would end up on {timelines} timelines.")

def test():
    pass

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: python3 day07.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)