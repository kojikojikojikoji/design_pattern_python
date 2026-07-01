"""Demo client for the Factory Method pattern.

Run from the repository root:

    python -m factory_method.main

The point to notice: this client works with the abstract ``Factory`` and
``Product`` types. Swap ``IDCardFactory`` for any other concrete factory
and the rest of the code keeps working unchanged.
"""

from .framework.factory import Factory
from .framework.product import Product
from .idcard.id_card_factory import IDCardFactory


def main() -> None:
    # The only line that mentions a concrete class. Everything below it
    # depends solely on the abstract Factory / Product interfaces.
    factory: Factory = IDCardFactory()

    cards: list[Product] = [
        factory.create("Alice"),
        factory.create("Bob"),
        factory.create("Charlie"),
    ]

    for card in cards:
        card.use()


if __name__ == "__main__":
    main()
