import sys
import os
from fractions import Fraction
import math

OFF = "."
ON = "#"

FREE = "free"
BOUND = "bound"

def parseinput(filename):
    finalindicators = list()
    buttonsets = list()
    finaljoltagesets = list()
    with open(filename) as file:
        while True:
            line = file.readline().strip().split()
            if not line:
                break
            finalindicators.append(line[0][1:-1])
            temp = list()
            for i in range(1, len(line)-1):
                temp.append(tuple(int(x) for x in line[i][1:-1].split(",")))
            temp.sort(key=lambda x: len(x), reverse=True)
            buttonsets.append(temp)
            finaljoltagesets.append(tuple(int(x) for x in line[-1][1:-1].split(",")))
            
    return finalindicators, buttonsets, finaljoltagesets

def toggleindicatorlight(indicator, light):
    indicator = list(indicator)
    if indicator[light] == OFF:
        indicator[light] = ON
    elif indicator[light] == ON:
        indicator[light] = OFF
    
    return "".join(indicator)

def _findindicatorsolution(indicator, finalindicator, takenactions, buttonset, cache, depth):
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

        newindicator, _ = _findindicatorsolution(temp, finalindicator, takenactions, buttonset, cache, depth-1)
        if newindicator == finalindicator:
            return newindicator, takenactions
        else:
            takenactions.pop()
    
    return indicator, takenactions
            
def findshortestindicatorsolution(finalindicator, buttonset):
    indicator = "."*len(finalindicator)
    cache = dict()
    for i in range(len(buttonset)):
        cache.clear()
        result, takenactions = _findindicatorsolution(indicator, finalindicator, [], buttonset, cache, i)
        if result == finalindicator:
            break
    
    return takenactions

def partone(filename):
    finalindicators, buttonsets, _ = parseinput(filename)
    actions = 0
    for finalindicator, buttonset in zip(finalindicators, buttonsets):
        takenactions = findshortestindicatorsolution(finalindicator, buttonset)
        actions += len(takenactions)

    print(f"The fewest button presses required to correctly configure the indicator lights on all of the machines is {actions}.")

def _findjoltagesetsolution(joltageset, finaljoltageset, takenactions, buttonset, cache, depth):
    if depth == 0:
        return tuple(joltageset), takenactions

    for currentjoltage, finaljoltage in zip(joltageset, finaljoltageset):
        if currentjoltage > finaljoltage:
            return tuple(joltageset), takenactions
                
    for button in buttonset:
        for i in button:
            joltageset[i] += 1
        takenactions.append(button)

        # cachekey = tuple(sorted(takenactions))
        # if cache.get(cachekey, False):
        #     takenactions.pop()
        #     continue
        # else:
        #     cache[cachekey] = True

        result, _ = _findjoltagesetsolution(joltageset, finaljoltageset, takenactions, buttonset, cache, depth-1)
        if result == finaljoltageset:
            return result, takenactions
        else:
            takenactions.pop()
            for i in button:
                joltageset[i] -= 1
    
    return result, takenactions

def findshortestjoltagesolution(finaljoltageset, buttonset):
    joltageset = [0]*len(finaljoltageset)
    cache = dict()
    i = 0
    while True:
        cache.clear()
        result, takenactions = _findjoltagesetsolution(joltageset, finaljoltageset, [], buttonset, cache, i)
        if result == finaljoltageset:
            break
        elif i == 100:
            print("MAX LIMIT REACHED")
            print(finaljoltageset)
            break
        else:
            i += 1

    return takenactions

def printgrid(grid):
    for row in grid:
        line = ""
        for value in row:
            line += f"{str(value):>5} "
        print(line)

def swaprows(matrix, row1, row2):
    if row1 == row2:
        return
    
    temp = matrix[row1]
    matrix[row1] = matrix[row2]
    matrix[row2] = temp

def multiplyrow(matrix, row, multipler):
    for i in range(len(matrix[row])):
        matrix[row][i] *= multipler

def addrows(matrix, targetrow, addendrow, multiplier=1):
    if multiplier != 1:
        temp = [0]*len(matrix[addendrow])
        for i in range(len(matrix[addendrow])):
            temp[i] = matrix[addendrow][i] * multiplier
    else:
        temp = matrix[addendrow]

    for i in range(len(matrix[targetrow])):
        matrix[targetrow][i] += temp[i]

def rref(matrix):
    """
    May and may not be good enough for general use. Definitely good enough for this though.
    https://www.math.purdue.edu/~shao92/documents/Algorithm%20REF.pdf
    """
    pivotcol = 0
    pivotrow = 0
    while pivotcol < len(matrix[0]) and pivotrow < len(matrix):
        # print(pivotrow, pivotcol)
        # printgrid(matrix)
        # print("")
        # Find pivot row
        maxrowindex = pivotrow
        maxrowvalue = abs(matrix[pivotrow][pivotcol])
        # print(maxrowindex, maxrowvalue)
        for row in range(pivotrow, len(matrix)):
            if abs(matrix[row][pivotcol]) > maxrowvalue:
                maxrowindex = row
                maxrowvalue = abs(matrix[row][pivotcol])
        if maxrowvalue != 0: 
            swaprows(matrix, pivotrow, maxrowindex)

        # print(maxrowindex, maxrowvalue)
        if maxrowvalue != 0:
            # Reduce pivot to one
            multiplier = 1/matrix[pivotrow][pivotcol]
            multiplyrow(matrix, pivotrow, multiplier)

            # Reduce all values above and below pivot to zero
            for row in range(0, len(matrix)):
                if row == pivotrow:
                    continue
                multiplier = -matrix[row][pivotcol]/matrix[pivotrow][pivotcol]
                addrows(matrix, row, pivotrow, multiplier)

            pivotcol += 1
            pivotrow += 1
        else:
            pivotcol += 1

def getvariabledata(matrix):
    variabledata = dict()
    for i in range(len(matrix[0])-1):
        variabledata[i] = FREE

    for i in range(len(matrix)):
        for j in range(len(matrix[i])-1):
            if matrix[i][j] == 1:
                variabledata[j] = BOUND
                break

    return variabledata

def getfreevarmaxpresses(variabledata, finaljoltageset, buttonset):
    freevarmaxpresses = dict()
    for i, v in variabledata.items():
        if v != BOUND:
            minvalue = finaljoltageset[buttonset[i][0]]   
            for index in buttonset[i]:
                if finaljoltageset[index] < minvalue:
                    minvalue = finaljoltageset[index]
            freevarmaxpresses[i] = minvalue
        
    return freevarmaxpresses

def _getallfreevarcombinations(freevarmaxpressvalues, allfreevarcombinations, currentvalues, currentvaluesindex):
    for i in range(freevarmaxpressvalues[currentvaluesindex]+1):
        currentvalues[currentvaluesindex] = i
        if currentvaluesindex == len(currentvalues)-1:
            allfreevarcombinations.append(tuple(currentvalues))
        else:
            _getallfreevarcombinations(freevarmaxpressvalues, allfreevarcombinations, currentvalues, currentvaluesindex+1)
    
def getallfreevarcombinations(freevarmaxpresses):
    allfreevarcombinations = list()
    if freevarmaxpresses != {}:
        _getallfreevarcombinations(list(freevarmaxpresses.values()), allfreevarcombinations, [0]*len(freevarmaxpresses.keys()), 0)
    else:
        allfreevarcombinations.append([])
    return allfreevarcombinations

def getsolution(matrix, freevarvalues, solutionlength, pivotrowcount):
    solution = [0]*solutionlength
    for key, value in freevarvalues.items():
        solution[key] = value

    for i in range(pivotrowcount):
        varindex = -1
        for j in range(len(matrix[i])):
            if j != len(matrix[i])-1:
                if varindex == -1 and matrix[i][j] == 1:
                    varindex = j
                elif varindex != -1 and matrix[i][j] != 0:
                    solution[varindex] -= matrix[i][j]*solution[j]
            else:
                if varindex != -1:
                    solution[varindex] += matrix[i][j]

    return solution

def validatesolution(solution):
    if sum(solution) != sum([abs(x) for x in solution]):
        # Solution is not all positive
        return False
    for value in solution:
        if not value.is_integer():
            # Non-integer value in solution
            return False

    return True

# def sumobjective(matrix):
#     return [1]*(len(matrix[0])-1) + [0]

# def setupsimplex(matrix, getobjective):
#     matrix.insert(0, getobjective(matrix))
#     for i in range(1, len(matrix)):
#         for j in range(0, len(matrix)):
#             if j==i:
#                 matrix[j].insert(-1, 1)
#             else:
#                 matrix[j].insert(-1, 0)

# def simplexminimize(matrix, getobjective):
#     setupsimplex(matrix, getobjective)
#     printgrid(matrix)

def findleastpressesjoltagesolution(finaljoltageset, buttonset, debug=False):
    matrix = list()
    for i in range(len(finaljoltageset)):
        matrix.append([0]*(len(buttonset)+1))
    for i, button in enumerate(buttonset):
        for j in button:
            matrix[j][i] = Fraction(1)
    for i in range(len(matrix)):
        matrix[i][-1] = finaljoltageset[i]

    rref(matrix)
    # simplexminimize(matrix, sumobjective)

    variabledata = getvariabledata(matrix)
    freevarmaxpresses = getfreevarmaxpresses(variabledata, finaljoltageset, buttonset)
    allfreevarcombinations = getallfreevarcombinations(freevarmaxpresses)
    allfreevarcombinations.sort(key=lambda x: sum(x))
    
    freevarvalues = dict()
    bestsolution = None
    bestsolutionsum = math.inf
    for freevarcombination in allfreevarcombinations: 
        for key, value in zip(freevarmaxpresses.keys(), freevarcombination):
            freevarvalues[key] = value
        # print(freevarvalues)
        solution = getsolution(matrix, freevarvalues, len(buttonset), len(finaljoltageset))
        if validatesolution(solution):
            if bestsolution is None or sum(solution) < bestsolutionsum:
                bestsolution = solution
                bestsolutionsum = sum(solution)

    # if debug:
    #     printgrid(matrix)
    #     print(buttonset)
    #     print(finaljoltageset)
    #     print(variabledata)
    #     print(freevarmaxpresses)
    #     # print(allfreevarcombinations)
    #     print(solution)
    #     print(sum(solution))
    
    return bestsolutionsum

def parttwo(filename):
    _, buttonsets, finaljoltagesets = parseinput(filename)
    totalactions = 0
    for finaljoltageset, buttonset in zip(finaljoltagesets, buttonsets):
        totalactions += findleastpressesjoltagesolution(finaljoltageset, buttonset)

        # actions = findleastpressesjoltagesolution(finaljoltageset, buttonset, True)
        # print(actions)
        # totalactions += actions
        
        # findleastpressesjoltagesolution(finaljoltagesets[12], buttonsets[12])
        # break

    if int(totalactions) == totalactions:
        totalactions = int(totalactions)

    print(f"The fewest button presses required to correctly configure the joltage level counters on all of the machines is {totalactions}.")

def test(filename):
    # [...##.] (0,3,4) (0,1,2,5) (0,1,3,4,5) (3,4) {53,34,17,42,42,34}
    finaljoltageset = (53,34,17,42,42,34)
    buttonset = [(0, 1, 3, 4, 5), (0, 1, 2, 5), (0, 3, 4), (3, 4)]

    findleastpressesjoltagesolution(finaljoltageset, buttonset)

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    # test(argv[1])
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: python3 day10.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)
