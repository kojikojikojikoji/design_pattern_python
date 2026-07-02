# `ui/` — the abstract side of the pattern

This package plays the role that a **UI toolkit author** would play in real life. It defines *what a widget family consists of* (buttons and checkboxes) and *what a factory for such a family looks like*, without knowing anything about light or dark themes — or any other concrete family.

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`button.py`](button.py) | **AbstractProduct A** | The interface every themed button satisfies: `label`, `theme`, `render()`. |
| [`checkbox.py`](checkbox.py) | **AbstractProduct B** | The interface every themed checkbox satisfies: adds `toggle()` because checkboxes carry state. |
| [`factory.py`](factory.py) | **AbstractFactory** | One creation method *per product kind*: `create_button()`, `create_checkbox()`. |

## The one rule of this package

> `ui/` must **never** import from `light_theme/`, `dark_theme/`, or any other concrete package.

The dependency arrow points one way only: concrete → abstract. That is what lets you add a whole new family (see the exercises in [`../README.md`](../README.md#10-exercises)) without editing this package — the Open/Closed Principle applied to *groups* of classes.

## Why one factory interface bundles several creation methods

```python
class UIFactory(ABC):
    @abstractmethod
    def create_button(self, label: str) -> Button: ...

    @abstractmethod
    def create_checkbox(self, label: str) -> Checkbox: ...
```

This is the difference between Abstract Factory and Factory Method. If buttons and checkboxes each had an *independent* factory, nothing would stop a client from combining a `LightButtonFactory` with a `DarkCheckboxFactory` and shipping a mixed-theme screen. By putting all creation methods on **one** interface, choosing the family becomes a single decision — pick the factory — and consistency is enforced by construction, not by code review.

## Why every product declares a `theme` property

The abstract interfaces require each widget to report which family it belongs to. That makes the pattern's central promise — *"products from one factory always match"* — **testable**: `test_products_from_one_factory_form_a_consistent_family` in [`../tests/`](../tests/) asserts it directly instead of trusting the class names.

## Why `ABC` + `@abstractmethod`

Declaring the creation methods with `@abstractmethod` means a factory that forgets one product kind **cannot even be instantiated** — Python raises `TypeError` at construction time instead of `AttributeError` when the missing widget is first requested. The test `test_incomplete_factory_cannot_be_instantiated` in [`../tests/`](../tests/) demonstrates this.
