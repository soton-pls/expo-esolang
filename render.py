import platform
import os
import math
import atexit

from typing import Optional

cols = (
    37, 31, 33, 32, 36, 34, 35
)


def prepare_ansi():
    if platform.system() == "Windows":
        os.system("cls")

        # absolutely ancient bug from the win7 days to enable ANSI in a terminal
        # apparently this yanks you into the new shell mode if you're running from old cmd and therefore ansi works
        os.system("")
    else:
        # linux
        os.system("clear")

    # don't show cursor
    print("\033[?25l", end="")
    # show cursor again once program is over
    atexit.register(lambda: print("\033[?25h", end=""))


def render_hanoi(arrangement: list[list[int]], scratch: Optional[int], pointer: tuple[int, int], element_char="█", tower_char="|", floor_char="█"):
    # count the number of elements in the arrangement tuple, add 1 to get maximum height
    max_height = sum(sum(1 for _ in t) for t in arrangement) + 1

    # if there's something being picked up, make sure we add 1 to this
    if pointer[1] is not None:
        max_height += 1
    if scratch is not None:
        max_height += 1

    # 2 space gap between each tower, size diff between two sequential elements is 2 and initial length of element is 3,
    # so spacing is simply (max_height * 2) + 3
    spacing = (max_height * 2) + 5

    def render_block(block: int) -> str:
        size = (1 + block * 2)
        return f"\u001b[{cols[block % len(cols)]};1m{element_char * size}\u001b[0m"

    def part(block: int) -> str:
        size = (1 + block * 2)
        pad_needed = spacing - size

        return "{}{}{}".format(
            " " * math.ceil(pad_needed / 2),
            render_block(block),
            " " * math.floor(pad_needed / 2),
        )

    lines = ""

    # show the pointer
    line = "  "
    for x in range(len(arrangement)):
        if pointer[0] == x:
            if pointer[1] is not None:
                # show the element
                part_str = part(pointer[1])
            else:
                part_str = "[v]".center(spacing)
        else:
            # show nothing
            part_str = "".center(spacing)

        line += part_str

    lines += line + "\n\n"

    # go from highest highest to lowest, if there is an element render it else render the empty "post" of the tower
    for y in range(max_height):
        line = ""
        for x in range(len(arrangement)):
            # because the list is in the wrong order, we need to "pad" it
            # in a max_height of 4 and a list of [1,2,3],
            # we want the first line to essentially check the "-1"th element (and come up empty)
            # we can do this by getting the length difference between the list and max_length
            # and modifying the y value by that
            offset = len(arrangement[x]) - max_height
            yt = y + offset

            if yt < len(arrangement[x]) and yt >= 0:
                # show the element
                part_str = part(arrangement[x][yt])
            else:
                # show the bare tower
                part_str = tower_char.center(spacing)

            line += part_str

        lines += "  " + line + "\n"

    lines += "    {a}".format(
        a=(floor_char * (spacing - 4))
    ) * len(arrangement)

    lines += "\n\nscratch: "
    if scratch is not None:
        lines += render_block(scratch)
    lines += " " * spacing
    lines += "\n"

    print("\u001b[H\n"+lines)
