"""Tests for the Prototype example.

Run from the repository root:

    python -m unittest discover -s prototype -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import copy
import unittest

from prototype.registry import ShapeRegistry
from prototype.shape import Shape
from prototype.shapes import Circle, Rectangle


class TestCloning(unittest.TestCase):
    def setUp(self) -> None:
        self.prototype = Circle("badge", 12, ["alert", "red"])

    def test_clone_is_a_new_object_not_the_prototype(self) -> None:
        """Cloning creates, it never hands back the original."""
        clone = self.prototype.clone()
        self.assertIsNot(clone, self.prototype)
        self.assertIsInstance(clone, Circle)

    def test_clone_preserves_the_prototypes_configuration(self) -> None:
        """A clone starts as an exact copy of its prototype's state."""
        clone = self.prototype.clone()
        self.assertEqual(clone.label, "badge")
        self.assertEqual(clone.radius, 12)
        self.assertEqual(clone.tags, ["alert", "red"])

    def test_mutating_a_clone_never_touches_the_prototype(self) -> None:
        """clone() is DEEP: no mutable state is shared with the original."""
        clone = self.prototype.clone()
        clone.tags.append("urgent")
        clone.radius = 99
        self.assertEqual(self.prototype.tags, ["alert", "red"])
        self.assertEqual(self.prototype.radius, 12)

    def test_shallow_copy_shares_nested_state_the_pitfall(self) -> None:
        """copy.copy would share the tags list — the bug clone() prevents."""
        shallow = copy.copy(self.prototype)
        self.assertIs(shallow.tags, self.prototype.tags)  # shared!
        shallow.tags.append("oops")
        self.assertIn("oops", self.prototype.tags)  # original corrupted


class TestShapeRegistry(unittest.TestCase):
    def setUp(self) -> None:
        self.registry = ShapeRegistry()
        self.registry.register("badge", Circle("badge", 12, ["alert"]))
        self.registry.register("banner", Rectangle("banner", 300, 80, ["header"]))

    def test_create_returns_clones_through_the_abstract_interface(self) -> None:
        """Clients get Shapes by key — concrete classes stay out of sight."""
        shape = self.registry.create("badge")
        self.assertIsInstance(shape, Shape)
        self.assertIsNot(shape, self.registry.create("badge"))

    def test_customising_a_created_object_never_corrupts_the_catalogue(self) -> None:
        """The registry hands out clones, so its samples stay pristine."""
        first = self.registry.create("badge")
        first.tags.append("mangled")
        second = self.registry.create("badge")
        self.assertEqual(second.tags, ["alert"])

    def test_a_tweaked_clone_can_be_registered_as_a_new_prototype(self) -> None:
        """New 'kinds' of object appear at runtime — no new classes."""
        urgent = self.registry.create("badge")
        urgent.tags.append("urgent")
        self.registry.register("urgent-badge", urgent)
        self.assertEqual(self.registry.create("urgent-badge").tags, ["alert", "urgent"])
        self.assertEqual(self.registry.create("badge").tags, ["alert"])

    def test_unknown_key_fails_fast_with_the_available_keys(self) -> None:
        """A typo raises immediately, and the message helps you fix it."""
        with self.assertRaises(KeyError) as ctx:
            self.registry.create("bdage")
        self.assertIn("badge", str(ctx.exception))
        self.assertIn("banner", str(ctx.exception))


if __name__ == "__main__":
    unittest.main()
