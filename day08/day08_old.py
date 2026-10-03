import sys
import os
import math

def createbox(x, y, z):
    return (x, y, z)

def printcircuits(circuits):
    for circuit in circuits:
        line = f"[{len(circuit)}] "
        for box in circuit:
            line += f"{box} "
        print(line)

def getcircuits(filename):
    circuits = list()
    with open(filename) as file:
        while True:
            line = file.readline().strip()
            if not line:
                break

            line = line.split(",")
            circuits.append([createbox(int(line[0]), int(line[1]), int(line[2]))])

    return circuits

def getdistance(box1, box2):
    return math.sqrt(pow(box1[0]-box2[0], 2)+pow(box1[1]-box2[1], 2)+pow(box1[2]-box2[2], 2))

def connectcircuits(circuits):
    while True:
        circuits.sort(key=lambda x: len(x))
        if len(circuits[0]) > 1:
            break
        circuit = circuits.pop(0)
        box = circuit[0]

        closestcircuit = None
        closestdistance = math.inf
        for i in range(len(circuits)):
            for b in circuits[i]:
                dist = getdistance(box, b)
                if dist < closestdistance:
                    closestdistance = dist
                    closestcircuit = circuits[i]

        closestcircuit.append(box)

def partone(filename):
    circuits = getcircuits(filename)
    connectcircuits(circuits)
    printcircuits(circuits)

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
        print(f"Usage: python3 day08.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)