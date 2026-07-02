# `glyphs/` — the shared side of the pattern

This package contains the two classes that make sharing work: the heavy object worth sharing, and the factory that enforces the sharing.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`glyph.py`](glyph.py) | **Flyweight** (concrete) | The ASCII-art shape of one character — intrinsic state only, immutable, safe to share. |
| [`glyph_factory.py`](glyph_factory.py) | **FlyweightFactory** | Get-or-create with a cache: guarantees at most one `Glyph` per character. |

(GoF also lists an abstract *Flyweight* interface and an *UnsharedConcreteFlyweight*; with one concrete flyweight and Python's duck typing, this example omits both — see section 8 of [`../README.md`](../README.md).)

## Intrinsic state: what may live inside a flyweight

A `Glyph` stores exactly two things — its character and its shape:

```python
self._char = char
self._rows = _FONT[char]   # intrinsic state: the shape itself
```

Both depend only on *which character* this is, never on *where it is used*. That context-independence is the admission test for intrinsic state: if a field would differ between two occurrences of `'1'` in a banner, it does **not** belong in the glyph. Position, banner membership, usage count — all extrinsic, all the client's problem (see [`../banner.py`](../banner.py)). The test `test_glyph_holds_only_intrinsic_state` in [`../tests/`](../tests/) pins this down by inspecting `vars(glyph)`.

## Immutability is not optional

A shared object has many holders. If one banner could recolour "its" glyph, every other banner's output would change behind its back. So the flyweight exposes its state as an immutable `tuple` and offers no mutators. In the pattern's contract, *shared* implies *read-only* — treat any urge to add a setter here as a design alarm.

## Why the factory is essential

```python
def get(self, char: str) -> Glyph:
    if char not in self._pool:
        self._pool[char] = Glyph(char)
    return self._pool[char]
```

Sharing cannot be enforced by the flyweight class alone — anyone can call `Glyph("1")` twice. The factory is the choke point that turns "please share" into "sharing is guaranteed": as long as clients obtain glyphs via `factory.get(...)`, two `Glyph` objects for the same character cannot exist in that pool. This is why GoF makes the factory a first-class participant of the pattern, not an implementation detail.

`Glyph.instances_created` (a class-level counter) exists purely so the demo and tests can *prove* the guarantee: render 26 characters, observe 3 constructions.

## Try it

```bash
# from the repository root
python -m flyweight.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to extend the font in this package.
