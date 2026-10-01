import sys
import os

def getstartandendranges(filename):
    starts = list()
    ends = list()
    with open(filename) as file:
        while True:
            line = file.readline().strip()
            if not line:
                break

            start = int(line.split("-")[0])
            starts.append(start)
            end = int(line.split("-")[1])
            ends.append(end)

    return (starts, ends)

def countfresh(filename, starts, ends):
    fresh = 0
    with open(filename) as file:
        for _ in range(len(starts)+1):
            file.readline()

        while True:
            line = file.readline().strip()
            if not line:
                break

            ingredientid = int(line)
            for s, e in zip(starts, ends):
                if s <= ingredientid and e >= ingredientid:
                    fresh += 1
                    break

    return fresh

def partone(filename):
    startsandends = getstartandendranges(filename)
    starts = startsandends[0]
    ends = startsandends[1]

    fresh = countfresh(filename, starts, ends)
    print(f"Number of available ingredient ids that are fresh is {fresh}.")

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
        print(f"Usage: python3 day05.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)