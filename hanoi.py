#! /usr/bin/env python3

import time, sys, signal, argparse, os, atexit, platform, math, json
from typing import TypeAlias, Optional


def exit_error(error: str):
    print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)


class HanoiInterpreter:
    Arrangement: TypeAlias = list[list[int]]
    Pointer: TypeAlias = tuple[int, int]

    cols = (47, 41, 43, 42, 46, 44, 45)

    def __init__(
        self,
        text_program: str,
        initial_state: Arrangement,
        goals: list[Arrangement],
        sleep_time: Optional[float] = None,
    ):
        self.parse(text_program)
        self.state = initial_state
        self.goals = goals
        self.sleep_time = sleep_time
        self.pc = 0
        self.tower_idx = 0
        self.held_value: Optional[int] = None
        self.scratch_value: Optional[int] = None
        self.max_height = sum(sum(1 for _ in t) for t in self.state) + 1
        self.cycles = 0

        self.prepare_ansi()
        self.run()

    def parse(self, text_program: str):
        self.program = list(
            filter(lambda x: x in ["<", ">", ".", "[", "]", "~"], text_program)
        )

        # All loops have statically defined branch addresses, so we can just
        # pre-cache them
        loop_stack: list[int] = []
        self.back_jumps: dict[int, int] = {}
        self.forward_jumps: dict[int, int] = {}

        for pc, char in enumerate(self.program):
            if char == "[":
                loop_stack.append(pc)
            elif char == "]":
                if not loop_stack:
                    exit_error(f"unexpected ] at token {pc}")

                start_pc = loop_stack.pop()
                self.back_jumps[pc] = start_pc + 1
                self.forward_jumps[start_pc] = pc + 1

        if loop_stack:
            exit_error("mismatched brackets. expected [ at EOF")

    def run(self):
        self.render()
        while self.pc < len(self.program):
            if self.state in self.goals:
                print("\u001b[35;1m", end="")
                print(
"""
██╗██╗██╗    ██╗    ██╗██╗███╗   ██╗███╗   ██╗███████╗██████╗     ██╗██╗██╗
██║██║██║    ██║    ██║██║████╗  ██║████╗  ██║██╔════╝██╔══██╗    ██║██║██║
██║██║██║    ██║ █╗ ██║██║██╔██╗ ██║██╔██╗ ██║█████╗  ██████╔╝    ██║██║██║
╚═╝╚═╝╚═╝    ██║███╗██║██║██║╚██╗██║██║╚██╗██║██╔══╝  ██╔══██╗    ╚═╝╚═╝╚═╝
██╗██╗██╗    ╚███╔███╔╝██║██║ ╚████║██║ ╚████║███████╗██║  ██║    ██╗██╗██╗
╚═╝╚═╝╚═╝     ╚══╝╚══╝ ╚═╝╚═╝  ╚═══╝╚═╝  ╚═══╝╚══════╝╚═╝  ╚═╝    ╚═╝╚═╝╚═╝
""", end="")
                print("\u001b[34;1m")
                print(f"Program length: {len(self.program)} characters")
                print(f"Execution time: {self.cycles} instructions")
                print("\u001b[0m")
                return

            if self.sleep_time is not None:
                time.sleep(self.sleep_time)
            else:
                input()
            self.step()
            self.render()

    def render(self):
        # 2 space gap between each tower, size diff between two sequential elements is 2 and initial length of element is 3,
        # so spacing is simply (max_height * 2) + 3
        spacing = (self.max_height * 2) + 5

        def render_block(block: int) -> str:
            size = 1 + block * 2
            return f"\u001b[{self.cols[block % len(self.cols)]};1m{' ' * size}\u001b[0m"

        def part(block: int) -> str:
            size = 1 + block * 2
            pad_needed = spacing - size

            return "{}{}{}".format(
                " " * math.ceil(pad_needed / 2),
                render_block(block),
                " " * math.floor(pad_needed / 2),
            )

        lines = ""

        # show the pointer
        line = "  "
        for x in range(len(self.state)):
            if self.tower_idx == x:
                if self.held_value is not None:
                    # show the element
                    part_str = part(self.held_value)
                else:
                    part_str = "[v]".center(spacing)
            else:
                # show nothing
                part_str = "".center(spacing)

            line += part_str

        lines += line + "\n\n"

        # go from highest highest to lowest, if there is an element render it else render the empty "post" of the tower
        for y in range(self.max_height):
            line = ""
            for x in range(len(self.state)):
                # because the list is in the wrong order, we need to "pad" it
                # in a max_height of 4 and a list of [1,2,3],
                # we want the first line to essentially check the "-1"th element (and come up empty)
                # we can do this by getting the length difference between the list and max_length
                # and modifying the y value by that
                offset = len(self.state[x]) - self.max_height
                yt = y + offset

                if yt < len(self.state[x]) and yt >= 0:
                    # show the element
                    part_str = part(self.state[x][yt])
                else:
                    # show the bare tower
                    part_str = "|".center(spacing)

                line += part_str

            lines += "  " + line + "\n"

        lines += f"    \u001b[{self.cols[0]};1m{' ' * (spacing - 4)}\u001b[0m" * len(
            self.state
        )

        lines += "\n\nbag: "
        if self.scratch_value is not None:
            lines += render_block(self.scratch_value)
        lines += " " * spacing
        lines += "\n\n"

        program_width = 60
        program_chunks = [
            (self.program + [" "])[i : i + program_width]
            for i in range(0, len(self.program), program_width)
        ]
        chunk = self.pc // program_width
        token_idx = self.pc % program_width
        program_chunks[chunk][
            token_idx
        ] = f"\u001b[{self.cols[4]};30;1m{program_chunks[chunk][token_idx]}\u001b[0m"

        for chunk in program_chunks:
            lines += "".join(chunk) + "\n"

        print("\u001b[H\n" + lines)

    @staticmethod
    def prepare_ansi():
        if platform.system() == "Windows":
            os.system("cls")

            # absolutely ancient bug from the win7 days to enable ANSI in a terminal
            # apparently this yanks you into the new shell mode if you're running
            # from old cmd and therefore ansi works
            os.system("")
        else:
            # linux
            os.system("clear")

        # don't show cursor
        print("\033[?25l", end="")
        # show cursor again once program is over
        atexit.register(lambda: print("\033[?25h", end=""))

    def step(self):
        self.cycles += 1
        next_pc = self.pc + 1
        match self.program[self.pc]:
            case ">":
                self.tower_idx += 1
            case "<":
                self.tower_idx -= 1
            case ".":
                if self.held_value is None:
                    if self.state[self.tower_idx]:
                        self.held_value = self.state[self.tower_idx].pop(0)
                elif (
                    not self.state[self.tower_idx]
                    or self.state[self.tower_idx][0] > self.held_value
                ):
                    self.state[self.tower_idx].insert(0, self.held_value)
                    self.held_value = None
            # As in brainfuck
            case "[":
                if self.held_value is None:
                    next_pc = self.forward_jumps[self.pc]
            case "]":
                if self.held_value is not None:
                    next_pc = self.back_jumps[self.pc]
            # Swap held with scratch reg
            case "~":
                tmp = self.scratch_value
                self.scratch_value = self.held_value
                self.held_value = tmp

        self.tower_idx %= len(self.state)
        self.pc = next_pc


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i", "--input", default="solution", type=str, help="path to input program"
    )
    parser.add_argument(
        "-t",
        "--time",
        type=float,
        help="time to spend on each instruction. if not specified, requires user to press enter to advance",
    )
    parser.add_argument("config", type=str, help="path to json config file")

    args = parser.parse_args()

    # Exit nicely on ctrl-c
    signal.signal(signal.SIGINT, lambda signum, frame: sys.exit())

    try:
        with open(args.config, "r") as f:
            config = json.load(f)

        if "init" not in config or "goals" not in config:
            exit_error(f"{args.config} is not a valid config, missing \"init\" or \"goals\"")

    except OSError:
        exit_error(f'could not open config "{args.config}"')

    try:
        with open(args.input, "r") as f:
            HanoiInterpreter(f.read(), config["init"], config["goals"], args.time)
    except OSError:
        exit_error(f'could not open input "{args.input}"')
