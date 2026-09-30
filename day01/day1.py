import sys
import os

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))

    combolock = 50
    password = 0
    with open(argv[1]) as file:
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

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print("Usage: ./day1.py [input]")
        sys.exit()
    
    main(argc, sys.argv)