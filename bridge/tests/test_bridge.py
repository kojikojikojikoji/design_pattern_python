"""Tests for the Bridge pattern example.

Run from the repository root:

    python -m unittest discover -s bridge -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from bridge.renderers.ascii_renderer import AsciiRenderer
from bridge.renderers.raster_renderer import RasterRenderer
from bridge.renderers.renderer import Renderer
from bridge.renderers.vector_renderer import VectorRenderer
from bridge.shapes.bordered_circle import BorderedCircle
from bridge.shapes.circle import Circle
from bridge.shapes.shape import Shape
from bridge.shapes.square import Square

RENDERER_CLASSES = (VectorRenderer, RasterRenderer, AsciiRenderer)


class TestTwoIndependentAxes(unittest.TestCase):
    def test_same_shape_draws_differently_with_each_renderer(self) -> None:
        """The 'how' axis varies while the 'what' axis stays fixed."""
        outputs = {Circle(cls(), 5).draw() for cls in RENDERER_CLASSES}
        self.assertEqual(len(outputs), 3)  # three genuinely different results

    def test_one_renderer_instance_serves_every_shape(self) -> None:
        """The 'what' axis varies while the 'how' axis stays fixed."""
        renderer = VectorRenderer()
        self.assertEqual(
            Circle(renderer, 5).draw(),
            "[vector] circle(radius=5) drawn with smooth curves",
        )
        self.assertEqual(
            Square(renderer, 4).draw(),
            "[vector] square(side=4) drawn with smooth curves",
        )

    def test_all_combinations_work_from_n_plus_m_classes(self) -> None:
        """3 shapes x 3 renderers = 9 behaviours from only 6 concrete classes."""
        outputs = set()
        for renderer_cls in RENDERER_CLASSES:
            renderer = renderer_cls()
            for shape in (Circle(renderer, 5), Square(renderer, 4), BorderedCircle(renderer, 3)):
                outputs.add(shape.draw())
        self.assertEqual(len(outputs), 9)


class TestExtensibility(unittest.TestCase):
    def test_new_renderer_plugs_in_without_touching_any_shape(self) -> None:
        """Extending the implementor axis costs one class, zero edits."""

        class DebugRenderer(Renderer):  # defined here, shapes never knew it
            def render_circle(self, radius: float) -> str:
                return f"debug:circle:{radius:g}"

            def render_square(self, side: float) -> str:
                return f"debug:square:{side:g}"

        self.assertEqual(Circle(DebugRenderer(), 2).draw(), "debug:circle:2")

    def test_refined_abstraction_reuses_existing_primitives(self) -> None:
        """BorderedCircle adds behaviour using only what renderers offer."""
        drawn = BorderedCircle(RasterRenderer(), 3).draw()
        self.assertIn("circle(radius=3)", drawn)
        self.assertIn("square(side=6)", drawn)  # border = diameter-sized square


class TestPatternContracts(unittest.TestCase):
    def test_shape_delegates_via_composition_not_inheritance(self) -> None:
        """The bridge is a HAS-A reference: a shape never IS-A renderer."""
        circle = Circle(AsciiRenderer(), 1)
        self.assertNotIsInstance(circle, Renderer)
        self.assertIsInstance(circle.renderer, Renderer)

    def test_both_hierarchy_roots_are_pure_interfaces(self) -> None:
        """Shape and Renderer are abstract - only the leaves are usable."""
        with self.assertRaises(TypeError):
            Shape(VectorRenderer())  # type: ignore[abstract]
        with self.assertRaises(TypeError):
            Renderer()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
