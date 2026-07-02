# `filesystem/` — the Element hierarchy (the *stable* side)

This package is the object structure being operated on: a tree of files and directories. In a real system this is the side that is **hard to change** — many modules depend on it, it may be serialized, it may live in a published library. The Visitor pattern exists precisely so this side can stay frozen while operations multiply.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`element.py`](element.py) | **Element** | The interface every node satisfies: `accept(visitor)`. |
| [`file.py`](file.py) | **ConcreteElement** (leaf) | A named file with a size; dispatches to `visit_file`. |
| [`directory.py`](directory.py) | **ConcreteElement** (composite) | A named, iterable collection of children; dispatches to `visit_directory`. |

## The one rule of this package

> Elements know **which** visitor method matches their type — and nothing else about any visitor.

Each concrete element's `accept` is exactly one line:

```python
class File(Element):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_file(self)          # "I am a File."

class Directory(Element):
    def accept(self, visitor: Visitor) -> None:
        visitor.visit_directory(self)     # "I am a Directory."
```

That one line is the second half of **double dispatch**: the *first* dispatch picked the element's `accept` (polymorphism on the element), and this call picks the visitor method (explicit dispatch on the element's own type). Together they select behaviour based on **two** runtime types — something a single virtual call cannot do — with no `isinstance` anywhere.

## Why `Directory.accept` does not traverse its children

It would work, but it would hard-code one traversal order into the tree forever. By keeping `accept` minimal and exposing children through `__iter__`, **each visitor decides its own traversal**: `ListVisitor` recurses depth-first and tracks the current path; a hypothetical `TopLevelVisitor` could choose not to recurse at all. Operations own their algorithms — the tree owns only its shape.

## The trade-off you accept

Adding a new *operation* costs nothing here. Adding a new *element type* (say, `Symlink`) costs a lot everywhere: `Visitor` gains an abstract `visit_symlink`, and **every existing visitor must implement it**. That's not a flaw — it's the deal. Visitor is for structures whose element set is stable and whose operation set grows. See section 8 of [`../README.md`](../README.md#8-when-to-use-it-and-when-not-to).
