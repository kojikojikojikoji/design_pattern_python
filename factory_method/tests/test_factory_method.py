"""Tests for the Factory Method example.

Run from the repository root:

    python -m unittest discover factory_method

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from factory_method.framework.factory import Factory
from factory_method.framework.product import Product
from factory_method.idcard.id_card import IDCard
from factory_method.idcard.id_card_factory import IDCardFactory


class TestIDCardFactory(unittest.TestCase):
    def setUp(self) -> None:
        self.factory = IDCardFactory()

    def test_create_returns_a_product(self) -> None:
        """Clients can treat the result as an abstract Product."""
        card = self.factory.create("Alice")
        self.assertIsInstance(card, Product)
        self.assertIsInstance(card, IDCard)

    def test_created_card_belongs_to_owner(self) -> None:
        card = self.factory.create("Alice")
        self.assertEqual(card.owner, "Alice")

    def test_every_created_card_is_registered(self) -> None:
        """create() guarantees registration — that's the template method."""
        self.factory.create("Alice")
        self.factory.create("Bob")
        owners = [card.owner for card in self.factory.registered_cards]
        self.assertEqual(owners, ["Alice", "Bob"])

    def test_serial_numbers_are_unique_and_sequential(self) -> None:
        """Centralising creation lets the factory own the serial policy."""
        serials = [self.factory.create(name).serial for name in ("A", "B", "C")]
        self.assertEqual(serials, [100, 101, 102])


class TestFrameworkContracts(unittest.TestCase):
    def test_abstract_classes_cannot_be_instantiated(self) -> None:
        """Factory and Product are pure interfaces."""
        with self.assertRaises(TypeError):
            Factory()  # type: ignore[abstract]
        with self.assertRaises(TypeError):
            Product()  # type: ignore[abstract]

    def test_incomplete_factory_cannot_be_instantiated(self) -> None:
        """A subclass must implement BOTH hook methods."""

        class HalfFactory(Factory):
            def create_product(self, owner: str) -> Product:
                return IDCard(owner, 0)
            # register_product intentionally missing

        with self.assertRaises(TypeError):
            HalfFactory()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
