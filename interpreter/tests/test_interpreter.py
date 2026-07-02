"""Tests for the Interpreter example.

Run from the repository root:

    python -m unittest discover -s interpreter -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest
from typing import List

from interpreter.language.errors import ParseError
from interpreter.language.nodes import parse
from interpreter.language.receiver import CommandReceiver
from interpreter.robot.robot import Robot


class RecordingReceiver(CommandReceiver):
    """A test double proving the language drives ANY CommandReceiver."""

    def __init__(self) -> None:
        self.calls: List[str] = []

    def go(self) -> None:
        self.calls.append("go")

    def turn_right(self) -> None:
        self.calls.append("right")

    def turn_left(self) -> None:
        self.calls.append("left")


class TestParsing(unittest.TestCase):
    def test_parser_builds_one_node_per_grammar_rule(self) -> None:
        """The syntax tree mirrors the grammar — visible in its repr."""
        tree = parse("program repeat 4 go right end end")
        self.assertEqual(repr(tree), "[program [[repeat 4 [go, right]]]]")

    def test_missing_end_is_a_parse_error(self) -> None:
        """Grammar violations fail at PARSE time, before anything runs."""
        with self.assertRaises(ParseError):
            parse("program go right")

    def test_unknown_command_is_a_parse_error(self) -> None:
        """Only the grammar's terminals are accepted."""
        with self.assertRaises(ParseError):
            parse("program fly end")

    def test_program_keyword_is_required(self) -> None:
        """Every sentence must derive from the start symbol <program>."""
        with self.assertRaises(ParseError):
            parse("repeat 4 go end")


class TestInterpretation(unittest.TestCase):
    def test_repeat_executes_its_body_the_given_number_of_times(self) -> None:
        """A nonterminal node interprets itself by looping over its child."""
        receiver = RecordingReceiver()
        parse("program repeat 3 go end end").execute(receiver)
        self.assertEqual(receiver.calls, ["go", "go", "go"])

    def test_nested_repeats_multiply(self) -> None:
        """Recursion in the grammar becomes recursion in the tree, free."""
        receiver = RecordingReceiver()
        parse("program repeat 2 repeat 2 go end right end end").execute(receiver)
        self.assertEqual(
            receiver.calls,
            ["go", "go", "right", "go", "go", "right"],
        )

    def test_language_is_decoupled_from_the_concrete_receiver(self) -> None:
        """The same tree drives any receiver — here, a plain recorder."""
        receiver = RecordingReceiver()
        parse("program go left go end").execute(receiver)
        self.assertEqual(receiver.calls, ["go", "left", "go"])

    def test_the_square_program_returns_the_robot_home(self) -> None:
        """End-to-end: text -> tree -> execution on the real receiver."""
        robot = Robot()
        parse("program repeat 4 go right end end").execute(robot)
        self.assertEqual(robot.position, (0, 0))
        self.assertEqual(robot.heading, "north")
        self.assertEqual(len(robot.log), 8)  # 4 moves + 4 turns


if __name__ == "__main__":
    unittest.main()
