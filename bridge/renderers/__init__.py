"""The Implementor side of the Bridge pattern.

This sub-package defines *how* drawing happens: the abstract
:class:`~bridge.renderers.renderer.Renderer` interface plus three
interchangeable implementations (vector, raster, ASCII). It knows nothing
about the shape hierarchy that will use it.
"""
