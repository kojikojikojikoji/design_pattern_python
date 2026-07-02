"""Demo client for the Prototype pattern.

Run from the repository root:

    python -m prototype.main

The point to notice: after the two ``register`` calls, this client never
mentions ``Circle`` or ``Rectangle`` again. New objects come from
``registry.create(key)`` — cloning a pre-configured sample — and each
clone is fully independent of its prototype. The final section shows why
``clone()`` deliberately uses deepcopy rather than a shallow copy.
"""

import copy

from .registry import ShapeRegistry
from .shapes import Circle, Rectangle


def main() -> None:
    # Setup: the only place concrete classes appear. Imagine this being
    # driven by a config file or a plugin system instead.
    registry = ShapeRegistry()
    registry.register("alert-badge", Circle("alert badge", 12, ["alert", "red"]))
    registry.register("banner", Rectangle("hero banner", 300, 80, ["header"]))

    print(f"Registered prototypes: {', '.join(registry.keys)}")
    print()

    # Create by cloning — no constructors, no concrete class names.
    badge_a = registry.create("alert-badge")
    badge_b = registry.create("alert-badge")
    badge_b.tags.append("urgent")  # customise ONE clone

    print("Two clones of 'alert-badge', one customised after cloning:")
    print(f"  clone A   : {badge_a.describe()}")
    print(f"  clone B   : {badge_b.describe()}")
    print(f"  prototype : {registry.create('alert-badge').describe()}")
    print()

    banner = registry.create("banner")
    print(f"A fresh banner: {banner.describe()}")
    print(f"Clones are new objects: banner is not a second banner -> "
          f"{banner is not registry.create('banner')}")
    print()

    # The pitfall clone() protects you from: copy.copy is SHALLOW, so the
    # copy shares its mutable tags list with the original.
    original = Circle("shared-state demo", 5, ["clean"])
    shallow = copy.copy(original)
    shallow.tags.append("oops")

    print("Why clone() uses deepcopy — the shallow-copy pitfall:")
    print(f"  shallow copy shares the tags list: "
          f"{shallow.tags is original.tags}")
    print(f"  we tagged only the copy, yet the original now reads:")
    print(f"    {original.describe()}")
    print(f"  a deep clone stays independent:")
    deep = original.clone()
    deep.tags.append("safe")
    print(f"    original after tagging the deep clone: {original.describe()}")


if __name__ == "__main__":
    main()
