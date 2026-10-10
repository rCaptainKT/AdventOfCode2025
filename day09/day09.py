import sys
import os

EMPTY = "."
RED_TILE = "#"
GREEN_TILE = "X"

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

def printgrid(grid):
    for row in grid:
        line = ""
        for char in row:
            line += char
        print(line)

def fillgreentiles(greentiles):
    for i in range(len(greentiles)):
        crossed = 0
        for j in range(len(greentiles[i])):
            if (greentiles[i][j] == RED_TILE or greentiles[i][j] == GREEN_TILE) and j-1 > 0 and (greentiles[i][j-1] != RED_TILE and greentiles[i][j-1] != GREEN_TILE):
                crossed += 1
            elif crossed%2 and greentiles[i][j] == EMPTY:
                greentiles[i][j] = GREEN_TILE

def getgreentiles(tiles):
    coords = [x for x in tiles.values()]
    maxx = max([x[0] for x in coords])
    maxy = max([x[1] for x in coords])

    greentiles = list()
    for i in range(maxy+1):
        row = list()
        for j in range(maxx+1):
            if (j, i) in coords:
                row.append(RED_TILE)
            else:
                row.append(EMPTY)
        greentiles.append(row)

    for i in range(len(coords)):
        if i == len(coords)-1:
            secondcoordindex = 0
        else:    
            secondcoordindex = i+1

        if coords[i][0] == coords[secondcoordindex][0]:
            # Vertical line
            if coords[i][1] > coords[secondcoordindex][1]:
                for j in range(coords[secondcoordindex][1]+1, coords[i][1]):
                    greentiles[j][coords[i][0]] = GREEN_TILE
            else:
                for j in range(coords[i][1]+1, coords[secondcoordindex][1]):
                    greentiles[j][coords[i][0]] = GREEN_TILE
        elif coords[i][1] == coords[secondcoordindex][1]:
            # Horizontal line
            if coords[i][0] > coords[secondcoordindex][0]:
                for j in range(coords[secondcoordindex][0]+1, coords[i][0]):
                    greentiles[coords[i][1]][j] = GREEN_TILE
            else:
                for j in range(coords[i][0]+1, coords[secondcoordindex][0]):
                    greentiles[coords[i][1]][j] = GREEN_TILE        

    return greentiles

def getboundarylines(tiles):
    boundarylines = list()
    coords = [coord for coord in tiles.values()]
    for i in range(len(tiles)):
        if i == len(tiles)-1:
            nexti = 0
        else:
            nexti = i+1

        if coords[i][1] == coords[nexti][1]:
            # Horizontal line
            boundarylines.append((coords[i], coords[nexti], "H"))
        elif coords[i][0] == coords[nexti][0]:
            # Vertical line
            boundarylines.append((coords[i], coords[nexti], "V"))

    return boundarylines

def getboundaryrotation(tiles):
    """
    Find the vertex with smallest y (and largest x if there are ties). 
    Let the vertex be A and the previous vertex in the list be B and the next vertex in the list be C. 
    Now compute the sign of the cross product of AB and AC.
    https://stackoverflow.com/questions/1165647/how-to-determine-if-a-list-of-polygon-points-are-in-clockwise-order

    https://en.wikipedia.org/wiki/Curve_orientation
    """
    vertices = [(i, v) for i,v in tiles.items()]
    vertices.sort(key=lambda v: (v[1][0], -v[1][1]))
    bindex = vertices[0][0]
    
    b = tiles[bindex]
    if bindex-1 < 0:
        a = tiles[len(tiles.keys())-1]
    else:
        a = tiles[bindex-1]
    if bindex+1 > len(tiles.keys())-1:
        c = tiles[0]
    else:
        c = tiles[bindex+1]

    det = (b[0]*c[1]+a[0]*b[1]+a[1]*c[0])-(a[1]*b[0]+b[1]*c[0]+a[0]*c[1])

    # Results here are inverted to account for grid used to store tile information is mirrored on y-axis
    if det > 0:
        return "CW" # Normally would be CCW
    elif det < 0:
        return "CCW" # Normally would be CW
    else:
        raise RuntimeError("Points are collinear.")

def getrectlines(tile1, tile2, rotation):
    rectlines = list()
    minrow = min(tile1[1], tile2[1])
    maxrow = max(tile1[1], tile2[1])
    mincol = min(tile1[0], tile2[0])
    maxcol = max(tile1[0], tile2[0])

    if rotation == "CW":
        rectlines.append(((mincol, minrow), (maxcol, minrow), "H"))
        rectlines.append(((maxcol, minrow), (maxcol, maxrow), "V"))
        rectlines.append(((maxcol, maxrow), (mincol, maxrow), "H"))
        rectlines.append(((mincol, maxrow), (mincol, minrow), "V"))
    elif rotation == "CCW":
        rectlines.append(((mincol, minrow), (mincol, maxrow), "V"))
        rectlines.append(((mincol, maxrow), (maxcol, maxrow), "H"))
        rectlines.append(((maxcol, maxrow), (maxcol, minrow), "V"))
        rectlines.append(((maxcol, minrow), (mincol, minrow), "H"))

    return rectlines

def checklinecollision(boundarylines, rectlines):
    for line in rectlines:
        for boundaryline in boundarylines:
            if line[2] == boundaryline[2]:
                continue
            elif line[2] == "H" and boundaryline[2] == "V":
                # Horizontal line collision
                boundarycol = boundaryline[0][0]
                mincol = min(line[0][0], line[1][0])
                maxcol = max(line[0][0], line[1][0])
                colcheck = boundarycol > mincol and boundarycol < maxcol

                linerow = line[0][1]
                minrow = min(boundaryline[0][1], boundaryline[1][1])
                maxrow = max(boundaryline[0][1], boundaryline[1][1])
                rowcheck = linerow > minrow and linerow < maxrow

                if colcheck and rowcheck:
                    return False      
            elif line[2] == "V" and boundaryline[2] == "H":
                # Vertical line collision
                boundaryrow = boundaryline[0][1]
                minrow = min(line[0][1], line[1][1])
                maxrow = max(line[0][1], line[1][1])
                rowcheck = boundaryrow > minrow and boundaryrow < maxrow

                linecol = line[0][0]
                mincol = min(boundaryline[0][0], boundaryline[1][0])
                maxcol = max(boundaryline[0][0], boundaryline[1][0])
                colcheck = linecol > mincol and linecol < maxcol

                if colcheck and rowcheck:
                    return False
    
    return True

def getlinechangesign(line):
    if line[2] == "H":
        if line[0][0] < line[1][0]:
            return "+"
        elif line[0][0] > line[1][0]:
            return "-"
    elif line[2] == "V":
        if line[0][1] < line[1][1]:
            return "+"
        elif line[0][1] > line[1][1]:
            return "-"

def checklinerotations(boundarylines, rectlines):
    for rectline in rectlines:
        for boundaryline in boundarylines:
            if rectline[2] == boundaryline[2]:
                # Lines have same orientation
                if rectline[2] == "H" and rectline[0][1] == boundaryline[0][1]:
                    # Lines are horizontal and on same row
                    boundarymin = min(boundaryline[0][0], boundaryline[1][0])
                    boundarymax = max(boundaryline[0][0], boundaryline[1][0])
                    rectcol1 = rectline[0][0]
                    rectcol2 = rectline[1][0]

                    if (rectcol1 >= boundarymin and rectcol1 <= boundarymax) or (rectcol2 >= boundarymin and rectcol2 <= boundarymax):
                        # Lines overlap
                        if getlinechangesign(rectline) != getlinechangesign(boundaryline):
                            # Lines run in opposite direction
                            return False
                elif rectline[2] == "V" and rectline[0][0] == boundaryline[0][0]:
                    # Lines are vertical and on same col
                    boundarymin = min(boundaryline[0][1], boundaryline[1][1])
                    boundarymax = max(boundaryline[0][1], boundaryline[1][1])
                    rectrow1 = rectline[0][1]
                    rectrow2 = rectline[1][1]

                    if (rectrow1 >= boundarymin and rectrow1 <= boundarymax) or (rectrow2 >= boundarymin and rectrow2 <= boundarymax):
                        # Lines overlap
                        if getlinechangesign(rectline) != getlinechangesign(boundaryline):
                            # Lines run in opposite direction
                            return False

    return True

def checklinecollision(boundarylines, rectlines):
    for line in rectlines:
        for boundaryline in boundarylines:
            if line[2] == boundaryline[2]:
                continue
            elif line[2] == "H" and boundaryline[2] == "V":
                # Horizontal line collision
                boundarycol = boundaryline[0][0]
                mincol = min(line[0][0], line[1][0])
                maxcol = max(line[0][0], line[1][0])
                colcheck = boundarycol > mincol and boundarycol < maxcol

                linerow = line[0][1]
                minrow = min(boundaryline[0][1], boundaryline[1][1])
                maxrow = max(boundaryline[0][1], boundaryline[1][1])
                rowcheck = linerow > minrow and linerow < maxrow

                if colcheck and rowcheck:
                    return False      
            elif line[2] == "V" and boundaryline[2] == "H":
                # Vertical line collision
                boundaryrow = boundaryline[0][1]
                minrow = min(line[0][1], line[1][1])
                maxrow = max(line[0][1], line[1][1])
                rowcheck = boundaryrow > minrow and boundaryrow < maxrow

                linecol = line[0][0]
                mincol = min(boundaryline[0][0], boundaryline[1][0])
                maxcol = max(boundaryline[0][0], boundaryline[1][0])
                colcheck = linecol > mincol and linecol < maxcol

                if colcheck and rowcheck:
                    return False
    
    return True

def checkbounds(tile1, tile2, boundarylines):
    for line in boundarylines:
        if (line[0] == tile1 and line[1] == tile2) or (line[0] == tile2 and line[1] == tile1):
            return True

    minrow = min(tile1[1], tile2[1])
    maxrow = max(tile1[1], tile2[1])
    mincol = min(tile1[0], tile2[0])
    maxcol = max(tile1[0], tile2[0])

def getcompressionkeys(tiles):
    rowset = set()
    colset = set()

    for tile in tiles.values():
        rowset.add(tile[1])
        colset.add(tile[0])

    rowset = sorted(list(rowset))
    temp = list()
    for i in range(len(rowset)-1):
        temp.append((rowset[i] + rowset[i+1])/2)
    rowset += temp
    rowset.sort()

    colset = sorted(list(colset))
    temp.clear()
    for i in range(len(colset)-1):
        temp.append((colset[i] + colset[i+1])/2)
    colset += temp
    colset.sort()

    rowcompressionkey = dict()
    for i in range(len(rowset)):
        rowcompressionkey[rowset[i]] = i 

    colcompressionkey = dict()
    for i in range(len(colset)):
        colcompressionkey[colset[i]] = i

    return rowcompressionkey, colcompressionkey

def fillcompressedgrid(compressedgrid):
    for i in range(len(compressedgrid)):
        crossed = 0
        for j in range(len(compressedgrid[i])):
            if (compressedgrid[i][j] == RED_TILE or compressedgrid[i][j] == GREEN_TILE):
                if j-1 > 0 and (compressedgrid[i][j-1] != RED_TILE and compressedgrid[i][j-1] != GREEN_TILE):
                    crossed += 1
                else:
                    crossed += 1
            elif crossed%2 and compressedgrid[i][j] == EMPTY:
                compressedgrid[i][j] = GREEN_TILE

def getcompressedgrid(tiles, rowcompressionkey, colcompressionkey):
    compressedgrid = list()
    for _ in range(len(rowcompressionkey.values())):
        compressedgrid.append([EMPTY]*len(colcompressionkey.values()))

    coords = list(tiles.values())
    for tile in coords:
        compressedgrid[rowcompressionkey[tile[1]]][colcompressionkey[tile[0]]] = RED_TILE

    for i in range(len(coords)):
        compressedrowindex1 = rowcompressionkey[coords[i][1]]
        compressedcolindex1 = colcompressionkey[coords[i][0]]
        if i == len(coords)-1:
            compressedrowindex2 = rowcompressionkey[coords[0][1]]
            compressedcolindex2 = colcompressionkey[coords[0][0]]
        else:    
            compressedrowindex2 = rowcompressionkey[coords[i+1][1]]
            compressedcolindex2 = colcompressionkey[coords[i+1][0]]

        if compressedcolindex1 == compressedcolindex2:
            # Vertical line
            for j in range(min(compressedrowindex1, compressedrowindex2)+1, max(compressedrowindex1, compressedrowindex2)):
                compressedgrid[j][compressedcolindex1] = GREEN_TILE
        elif compressedrowindex1 == compressedrowindex2:
            # Horizontal line
            for j in range(min(compressedcolindex1, compressedcolindex2)+1, max(compressedcolindex1, compressedcolindex2)):
                compressedgrid[compressedrowindex1][j] = GREEN_TILE

    fillcompressedgrid(compressedgrid)
    return compressedgrid

def gettileidsfromkey(key):
    key = key.split("-")
    return (int(key[0]), int(key[1]))

def findlargestvalidrectarea(tiles, rowcompressionkey, colcompressionkey, compressedgrid):
    areas = calculateareas(tiles)
    areas.reverse()

    for area in areas:
        ids = gettileidsfromkey(area[0])
        tile1 = tiles[ids[0]]
        tile2 = tiles[ids[1]]
        tile1compressedrow = rowcompressionkey[tile1[1]]
        tile1compressedcol = colcompressionkey[tile1[0]]
        tile2compressedrow = rowcompressionkey[tile2[1]]
        tile2compressedcol = colcompressionkey[tile2[0]]

        valid = True
        for i in range(min(tile1compressedrow, tile2compressedrow), max(tile1compressedrow, tile2compressedrow)+1):
            for j in range(min(tile1compressedcol, tile2compressedcol), max(tile1compressedcol, tile2compressedcol)+1):
                if compressedgrid[i][j] == EMPTY:
                    valid = False
                    break
            if valid == False:
                break

        if valid:
            return area[1]

def parttwo(filename):
    tiles = gettiles(filename)
    rowcompressionkey, colcompressionkey = getcompressionkeys(tiles)
    compressedgrid = getcompressedgrid(tiles, rowcompressionkey, colcompressionkey)

    # with open("output.txt", "w") as file:
    #     for row in compressedgrid:
    #         line = ""
    #         for char in row:
    #             line += char
    #         file.write(f"{line}\n")
    
    area = findlargestvalidrectarea(tiles, rowcompressionkey, colcompressionkey, compressedgrid)
    print(f"The largest area of any rectangle you can make using only red and green tiles is {area}.")

def test(filename):
    test = ["#", "X", "#", ".", ".", ".", "X"]
    crossed = 0
    for j in range(len(test)):
        if (test[j] == RED_TILE or test[j] == GREEN_TILE):
            if j-1 > 0 and (test[j-1] != RED_TILE and test[j-1] != GREEN_TILE):
                crossed += 1
            else:
                crossed += 1
        elif crossed%2 and test[j] == EMPTY:
            test[j] = GREEN_TILE
        print(crossed)
    print(test)

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # test(argv[1])
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: python3 day09.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)