import sys
import os

EMPTY = "."
ROLL = "@"

def getfloor(filename):
    floor = list()
    with open(filename) as file:
        while True:
            line = file.readline().strip()
            if not line:
                break

            row = list()
            for char in line:
                row.append(char)
            floor.append(row)

    return floor

def checkneighbours(floor, row, col):
    neighbours = 0
    for i in range(row-1, row+2):
        for j in range(col-1, col+2):
            if i == row and j == col:
                # Tile being checked
                continue
            elif i < 0 or i > len(floor)-1:
                # Row out of bounds
                continue
            elif j < 0 or j > len(floor[row])-1:
                # Col out of bounds
                continue

            if floor[i][j] == ROLL:
                neighbours += 1

    return neighbours

def partone(filename):
    rolls = 0
    floor = getfloor(filename)

    for i in range(len(floor)):
        for j in range(len(floor[i])):
            if floor[i][j] == EMPTY:
                continue
            elif floor[i][j] == ROLL:
                if checkneighbours(floor, i, j) < 4:
                    rolls += 1

    print(f"Number of rolls accessible by forklift is {rolls}.")

def parttwo(filename):
    pass

def test():
    pass

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: python3 day04.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)