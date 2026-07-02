# `shapes/` — the Abstraction axis (what is drawn)

This package is the side of the bridge that **clients talk to**. It defines what shapes exist and what high-level operations they offer, while delegating every primitive drawing step across the bridge to a [`Renderer`](../renderers/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`shape.py`](shape.py) | **Abstraction** | Holds the bridge reference (`self._renderer`); declares `draw()`. |
| [`circle.py`](circle.py) | **(concrete Abstraction)** | Owns circle geometry; forwards to `render_circle`. |
| [`square.py`](square.py) | **(concrete Abstraction)** | Owns square geometry; forwards to `render_square`. |
| [`bordered_circle.py`](bordered_circle.py) | **RefinedAbstraction** | Richer behaviour (a border) composed from existing primitives. |

## The one attribute that is the whole pattern

```python
class Shape(ABC):
    def __init__(self, renderer: Renderer) -> None:
        self._renderer = renderer     # HAS-A, chosen per instance
```

A shape **has** a renderer; it never **is** one. Because the pairing happens at construction time, `Circle(VectorRenderer(), 5)` and `Circle(RasterRenderer(), 5)` are two instances of *one* class — not two classes. The test `test_shape_delegates_via_composition_not_inheritance` in [`../tests/`](../tests/) pins this down.

## What a refined abstraction proves

`BorderedCircle` adds a feature (a snug square border) using only `render_circle` and `render_square`:

```python
def draw(self) -> str:
    circle = super().draw()
    border = self._renderer.render_square(2 * self._radius)
    return f"{circle}, inside a border: {border}"
```

No renderer was edited, so **every** renderer — including ones not yet written — supports borders automatically. When you extend this package, hold yourself to the same standard: if your new shape needs changes in [`../renderers/`](../renderers/), you are either missing a genuine primitive (fine, add it consciously — see exercise 2 in [`../README.md`](../README.md#10-exercises)) or leaking "how" concerns into "what" code (not fine).

## The one rule of this package

> `shapes/` may import the abstract `Renderer` type — never a *concrete* renderer.

The moment `circle.py` mentions `VectorRenderer`, the axes are welded together again and the bridge has collapsed.
