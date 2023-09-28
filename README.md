# Expo Esolang
A Esoteric Toy Language designed in a similar mannor to BrainFuck, where the sytax in made of a small selection of single-character long keywords.
This language allows for users to write algorithms to solve the Towers of Hanoi problem, and provides animated feedback to the user.
## How To Run
1. Clone the GitHub Repo
2. Write code into the `solution` file
3. Run `python hanoi.py "problems/hanoi_3.json" --time 0.3`
4. Enjoy!
## Parameters
### Problems
You can replace `problems/hanoi_3.json` with another Json file found in `problems/` to attempt different problems (i.e. amount of blocks). We have provided Json files for 3 blocks, 6 blocks and 7 blocks.
### Time
You can replace the number after `--time` with a number of seconds to wait between showing each step of the animation (i.e. a lower number will speed up the animation process). You can also optionally remove this parameter and step through your solution by pressing the enter key (make sure you're focused on the terminal window to do so)
## Solutions
The `solutions/` folder contains a selection of solutions using different subsets of the characters, including our winning 9 character general solution!
## Analysing Programs
See `model/README.md` for a model that allowed us to prove that there are no programs smaller than 9 characters that solve N=3 Towers of Hanoi using our language.

Also checkout [hanoi-rs](https://github.com/LordIdra/hanoi-rs/tree/master) from a society member that enumerates all programs of a given length that solve N=3 Towers of Hanoi.
## Credits
Credits to Dillon Geary and George Rennie for designing the language and writing the interpreter. Credits also to Chris Taperell (https://plaao.net) for creating the ANSI animation.
