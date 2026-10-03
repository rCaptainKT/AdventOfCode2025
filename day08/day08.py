import sys
import os
import math

def getboxes(filename):
    boxes = dict()
    with open(filename) as file:
        i = 0
        while True:
            line = file.readline().strip()
            if not line:
                break

            line = line.split(",")
            boxes[i] = (int(line[0]), int(line[1]), int(line[2]))
            i +=1

    return boxes

def getdistance(coords1, coords2):
    return math.sqrt(pow(coords1[0]-coords2[0], 2)+pow(coords1[1]-coords2[1], 2)+pow(coords1[2]-coords2[2], 2))

def calculatedistances(boxes):
    distances = list()
    for i in range(len(boxes.keys())):
        for j in range(i+1, len(boxes.keys())):
            distances.append((f"{i}-{j}", getdistance(boxes[i], boxes[j])))
    
    distances.sort(key=lambda x: x[1])
    return distances

def printcircuits(circuits):
    for circuit in circuits:
        line = f"[{len(circuit)}] "
        for box in circuit:
            line += f"{box} "
        print(line)

def getdistanceboxids(key):
    key = key.split("-")
    return (int(key[0]), int(key[1]))

def makecircuit(id1, id2, circuits):
    circuit1 = None
    circuit2 = None
    for circuit in circuits:
        for id in circuit:
            if id == id1:
                circuit1 = circuit
            if id == id2:
                circuit2 = circuit

            if circuit1 and circuit2:
                break

        if circuit1 and circuit2:
            break

    if circuit1 != circuit2:
        circuits.remove(circuit2)
        circuit1 += circuit2
    else:
        return

def makecircuits(boxes, distances, count=None):
    if count is None:
        count = len(distances)

    circuits = [[key] for key in boxes.keys()]
    for i in range(count):
        ids = getdistanceboxids(distances[i][0])
        makecircuit(ids[0], ids[1], circuits)

    circuits.sort(key= lambda x: len(x))
    return circuits

def partone(filename, pairs_to_connect):
    boxes = getboxes(filename)
    distances = calculatedistances(boxes)
    circuits = makecircuits(boxes, distances, pairs_to_connect)
    # printcircuits(circuits)

    circuitlengths = [len(circuit) for circuit in circuits]
    answer = circuitlengths[-1]*circuitlengths[-2]*circuitlengths[-3]
    print(f"The value obtained from multiplying the sizes of the three largest circuits is {answer}.")

def findfinalcircuitconnection(boxes, distances):
    circuits = [[key] for key in boxes.keys()]
    for i in range(len(distances)):
        ids = getdistanceboxids(distances[i][0])
        makecircuit(ids[0], ids[1], circuits)

        if len(circuits) == 1:
            return (ids[0], ids[1])

    return None

def parttwo(filename):
    boxes = getboxes(filename)
    distances = calculatedistances(boxes)
    finalcircuitconnection = findfinalcircuitconnection(boxes, distances)
    answer = None
    if finalcircuitconnection:
        answer = boxes[finalcircuitconnection[0]][0]*boxes[finalcircuitconnection[1]][0]
    print(f"The value obtained from multiplying the sizes of the three largest circuits is {answer}.")

def test():
    pass

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    partone(argv[1], int(argv[2]))
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 3:
        print(f"Usage: python3 day08.py [input] [pairs_to_connect]")
        sys.exit()

    # test()
    main(argc, sys.argv)