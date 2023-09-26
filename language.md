# Language

## Goal

A Toy Language designed in a similar manor to brainfuck, where the goal is for the user to solve the towers of hanoi problem.

Basic Features:
- **Three Towers** of `n` **Blocks**
- A **Pointer** to move blocks
- An instruction set to control the pointer
- A scratch register
- **Visual** of **Final Tower Arrangement**

Expansive Features:
- **Multiple Towers**
- **Interactive REPL**
- **Animated** Visuals

## Backend Features

There will be a pointer that can be moved left and right, but will stop moving if all the way left and all the way right.
The pointer can pick up and drop blocks, with one `interact` keyword. This creates challenge by having a simplistic rule set.
Rudimentary loops, based on the pointers current state, will allow for the solution to be solved in complex and creative ways, whilst expanding whats possible in the language.
Invalid moves will be ignored, or will cause the script to `break`.

## Syntax Features

`>` : Move the cursor right

`<` : Move the cursor left

`.` : Interact (Pickup / Drop)

`[` : While holding block

`]` : End While

`~` : Swap Held and Scratch value
