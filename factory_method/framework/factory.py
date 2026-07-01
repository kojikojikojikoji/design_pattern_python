"""Abstract Factory (Creator) — defines *how* products are created.

:meth:`Factory.create` is a **Template Method**: it fixes the overall
creation procedure (create a product, then register it) while delegating
each step to abstract "factory methods" that subclasses implement.
This is the heart of the Factory Method pattern — the framework decides
*when* to create, the subclass decides *what* to create.
"""

from abc import ABC, abstractmethod
from typing import final

from .product import Product


class Factory(ABC):
    """Creator that produces :class:`Product` instances via a fixed procedure.

    Subclasses (e.g. ``IDCardFactory``) implement the two hook methods:

    * :meth:`create_product` — instantiate a concrete product
    * :meth:`register_product` — record the created product somewhere

    Client code only ever calls :meth:`create`, so the creation procedure
    stays consistent no matter which concrete factory is used.
    """

    @final
    def create(self, owner: str) -> Product:
        """Create and register a product for ``owner``.

        Marked ``@final``: subclasses must not change the procedure itself,
        only fill in the steps. This guarantees every product is registered.
        """
        product = self.create_product(owner)
        self.register_product(product)
        return product

    @abstractmethod
    def create_product(self, owner: str) -> Product:
        """Instantiate a concrete product for ``owner``."""
        raise NotImplementedError

    @abstractmethod
    def register_product(self, product: Product) -> None:
        """Record the created product (e.g. in a registry or database)."""
        raise NotImplementedError
