"""The Abstraction side of the Bridge pattern.

This sub-package defines *what* can be drawn: the
:class:`~bridge.shapes.shape.Shape` abstraction, the concrete shapes
(circle, square) and a refined abstraction (bordered circle). Every shape
holds a :class:`~bridge.renderers.renderer.Renderer` — that reference is
the "bridge" between the two hierarchies.
"""
