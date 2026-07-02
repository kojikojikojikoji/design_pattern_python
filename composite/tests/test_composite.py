"""Tests for the Composite pattern example.

Run from the repository root:

    python -m unittest discover -s composite -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from composite.filesystem.directory import Directory
from composite.filesystem.entry import Entry
from composite.filesystem.file import File


class TestUniformInterface(unittest.TestCase):
    def test_leaf_and_composite_share_the_component_interface(self) -> None:
        """A File and a Directory are both just Entry to client code."""
        self.assertIsInstance(File("a.txt", 1), Entry)
        self.assertIsInstance(Directory("docs"), Entry)

    def test_client_code_needs_no_isinstance_checks(self) -> None:
        """One function handles files and whole trees identically."""

        def total_size(entries: list[Entry]) -> int:  # knows only Entry
            return sum(entry.size for entry in entries)

        tree = Directory("d").add(File("a", 10), File("b", 20))
        self.assertEqual(total_size([File("c", 5), tree]), 35)


class TestRecursiveAggregation(unittest.TestCase):
    def test_leaf_reports_its_own_size(self) -> None:
        self.assertEqual(File("readme.txt", 5500).size, 5500)

    def test_directory_size_aggregates_the_whole_subtree(self) -> None:
        """The composite's operation is defined in terms of its children's."""
        root = Directory("root").add(
            Directory("bin").add(File("vi", 10000), File("latex", 15000)),
            File("readme.txt", 5500),
        )
        self.assertEqual(root.size, 30500)

    def test_empty_directory_has_size_zero(self) -> None:
        """The recursion's base case: a composite with no children."""
        self.assertEqual(Directory("empty").size, 0)


class TestTreeManagement(unittest.TestCase):
    def test_add_returns_self_so_trees_build_fluently(self) -> None:
        directory = Directory("d")
        self.assertIs(directory.add(File("a", 1)), directory)

    def test_safe_design_leaves_have_no_child_management(self) -> None:
        """The 'safe' variant: File.add does not even exist (vs raising)."""
        self.assertFalse(hasattr(File("a.txt", 1), "add"))

    def test_cycles_are_rejected_so_the_tree_stays_a_tree(self) -> None:
        """Adding an ancestor into its own subtree raises ValueError."""
        root = Directory("root")
        child = Directory("child")
        root.add(child)
        with self.assertRaises(ValueError):
            child.add(root)
        with self.assertRaises(ValueError):
            root.add(root)


if __name__ == "__main__":
    unittest.main()
