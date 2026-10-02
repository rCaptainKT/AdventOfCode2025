import sys
import os

def getoperators(filename):
    operators = list()
    with open(filename) as file:
        while True:
            char = file.read(1)
            if char == "\n" or char == " ":
                continue
            elif char == "+" or char == "*":
                operators.append(char)
            elif char:
                continue
            else:
                break

    return operators

def dooperation(num1, num2, operator):
    match(operator):
        case "+":
            return num1 + num2
        case "*":
            return num1 * num2
        case _:
            raise ValueError(f"Unknown operator: {operator}")

def getanswers(filename, operators):
    answers = list()
    with open(filename) as file:
        i = 0
        num = ""
        while True:
            char = file.read(1)
            if char == " ":
                if num != "":
                    if len(answers) != len(operators):
                        answers.append(int(num))
                    else:
                        answers[i] = dooperation(answers[i], int(num), operators[i])
                    num = ""
                    i += 1
            elif char == "\n":
                if num != "":
                    if len(answers) != len(operators):
                        answers.append(int(num))
                    else:
                        answers[i] = dooperation(answers[i], int(num), operators[i])
                    num = ""
                i = 0
            elif char == "+" or char == "*":
                break
            else:
                num += char
    
    return answers

def partone(filename):
    operators = getoperators(filename)
    answers = getanswers(filename, operators)
    print(f"The grand total is {sum(answers)}.")

def getrowlength(filename):
    length = 0
    with open(filename) as file:
        while True:
            char = file.read(1)
            length += 1
            if char == "\n":
                break

    return length

def getrowcount(filename):
    rowcount = 0

    with open(filename) as file:
        while True:
            char = file.read(1)
            if char == "\n":
                rowcount += 1
            elif char == "+" or char == "*":
                rowcount += 1
                break
    
    return rowcount

def getchar(filename, rowlength, row, col):
    char = ""

    with open(filename) as file:
        for _ in range(rowlength*row+col):
            file.read(1)
        char = file.read(1)

    return char

def liststrtoint(l):
    for i in range(len(l)):
        l[i] = int(l[i])

def listoperation(nums, operator):
    answer = 0
    match operator:
        case "+":
            for num in nums:
                answer += num
        case "*":
            answer += 1
            for num in nums:
                answer *= num
        case _:
            raise ValueError(f"Unknown operator: {operator}")

    return answer

def parttwo(filename):
    rowlength = getrowlength(filename)
    rowcount = getrowcount(filename)

    i = rowlength-2
    nums = list()
    operator = ""
    total = 0
    while i > -1:
        nums.append("")
        for j in range(rowcount):
            if j == rowcount-1:
                operator = getchar(filename, rowlength, j, i)
            else:
                nums[-1] = nums[-1] + getchar(filename, rowlength, j, i)
        i -= 1
        
        if operator == "+" or operator == "*":
            liststrtoint(nums)
            total += listoperation(nums, operator)
            nums.clear()
            i -= 1

    print(f"The grand total is {total}.")

def test():
    pass

def main(argc, argv):
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    partone(argv[1])
    parttwo(argv[1])

if __name__ == "__main__":
    argc = len(sys.argv)
    if argc < 2:
        print(f"Usage: python3 day06.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)