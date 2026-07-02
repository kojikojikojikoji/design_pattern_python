"""Demo client for the Visitor pattern.

Run from the repository root:

    python -m visitor.main

The point to notice: two completely different operations (listing and
size measurement) run over the same tree, and the element classes in
``filesystem/`` contain neither operation — only ``accept``.
"""

from .filesystem.directory import Directory
from .filesystem.file import File
from .visitors.list_visitor import ListVisitor
from .visitors.size_visitor import SizeVisitor


def build_tree() -> Directory:
    """Build a small, fixed file-system tree (same shape every run)."""
    root = Directory("root")

    bin_dir = Directory("bin")
    bin_dir.add(File("vi", 10000)).add(File("latex", 20000))

    tmp_dir = Directory("tmp")  # deliberately empty

    usr_dir = Directory("usr")
    alice = Directory("alice")
    alice.add(File("diary.html", 100)).add(File("index.html", 200))
    bob = Directory("bob")
    bob.add(File("game.doc", 400))
    usr_dir.add(alice).add(bob)

    root.add(bin_dir).add(tmp_dir).add(usr_dir)
    return root


def main() -> None:
    root = build_tree()

    # Operation 1: render the tree. The elements don't know how.
    lister = ListVisitor()
    root.accept(lister)
    print("Listing produced by ListVisitor:")
    print(lister.report())
    print()

    # Operation 2: measure the tree. Same elements, different visitor.
    sizer = SizeVisitor()
    root.accept(sizer)
    print(f"Total size measured by SizeVisitor: {sizer.total} bytes")

    # Visitors work on any subtree, too.
    for subtree in root:
        sub_sizer = SizeVisitor()
        subtree.accept(sub_sizer)
        print(f"  /root/{subtree.name}: {sub_sizer.total} bytes")


if __name__ == "__main__":
    main()
