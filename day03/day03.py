import sys
import os

def partone(filename):
    totaljoltage = 0

    with open(filename) as file:
        while True:    
            line = file.readline().strip()
            if not line:
                break

            bank = list(line)
            maxbatindex1 = 0
            for i in range(len(bank)-1):
                if bank[i] > bank[maxbatindex1]:
                    maxbatindex1 = i

            maxbatindex2 = maxbatindex1 + 1
            for i in range(maxbatindex1+1, len(bank)):
                if bank[i] > bank[maxbatindex2]:
                    maxbatindex2 = i
                    
            totaljoltage += int(bank[maxbatindex1]+bank[maxbatindex2])

    print(f"Total joltage output is {totaljoltage}.")

def parttwo(filename):
    pass

def test():
    bank = ['9', '8', '7', '6', '5', '4', '3', '2', '1', '1', '1', '1', '1', '1', '1']
    maxbatindex1 = 0
    maxbatindex2 = 1
    for i in range(len(bank)-1):
        if bank[i] > bank[maxbatindex1]:
            maxbatindex1 = i

    for i in range(maxbatindex1+1, len(bank)):
        print(i)
        if bank[i] > bank[maxbatindex2]:
            maxbatindex2 = i

    print(bank)
    print(list(range(maxbatindex1+1, len(bank))))
    print(f"{maxbatindex1} {maxbatindex2}")
    print(bank[maxbatindex1] + bank[maxbatindex2])

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: ./day03.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)