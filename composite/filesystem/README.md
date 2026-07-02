# `filesystem/` — the three roles of the Composite pattern

This package models a file-system tree with exactly the three classes GoF prescribes — one per role.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`entry.py`](entry.py) | **Component** | The uniform interface: `name`, `size`, `render_tree()`. Also hosts the shared tree-rendering logic. |
| [`file.py`](file.py) | **Leaf** | A node with no children; its `size` is its own size — the recursion's base case. |
| [`directory.py`](directory.py) | **Composite** | Holds `list[Entry]` children; implements every operation by delegating to them. |

## The load-bearing type annotation

```python
self._children: list[Entry] = []
```

`Directory` stores children as the abstract `Entry` — not as `File | Directory`. That single annotation is why:

- a directory can contain files and directories **mixed**, without telling them apart;
- trees nest to arbitrary depth with zero additional code;
- new node types (a `Symlink`, say) slot in without touching this package's existing classes.

And the recursion it enables reads like the pattern's definition:

```python
@property
def size(self) -> int:
    return sum(child.size for child in self._children)
```

`child.size` resolves to `File.size` (base case) or `Directory.size` (recursive case) — chosen by polymorphism, not by `isinstance`.

## Design choices worth noticing

**Safe, not transparent.** `add` exists only on `Directory`. Calling `File("x").add(...)` is not a runtime exception — it is an `AttributeError`-shaped mistake that `hasattr`, autocomplete and type checkers catch *before* runtime. The trade-off against GoF's transparent variant (declare `add` on `Entry`, raise in leaves) is discussed in [`../README.md`](../README.md#4-code-walkthrough), and exercise 3 there has you build the other side.

**A tree must stay a tree.** `Directory.add` rejects any entry whose subtree already contains the target directory (or the directory itself), raising `ValueError`. Without this guard, `home.add(root)` would create a cycle and `size`/`render_tree` would recurse forever. Composites that mutate at runtime should defend their own shape invariant.

**Fluent building.** `add(*entries)` returns `self`, so demo trees assemble declaratively:

```python
root = Directory("root").add(bin_dir, home, File("readme.txt", 5500))
```

**`File` and `Directory` are `@final`.** Extension is meant to happen by adding new `Entry` subclasses (new node types), not by subclassing the two canonical roles into variants.

## Try it

```bash
# from the repository root
python -m composite.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to add a sibling leaf type to this very package.
