# `renderers/` — the Implementor axis (how it is drawn)

This package is the side of the bridge that **does the low-level work**. It defines the primitive operations drawing is built from, and ships three interchangeable backends.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`renderer.py`](renderer.py) | **Implementor** | The primitive interface: `render_circle(radius)`, `render_square(side)`. |
| [`vector_renderer.py`](vector_renderer.py) | **ConcreteImplementor** | Draws as resolution-independent curves. |
| [`raster_renderer.py`](raster_renderer.py) | **ConcreteImplementor** | Draws as pixels (and says how many). |
| [`ascii_renderer.py`](ascii_renderer.py) | **ConcreteImplementor** | Draws as terminal-friendly characters. |

## The one rule of this package

> `renderers/` must **never** import from `shapes/`.

Renderers know how to put a circle or a square somewhere. They do not know what a `BorderedCircle` is — and they never will, even as the shape hierarchy grows. This one-way ignorance is what lets the two axes evolve independently; the test `test_new_renderer_plugs_in_without_touching_any_shape` in [`../tests/`](../tests/) demonstrates the payoff from the other direction.

## Why the interface is deliberately primitive

GoF calls the implementor's methods *primitive operations*, in contrast with the abstraction's *higher-level operations*. The split matters:

- **Primitives here:** "render a circle of radius r", "render a square of side s".
- **Composed behaviour there:** "a circle inside a border" = one `render_circle` + one `render_square`, assembled by `BorderedCircle` in [`../shapes/`](../shapes/).

Keep the primitive set small and orthogonal. Every method added here must be implemented by *all* backends (that is the cost of growing this interface — exercise 2 in [`../README.md`](../README.md#10-exercises) makes you feel it), so promote a behaviour to a primitive only when shapes genuinely cannot compose it from what exists.

## Why the concrete renderers are `@final`

Each backend is a complete, self-contained strategy for drawing. Variation is meant to happen by writing a **sibling** (a fourth renderer), not by subclassing `RasterRenderer` into something that half-overrides its arithmetic. `typing.final` documents that intent to readers and type checkers.
