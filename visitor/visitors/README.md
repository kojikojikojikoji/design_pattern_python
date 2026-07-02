# `visitors/` — the operations (the *open* side)

This package is where operations over the tree live — and where **all future operations will live too**. Each visitor class is one complete algorithm over the whole element hierarchy, kept in one file instead of being smeared as one method per element class.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`visitor.py`](visitor.py) | **Visitor** | The operation interface: one `visit_*` method per concrete element type. |
| [`list_visitor.py`](list_visitor.py) | **ConcreteVisitor** | Renders the tree as an indented full-path listing. |
| [`size_visitor.py`](size_visitor.py) | **ConcreteVisitor** | Totals the bytes of every file in a subtree. |

## What to notice

**One operation = one class = one file.** `ListVisitor` is *everything* about listing: the formatting, the traversal, and the working state (`_current_path`, `_lines`). Without the pattern, that logic would be split into `File.list_line()` and `Directory.list_lines()` — and the traversal state would have to be threaded through parameters or globals.

**Visitors own their traversal.** `Directory.accept` does not recurse; the visitor does:

```python
def visit_directory(self, directory: Directory) -> None:
    ...
    for child in directory:
        child.accept(self)     # recurse — because THIS operation wants to
```

`SizeVisitor` recurses too, but silently; another visitor might not recurse at all. The tree exposes its shape (`__iter__`), each operation picks its walk.

**Visitors accumulate state across the walk.** `SizeVisitor.total` grows as the traversal proceeds. This is the natural home for "fold over a structure" logic — compare `ast.NodeVisitor` collecting names from a Python syntax tree.

**Adding operation #3 touches nothing outside this package.** A `CountVisitor`, a `SearchVisitor`, an `XmlExportVisitor` — each is a new sibling file here. `filesystem/` stays byte-for-byte identical. The test `test_new_operation_requires_no_element_changes` in [`../tests/`](../tests/) proves it by defining a brand-new visitor inside the test itself.

## The corresponding cost

`Visitor` declares one abstract method per element type. If the element set ever grows, every class in this package gains a mandatory method (enforced by `abc` — an incomplete visitor won't even instantiate). Cheap operations, expensive elements: that's the trade this package signs up for.

## Try it

```bash
# from the repository root
python -m visitor.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to build a sibling of these very classes.
