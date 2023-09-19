from time import sleep
from render import *


def lexer(code):
    out = filter(lambda x: x in ["<", ">", ".", "[", "]"], code)
    return list(out)


def solver(arrangement, location, holding, code):

    render_hanoi(arrangement, (location, holding))

    sleep(0.3)

    if not code:
        return arrangement,[location,holding]
    instruction = code.pop(0)
    match instruction:
        case ">":
            location = min(location + 1, 2)
        case "<":
            location = max(location - 1, 0)
        case ".":
            if holding == -1:
                holding = arrangement[location].pop(0)
            elif next(iter(arrangement[location]),100) > holding:
                arrangement[location].insert(0, holding)
                holding = -1

    return solver(arrangement, location, holding, code)


def hanoiPrint(arrangement,pointer):
    output = "\n\n"

    if pointer:
        location = pointer[0]
        number = pointer[1]

        if number == -1: number = "v"

        output = output + " " + "".join(["  " for i in range(location)]) + str(number) + "\n"

    list0 = arrangement[0]
    list1 = arrangement[1]
    list2 = arrangement[2]

    amount = max(list0 + list1 + list2)
    list0 = ["|" for i in range(amount - len(list0))] + list0
    list1 = ["|" for i in range(amount - len(list1))] + list1
    list2 = ["|" for i in range(amount - len(list2))] + list2


    for i in range(amount):
        output = output + " " + str(list0.pop(0)) + " " + str(list1.pop(0)) + " " + str(list2.pop(0)) + "\n"
    output = output + "-=====-"
    print(output)

if __name__ == "__main__":
    #scriptFile = input("Script: ")
    filecontents = open("solution","r").read()
    script = lexer(filecontents)
    prepare_ansi()
    solution = solver(([1, 2, 3], [], []), 0, -1,script)