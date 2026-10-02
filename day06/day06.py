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
        print(f"Usage: python3 day06.py [input]")
        sys.exit()

    # test()
    main(argc, sys.argv)