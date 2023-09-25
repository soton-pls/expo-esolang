#! /usr/bin/env python3

from time import sleep
from typing import TypeAlias

from render import *

Arrangement: TypeAlias = list[list[int]]
Pointer: TypeAlias = tuple[int,int]

def lexer(code):
    out = filter(lambda x: x in ["<", ">", ".", "[", "]"], code)
    open = filter(lambda x: x == "[", code)
    close = filter(lambda x: x == "]", code)
    if len(list(open)) == len(list(close)):
        return list(out)
    else:
        return ""


def skip(code: str, pointer: int, count: int = 0) -> int:
    if pointer > len(code) - 1:
        return pointer

    instruction = code[pointer]
    if instruction == "[":
        count += 1
    if instruction == "]":
        count -= 1

    if count == 0:
        return pointer
    else:
        return skip(code, pointer + 1, count)


def solver(arrangement: Arrangement, code: str, location: int = 0, holding: int = -1, pointer: int = 0,
           loop_locations: list[int] = []) -> (tuple[Arrangement, Pointer] | tuple[Arrangement, tuple[int]]):

    render_hanoi(arrangement, (location, holding))

    if pointer > len(code) - 1:
        return arrangement, (location, holding)

    instruction = code[pointer]
    print(instruction)

    sleep_time = 0.5
    match instruction:
        case ">":
            sleep(sleep_time)
            location = min(location + 1, 2)
        case "<":
            sleep(sleep_time)
            location = max(location - 1, 0)
        case ".":
            sleep(sleep_time)
            if holding == -1:
                holding = arrangement[location].pop(0)
            elif next(iter(arrangement[location]), 100) > holding:
                arrangement[location].insert(0, holding)
                holding = -1
        case "[":
            if holding == -1:
                pointer = skip(code, pointer)
            else:
                loop_locations.insert(0, pointer)
        case "]":
            pointer = loop_locations.pop(0) - 1

    print(pointer)

    return solver(arrangement, code, location, holding, pointer + 1, loop_locations)


def hanoiPrint(arrangement, pointer):
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
    # scriptFile = input("Script: ")
    with open("solution", "r") as f:
        file_contents = f.read()
    script = lexer(file_contents)
    if script == "":
        print("INVALID CODE")
    else:
        prepare_ansi()
        solution = solver([[1, 2, 3], [], []], script)
