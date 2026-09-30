import sys
import os

def getranges(filename):
    ranges = list()
    with open(filename) as file:
        separator = ","
        buffer = ""
        while True:
            char = file.read(1)
            if not char:
                # End of file
                if buffer:
                    # Append anything left in the buffer, strip any remaining whitespace at the end
                    ranges.append(buffer.strip())
                break

            if char == separator:
                # Append range to range list and clear buffer
                ranges.append(buffer)
                buffer = ""
            else:
                # Append char to buffer
                buffer += char

    return ranges

def partone(filename):
    ranges = getranges(filename)
    answer = 0

    for r in ranges:
        startvalue = int(r.split("-")[0])
        endvalue = int(r.split("-")[1])
        for i in range(startvalue, endvalue+1):
            num = str(i)
            numlength = len(num)
            if numlength%2:
                # num has odd number of digits
                continue

            midpoint = int(numlength/2)
            if num[:midpoint] == num[midpoint:]:
                answer += i

    print(f"Sum of invalid ids is {answer}.")

def parttwo(filename):
    ranges = getranges(filename)

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: ./day02.py [input]")
        sys.exit()

    main(argc, sys.argv)
