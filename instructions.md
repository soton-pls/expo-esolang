## Towers of Hanoi

Towers of Hanoi is a mathematical game / puzzle where the goal is to move a
stack of discs from one pole to another, with the caveat that a disc can only
be placed on discs of a larger size than itself!

## Challenge

We have created a "toy-language" that allows you to solve the Towers of Hanoi.
However, this language is an esoteric programming language, meaning that its
syntax isn't the most conventional or easiest to use. Our language is inspired
by "Brainfuck", in that it has a very small instruction set where the user
controls a pointer that can interact with the Towers of Hanoi!

## Language Syntax

`>` : Move the cursor right

`<` : Move the cursor left

`.` : Interact (Pickup / Drop)

`[` : While holding block

`]` : End While

Any characters written in the solution that aren't one of these 5 will be
ignored. An invalid input (moving right when on the rightmost column, attempting
to place a disc on an invalid stack) will simply not compute but the solution
will continue running.
