"""Demo client for the Composite pattern.

Run from the repository root:

    python -m composite.main

The point to notice: after the tree is built, the client treats a single
file and a whole directory tree **identically** — same ``size`` property,
same ``render_tree`` call. No isinstance checks anywhere.
"""

from .filesystem.directory import Directory
from .filesystem.entry import Entry
from .filesystem.file import File


def main() -> None:
    # Build the tree. Directory.add returns self, so construction chains.
    bin_dir = Directory("bin").add(
        File("vi", 10000),
        File("latex", 15000),
    )
    home = Directory("home").add(
        Directory("alice").add(File("diary.html", 100)),
    )
    root = Directory("root").add(bin_dir, home, File("readme.txt", 5500))

    print("=== The whole tree, from the root ===")
    print(root.render_tree())

    print()
    print("=== Uniform treatment: leaf and composite through one interface ===")
    entries: list[Entry] = [File("standalone.txt", 42), bin_dir, root]
    for entry in entries:
        # The client cannot tell (and does not care) which is which.
        print(f"{entry.name}: {entry.size} bytes")

    print()
    print("=== A tree must stay a tree: cycles are rejected ===")
    try:
        home.add(root)  # root already contains home
    except ValueError as error:
        print(f"ValueError caught: {error}")


if __name__ == "__main__":
    main()
