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

def _findlargest(bank, start, digitsleft):
    if digitsleft == 0:
        return ""

    maxbatindex = start
    for i in range(start, len(bank)-digitsleft+1):
        if bank[i] > bank[maxbatindex]:
            maxbatindex = i

    return bank[maxbatindex] + _findlargest(bank, maxbatindex+1, digitsleft-1)

def findlargest(bank, digitsleft):
    return _findlargest(bank, 0, digitsleft)

def parttwo(filename):
    totaljoltage = 0

    with open(filename) as file:
        while True:    
            line = file.readline().strip()
            if not line:
                break

            bank = list(line)
            totaljoltage += int(findlargest(bank, 12))
    
    print(f"Total joltage output is {totaljoltage}.")

def test():
    bankstr = "811111111111119"
    bank = list(bankstr)
    print(findlargest(bank, 2))

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