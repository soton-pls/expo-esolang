## Towers of Hanoi

Towers of Hanoi is a mathematical game / puzzle where the goal is to move a
stack of discs from one pole to another, with the caveat that a disc can only
be placed on discs of a larger size than itself!

## Challenge

We have created a "toy-language" that allows you to solve the Towers of Hanoi.
However, this language is an esoteric programming language, meaning that its
syntax isn't the most conventional or easiest to use. Our language is inspired
by "Brainfuck", in that it has a very small instruction set where the user
controls a pointer that can interact with the Towers of Hanoi! We have also
added an extra "bag" you can put blocks you are holding into.

## Language Syntax

`>` : Move the cursor right

`<` : Move the cursor left

`.` : Interact (Pickup / Drop block)

`[` : While holding block (If not holding block, jump to corresponding `]`)

`]` : End While (If holding block, jump back to corresponding `[`)

`~` : Swap Held and Bag blocks

Any characters written in the solution that aren't one of these 6 will be
ignored. An invalid input (attempting to place a disc on an invalid stack or
pick up when there is nothing to pick up) will simply not compute but the
solution will continue running.
