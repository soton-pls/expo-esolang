#! /usr/bin/env python3

import time, sys
from typing import TypeAlias, Optional
import argparse

from render import *


def exit_error(error: str):
    print(f"ERROR: {error}", file=sys.stderr)
    sys.exit(1)


class HanoiInterpreter:
    Arrangement: TypeAlias = list[list[int]]
    Pointer: TypeAlias = tuple[int, int]

    def __init__(
        self,
        text_program: str,
        initial_state: Arrangement,
        sleep_time: Optional[float] = None,
    ):
        self.parse(text_program)
        self.state = initial_state
        self.sleep_time = sleep_time
        self.pc = 0
        self.tower_idx = 0
        self.held_value: Optional[int] = None

        prepare_ansi()
        self.run()

    def parse(self, text_program: str):
        self.program = list(
            filter(lambda x: x in ["<", ">", ".", "[", "]"], text_program)
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
                self.back_jumps[pc] = start_pc
                self.forward_jumps[start_pc] = pc + 1

        if loop_stack:
            exit_error("mismatched brackets. expected [ at EOF")

    def run(self):
        self.render()
        while self.pc < len(self.program):
            if self.sleep_time is not None:
                time.sleep(self.sleep_time)
            else:
                input()
            self.step()
            self.render()

    def render(self):
        render_hanoi(self.state, (self.tower_idx, self.held_value))
        print("".join(self.program))
        pre_space = " " * self.pc
        post_space = " " * (len(self.program) - self.pc - 1)
        print(pre_space, "^", post_space, sep="")

    def step(self):
        next_pc = self.pc + 1
        match self.program[self.pc]:
            case ">":
                self.tower_idx = min(self.tower_idx + 1, len(self.state) - 1)
            case "<":
                self.tower_idx = max(self.tower_idx - 1, 0)
            case ".":
                if self.held_value is None:
                    self.held_value = self.state[self.tower_idx].pop(0)
                elif (
                    not self.state[self.tower_idx]
                    or self.state[self.tower_idx][0] > self.held_value
                ):
                    self.state[self.tower_idx].insert(0, self.held_value)
                    self.held_value = None
            case "[":
                if self.held_value is None:
                    next_pc = self.forward_jumps[self.pc]
            case "]":
                next_pc = self.back_jumps[self.pc]
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

    args = parser.parse_args()

    try:
        with open(args.input, "r") as f:
            HanoiInterpreter(f.read(), [[1, 2, 3], [], []], args.time)
    except OSError:
        exit_error(f'could not open input "{args.input}"')
