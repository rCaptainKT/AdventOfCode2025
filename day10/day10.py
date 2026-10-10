import sys
import os

OFF = "."
ON = "#"

def parseinput(filename):
    finalindicators = list()
    buttonsets = list()
    joltages = list()
    with open(filename) as file:
        while True:
            line = file.readline().strip().split()
            if not line:
                break
            finalindicators.append(line[0][1:-1])
            temp = list()
            for i in range(1, len(line)-1):
                temp.append(tuple(int(x) for x in line[i][1:-1].split(",")))
            buttonsets.append(temp)
            joltages.append([int(x) for x in line[-1][1:-1].split(",")])
            
    return finalindicators, buttonsets, joltages

def toggleindicatorlight(indicator, light):
    indicator = list(indicator)
    if indicator[light] == OFF:
        indicator[light] = ON
    elif indicator[light] == ON:
        indicator[light] = OFF
    
    return "".join(indicator)

def _findsolution(indicator, finalindicator, takenactions, buttonset, cache, depth):
    if depth == 0:
        return indicator, takenactions

    for button in buttonset:
        if button in takenactions:
            continue
        temp = indicator
        for i in button:
            temp = toggleindicatorlight(temp, i)
        takenactions.append(button)
        
        cachekey = tuple(sorted(takenactions))
        if cache.get(cachekey, False):
            takenactions.pop()
            continue
        else:
            cache[cachekey] = True

        newindicator, _ = _findsolution(temp, finalindicator, takenactions, buttonset, cache, depth-1)
        if newindicator == finalindicator:
            return newindicator, takenactions
        else:
            takenactions.pop()
    
    return indicator, takenactions
            
def findshortestbuttonsolution(finalindicator, buttonset):
    indicator = "."*len(finalindicator)
    cache = dict()
    for i in range(len(buttonset)):
        cache.clear()
        result, takenactions = _findsolution(indicator, finalindicator, [], buttonset, cache, i)
        if result == finalindicator:
            break

    return result, takenactions

def partone(filename):
    finalindicators, buttonsets, _ = parseinput(filename)
    actions = 0
    for finalindicator, buttonset in zip(finalindicators, buttonsets):
        _, takenactions = findshortestbuttonsolution(finalindicator, buttonset)
        actions += len(takenactions)

    print(f"The fewest button presses required to correctly configure the indicator lights on all of the machines is {actions}.")

def parttwo(filename):
    pass

def test():
    pass

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # test()
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: python3 day10.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)