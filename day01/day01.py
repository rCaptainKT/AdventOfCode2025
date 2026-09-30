import sys
import os

def partone(filename):
    combolock = 50
    password = 0
    with open(filename) as file:
        while True:
            line = file.readline()
            if not line:
                break

            direction = line[0]
            distance = int(line[1:])
            if direction == "R":
                combolock += distance
            elif direction == "L":
                combolock -= distance

            while combolock < 0:             
                combolock = 100+combolock
            while combolock > 99:
                combolock = combolock-100
                
            if combolock == 0:
                password += 1

    print(f"Password is {password}.")

def parttwo(filename):
    combolock = 50
    password = 0
    with open(filename) as file:
        while True:
            line = file.readline()
            if not line:
                break

            direction = line[0]
            distance = int(line[1:])

            if distance > 99:
                password += int(distance/100)
                distance = distance%100

            startCheck = False
            if combolock != 0:
                startCheck = True

            if direction == "R":
                combolock += distance
            elif direction == "L":
                combolock -= distance

            endCheck = False
            if combolock < 0:             
                combolock = 100+combolock
                if combolock != 0:
                    endCheck = True
            if combolock > 99:
                combolock = combolock-100
                if combolock != 0:
                    endCheck = True

            if startCheck and endCheck:
                password += 1
                
            if combolock == 0:
                password += 1

    print(f"Password is {password}.")

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print("Usage: ./day01.py [input]")
        sys.exit()
    
    main(argc, sys.argv)