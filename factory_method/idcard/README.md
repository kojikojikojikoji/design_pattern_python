# `idcard/` — the concrete side of the pattern

This package plays the role of an **application developer using the framework**. It plugs a specific product family — ID cards — into the abstract machinery defined in [`../framework/`](../framework/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`id_card.py`](id_card.py) | **ConcreteProduct** | An ID card with an owner and a serial number; implements `use()`. |
| [`id_card_factory.py`](id_card_factory.py) | **ConcreteCreator** | Instantiates `IDCard`s, assigns serial numbers, keeps a registry of every card issued. |

## What to notice

**Only the hooks are implemented.** `IDCardFactory` defines `create_product` and `register_product` — nothing else. The `create()` procedure (create → register → return) is inherited untouched from `framework.Factory`. If you find yourself re-implementing `create()`, you are fighting the pattern.

**The factory owns creation policy.** Serial numbers are computed inside the factory:

```python
def create_product(self, owner: str) -> IDCard:
    serial = len(self._registry) + 100
    return IDCard(owner, serial)
```

Client code physically cannot mint a card with a forged serial *through the factory*, and every card issued via `create()` is guaranteed to be in `registered_cards`. This is the practical payoff of routing creation through one point — compare with calling `IDCard("Alice", 999)` all over a codebase.

**This package depends on `framework/`, never the reverse.** To add a different product family (e.g. `TVCard`), you would create a *sibling* package that also imports from `framework/` — you would not touch this one. Each concrete family stays independent and disposable.

## Try it

```bash
# from the repository root
python -m factory_method.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to build a sibling of this very package.
