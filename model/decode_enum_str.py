#! /usr/bin/env python3
# Convert a decimal value corresponding to the `mem` value from a hanoi model
# trace into the corresponding program. The decimal value should be supplied
# as the first program argument

import sys

assert len(sys.argv) == 2

num = int(sys.argv[1])

program = ""
while num != 0:
    match num % 8:
        case 0: program += "<"
        case 1: program += ">"
        case 2: program += "."
        case 3: program += "["
        case 4: program += "]"
        case 5: program += "~"
        case 6: program += " "
    num //= 8

print("".join(reversed(program)))
