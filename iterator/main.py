"""Demo client for the Iterator pattern.

Run from the repository root:

    python -m iterator.main

The point to notice: the same shelf is traversed three ways — the
explicit GoF way, the Python for-loop way, and the comprehension way —
and the client never touches the shelf's internal storage in any of them.
"""

from .bookshelf.book import Book
from .bookshelf.book_shelf import BookShelf


def main() -> None:
    shelf = BookShelf()
    for title in (
        "Around the World in 80 Days",
        "Bible",
        "Cinderella",
        "Daddy-Long-Legs",
    ):
        shelf.append_book(Book(title))

    print("--- GoF style: explicit iterator object ---")
    iterator = shelf.iterator()
    while iterator.has_next():
        book = iterator.next()
        print(book.title)

    print()
    print("--- Pythonic style: the same iterator drives a for loop ---")
    for book in shelf:
        print(book.title)

    print()
    print("--- Pythonic style: comprehensions, len-free and index-free ---")
    initials = [book.title[0] for book in shelf]
    print(f"Shelf holds {len(shelf)} books with initials {initials}")


if __name__ == "__main__":
    main()
