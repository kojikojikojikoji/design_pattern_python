# `robot/` — the concrete side of the pattern

This package plays the role of an **application developer using the language**. It provides one concrete implementation of the [`CommandReceiver`](../language/receiver.py) interface that interpreted programs drive: a robot walking a 2-D grid.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`robot.py`](robot.py) | *(concrete receiver / the interpreter's "machine")* | Executes `go` / `turn_right` / `turn_left` on a grid; keeps a human-readable action log. |

## What to notice

**The robot knows no grammar.** It has never heard of `repeat`, `end`, tokens or parse trees. It exposes three motion primitives, and that's the entire coupling surface between the language and the world:

```python
class Robot(CommandReceiver):
    def go(self) -> None: ...          # one step in the current heading
    def turn_right(self) -> None: ...  # rotate 90° clockwise
    def turn_left(self) -> None: ...   # rotate 90° counter-clockwise
```

**State is minimal and observable.** Position `(x, y)`, a compass heading, and a log of every action taken. The log is what `main.py` prints — the visible trace of an interpreted program — and the `position`/`heading` properties are what the tests assert on (the square-walking program must return the robot to `(0, 0)` facing north).

**Receivers are swappable.** Because programs are interpreted against the abstract `CommandReceiver`, this package is one of *many possible* back ends. The test suite exercises the language with a plain recording double, and exercise 2 in [`../README.md`](../README.md#10-exercises) asks you to add an ASCII-drawing sibling. None of those additions touch `language/`.

## Try it

```bash
# from the repository root
python -m interpreter.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the second one asks you to build a sibling receiver of this very package.
