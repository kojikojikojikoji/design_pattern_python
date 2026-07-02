"""Tests for the Visitor example.

Run from the repository root:

    python -m unittest discover -s visitor -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

from __future__ import annotations

import unittest

from visitor.filesystem.directory import Directory
from visitor.filesystem.element import Element
from visitor.filesystem.file import File
from visitor.visitors.list_visitor import ListVisitor
from visitor.visitors.size_visitor import SizeVisitor
from visitor.visitors.visitor import Visitor


def small_tree() -> Directory:
    """root/ ├── notes.txt (100)  └── docs/ ├── a.txt (200) └── b.txt (300)"""
    docs = Directory("docs")
    docs.add(File("a.txt", 200)).add(File("b.txt", 300))
    root = Directory("root")
    root.add(File("notes.txt", 100)).add(docs)
    return root


class TestDoubleDispatch(unittest.TestCase):
    def test_accept_dispatches_on_the_element_type(self) -> None:
        """Double dispatch: each element routes the SAME visitor to the
        visit_* method matching its own concrete type — no isinstance."""
        calls: list[str] = []

        class SpyVisitor(Visitor):
            def visit_file(self, file: File) -> None:
                calls.append(f"file:{file.name}")

            def visit_directory(self, directory: Directory) -> None:
                calls.append(f"dir:{directory.name}")

        spy = SpyVisitor()
        File("x.txt", 1).accept(spy)
        Directory("home").accept(spy)
        self.assertEqual(calls, ["file:x.txt", "dir:home"])


class TestConcreteVisitors(unittest.TestCase):
    def test_size_visitor_totals_every_file_in_the_subtree(self) -> None:
        """One operation over the whole structure lives in one class."""
        sizer = SizeVisitor()
        small_tree().accept(sizer)
        self.assertEqual(sizer.total, 600)  # 100 + 200 + 300

    def test_list_visitor_renders_the_full_tree_with_paths(self) -> None:
        """Visitors own their traversal and its working state (the
        current path) — state the elements never have to carry."""
        lister = ListVisitor()
        small_tree().accept(lister)
        self.assertEqual(
            lister.report(),
            "/root (dir)\n"
            "/root/notes.txt (100 bytes)\n"
            "/root/docs (dir)\n"
            "/root/docs/a.txt (200 bytes)\n"
            "/root/docs/b.txt (300 bytes)",
        )

    def test_new_operation_requires_no_element_changes(self) -> None:
        """The pattern's payoff: operation #3 is a brand-new class defined
        HERE, and the filesystem/ package is not touched at all."""

        class CountVisitor(Visitor):
            def __init__(self) -> None:
                self.files = 0
                self.directories = 0

            def visit_file(self, file: File) -> None:
                self.files += 1

            def visit_directory(self, directory: Directory) -> None:
                self.directories += 1
                for child in directory:
                    child.accept(self)

        counter = CountVisitor()
        small_tree().accept(counter)
        self.assertEqual((counter.files, counter.directories), (3, 2))

    def test_visitors_work_on_any_subtree(self) -> None:
        """accept() is available on every element, so operations can be
        aimed at a single file or any directory, not just the root."""
        sizer = SizeVisitor()
        File("solo.bin", 42).accept(sizer)
        self.assertEqual(sizer.total, 42)


class TestPatternContracts(unittest.TestCase):
    def test_abstract_element_and_visitor_cannot_be_instantiated(self) -> None:
        """Element and Visitor are pure interfaces."""
        with self.assertRaises(TypeError):
            Element()  # type: ignore[abstract]
        with self.assertRaises(TypeError):
            Visitor()  # type: ignore[abstract]

    def test_incomplete_visitor_cannot_be_instantiated(self) -> None:
        """A visitor must handle EVERY element type — a forgotten case
        fails at construction time, not mid-traversal."""

        class HalfVisitor(Visitor):
            def visit_file(self, file: File) -> None:
                pass
            # visit_directory intentionally missing

        with self.assertRaises(TypeError):
            HalfVisitor()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
