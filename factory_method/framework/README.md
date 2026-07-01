# `framework/` — the abstract side of the pattern

This package plays the role that a **library or framework author** would play in real life. It defines *what a factory does* and *what a product is*, without knowing anything about ID cards — or any other concrete product.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`product.py`](product.py) | **Product** | The interface every creatable object must satisfy: `use()`. |
| [`factory.py`](factory.py) | **Creator** | The fixed creation procedure: `create()` = `create_product()` → `register_product()` → return. |

## The one rule of this package

> `framework/` must **never** import from `idcard/` (or any other concrete package).

The dependency arrow points one way only: concrete → abstract. That is what lets you add new product families (see the exercises in [`../README.md`](../README.md#10-exercises)) without ever editing this package — the Open/Closed Principle.

## Why `create()` is marked `@final`

```python
@final
def create(self, owner: str) -> Product:
    product = self.create_product(owner)
    self.register_product(product)
    return product
```

`create()` is a **template method**: it encodes an invariant of the whole system — *"no product exists without being registered"*. If subclasses could override it, that invariant would become a suggestion. `@final` (checked by type checkers such as mypy/pyright) turns the convention into a rule.

Subclasses customise behaviour only through the two abstract hooks:

- `create_product(owner)` — *which* class to instantiate and *how*
- `register_product(product)` — *where* to record it (memory, file, database…)

## Why `ABC` + `@abstractmethod`

Declaring the hooks with `@abstractmethod` means an incomplete factory **cannot even be instantiated** — Python raises `TypeError` at construction time instead of `AttributeError` deep inside `create()` at call time. Fail fast, fail loudly. The test `test_incomplete_factory_cannot_be_instantiated` in [`../tests/`](../tests/) demonstrates this.
