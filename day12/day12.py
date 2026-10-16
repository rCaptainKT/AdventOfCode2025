import sys
import os

FILLED = "#"
EMPTY = "."

def printgrid(grid):
    for row in grid:
        line = ""
        for char in row:
            line += char
        print(line)

def getshapesandregions(filename):
    shapes = dict()
    regions = list()
    with open(filename) as file:
        isshape = False
        shapeindex = 0
        shape = list()
        while True:
            line = file.readline()
            if not line:
                break
            line = line.strip()

            if isshape:
                if line == "":
                    isshape = False
                    shapes[shapeindex] = tuple(shape)
                    shape.clear()
                else:
                    shape.append(tuple(line))
            else:
                if line[-1] == ":":
                    isshape = True
                    shapeindex = int(line[:-1])
                else:
                    line = line.split()
                    line[0] = tuple(int(x) for x in line[0][:-1].split("x"))
                    line[1:] = [int(x) for x in line[1:]]
                    regions.append(tuple(line))

    return shapes, regions

def getshapearea(shape):
    area = 0
    for row in shape:
        for char in row:
            if char == FILLED:
                area += 1

    return area

def getshapeareas(shapes):
    shapeareas = dict()
    for i, shape in shapes.items():
        shapeareas[i] = getshapearea(shape)

    return shapeareas

def getshaperectareas(shapes):
    shaperectareas = dict()
    for i, shape in shapes.items():
        shaperectareas[i] = len(shape)*len(shape[0])
    
    return shaperectareas
    
def partone(filename):
    shapes, regions = getshapesandregions(filename)
    
    shapeareas = getshapeareas(shapes)
    possibleregions = list()
    for region in regions:
        regionarea = region[0][0]*region[0][1]
        neededshapearea = 0
        for i in range(1, len(region)):
            neededshapearea += shapeareas[i-1]*region[i]

        if regionarea >= neededshapearea:
            possibleregions.append(region)
            # print(region)
            # print(regionarea, neededshapearea)
    print(f"Possibly Solvable Regions: {len(possibleregions)}/{len(regions)}")

    shaperectareas = getshaperectareas(shapes)
    nontrivialpossibleregions = list()
    for region in possibleregions:
        regionarea = region[0][0]*region[0][1]
        neededshapearea = 0
        for i in range(1, len(region)):
            neededshapearea += shaperectareas[i-1]*region[i]
        
        if regionarea < neededshapearea:
            nontrivialpossibleregions.append(region)
            # print(region)
            # print(regionarea, neededshapearea)
    print(f"Non-Trivial Possibly Solvable Regions: {len(nontrivialpossibleregions)}/{len(regions)}")

def parttwo(filename):
    pass

def test(filename):
    pass

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # test(argv[1])
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: python3 day12.py [input]")
        sys.exit()
    
    main(argc, sys.argv)