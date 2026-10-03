import sys
import os

def gettiles(filename):
    tiles = dict()
    with open(filename) as file:
        i = 0
        while True:
            line = file.readline().strip()
            if not line:
                break

            line = line.split(",")
            tiles[i] = (int(line[0]), int(line[1]))
            i += 1

    return tiles

def getarea(coords1, coords2):
    return (abs(coords1[0]-coords2[0])+1)*(abs(coords1[1]-coords2[1])+1)

def calculateareas(tiles):
    areas = list()
    for i in range(len(tiles.keys())):
        for j in range(i+1, len(tiles.keys())):
            areas.append((f"{i}-{j}", getarea(tiles[i], tiles[j])))
    
    areas.sort(key=lambda x: x[1])
    return areas

def getareatileids(key):
    key = key.split("-")
    return (int(key[0]), int(key[1]))

def partone(filename):
    tiles = gettiles(filename)
    areas = calculateareas(tiles)
    print(f"The largest area of any rectangle you can make is {areas[-1][1]}.")

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
        print(f"Usage: python3 day09.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)