"""Demo client for the Interpreter pattern.

Run from the repository root:

    python -m interpreter.main

The point to notice: the program is DATA — a plain string. The client
parses it into a tree of Node objects and then asks the tree to execute
itself against a Robot. Change the string and the behaviour changes,
with no Python code modified anywhere.
"""

from .language.nodes import parse
from .robot.robot import Robot


def run(program_text: str) -> None:
    print(f"source : {program_text}")
    tree = parse(program_text)
    print(f"parsed : {tree!r}")
    robot = Robot()
    tree.execute(robot)
    for line in robot.log:
        print(f"  {line}")
    print(f"final  : position {robot.position}, facing {robot.heading}")


def main() -> None:
    print("--- Program 1: walk a square ---")
    run("program repeat 4 go right end end")

    print()
    print("--- Program 2: nested repeats ---")
    run("program repeat 2 repeat 2 go end right end end")


if __name__ == "__main__":
    main()
