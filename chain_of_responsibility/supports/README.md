# `supports/` — the concrete side of the pattern

This package plays the role of an **application developer using the framework**. It plugs specific support capabilities into the abstract chain machinery defined in [`../framework/`](../framework/).

| File | Pattern role (GoF name) | Responsibility |
| --- | --- | --- |
| [`no_support.py`](no_support.py) | **ConcreteHandler** | Never resolves anything — a pure pass-through (intake desk / triage bot). |
| [`limit_support.py`](limit_support.py) | **ConcreteHandler** | Resolves tickets with `number < limit` — a support tier with a capability ceiling. |
| [`odd_support.py`](odd_support.py) | **ConcreteHandler** | Resolves odd-numbered tickets — deliberately arbitrary, to show any predicate composes. |
| [`special_support.py`](special_support.py) | **ConcreteHandler** | Resolves one exact ticket number — the specialist who owns a notorious incident. |

## What to notice

**Each handler is one predicate.** A concrete support implements `resolve()` and nothing else — no linking logic, no forwarding logic, no failure handling. All of that is inherited from `framework.Support`:

```python
class LimitSupport(Support):
    def resolve(self, ticket: Ticket) -> bool:
        return ticket.number < self._limit
```

If you find yourself overriding `handle()`, you are fighting the pattern.

**Handlers don't know each other.** `LimitSupport` has no idea whether a `SpecialSupport` sits in front of it or an `OddSupport` behind it. Order, membership and even *whether a chain exists at all* are decided by whoever assembles the chain (here, `main.py`). That is why the same handler classes can serve completely different escalation policies.

**"Never resolves" is a valid capability.** `NoSupport` always declines — and the chain simply flows through it. It's the degenerate handler that proves the walk is robust: pass-through stations cost nothing but a hop.

## Try it

```bash
# from the repository root
python -m chain_of_responsibility.main
```

Then try the exercises in [`../README.md`](../README.md#10-exercises) — the first one asks you to build a sibling of the handlers in this very package.
