# Design Patterns in Python

[![tests](https://github.com/kojikojikojikoji/python-design-patterns/actions/workflows/tests.yml/badge.svg)](https://github.com/kojikojikojikoji/python-design-patterns/actions/workflows/tests.yml)

All **23 classic (GoF) design patterns** implemented in modern, dependency-free Python — written as **hands-on tutorials**, not just code dumps. Every pattern is a self-contained package with a runnable demo, a test suite, and a README that explains the problem, the solution, real-world use cases, Pythonic alternatives, and exercises.

## Requirements

- Python **3.9+** (standard library only — nothing to install)

## Pattern catalog

### Creational — how objects get made

| Pattern | One-line intent | Tutorial | Demo |
| --- | --- | --- | --- |
| **Factory Method** | Let subclasses decide which class to instantiate | [factory_method/](factory_method/) | `python -m factory_method.main` |
| **Abstract Factory** | Create whole families of related objects | [abstract_factory/](abstract_factory/) | `python -m abstract_factory.main` |
| **Builder** | Assemble a complex object step by step | [builder/](builder/) | `python -m builder.main` |
| **Prototype** | Create objects by cloning a registered exemplar | [prototype/](prototype/) | `python -m prototype.main` |
| **Singleton** | Guarantee exactly one shared instance | [singleton/](singleton/) | `python -m singleton.main` |

### Structural — how objects compose

| Pattern | One-line intent | Tutorial | Demo |
| --- | --- | --- | --- |
| **Adapter** | Make an incompatible API fit the interface you need | [adapter/](adapter/) | `python -m adapter.main` |
| **Bridge** | Let abstraction and implementation vary independently | [bridge/](bridge/) | `python -m bridge.main` |
| **Composite** | Treat single objects and trees of objects uniformly | [composite/](composite/) | `python -m composite.main` |
| **Decorator** | Stack extra behaviour onto an object at runtime | [decorator/](decorator/) | `python -m decorator.main` |
| **Facade** | Offer one simple entry point to a messy subsystem | [facade/](facade/) | `python -m facade.main` |
| **Flyweight** | Share heavy immutable state between many objects | [flyweight/](flyweight/) | `python -m flyweight.main` |
| **Proxy** | Stand in for an object to add lazy loading or access control | [proxy/](proxy/) | `python -m proxy.main` |

### Behavioral — how objects collaborate

| Pattern | One-line intent | Tutorial | Demo |
| --- | --- | --- | --- |
| **Chain of Responsibility** | Pass a request along handlers until one takes it | [chain_of_responsibility/](chain_of_responsibility/) | `python -m chain_of_responsibility.main` |
| **Command** | Turn requests into objects you can queue and undo | [command/](command/) | `python -m command.main` |
| **Interpreter** | Evaluate sentences of a small language with a class per rule | [interpreter/](interpreter/) | `python -m interpreter.main` |
| **Iterator** | Walk a collection without exposing its internals | [iterator/](iterator/) | `python -m iterator.main` |
| **Mediator** | Centralise how a group of objects talk to each other | [mediator/](mediator/) | `python -m mediator.main` |
| **Memento** | Snapshot and restore state without breaking encapsulation | [memento/](memento/) | `python -m memento.main` |
| **Observer** | Notify many dependents when one subject changes | [observer/](observer/) | `python -m observer.main` |
| **State** | Change behaviour by switching state objects, not if-else | [state/](state/) | `python -m state.main` |
| **Strategy** | Swap interchangeable algorithms at runtime | [strategy/](strategy/) | `python -m strategy.main` |
| **Template Method** | Fix an algorithm's skeleton, let subclasses fill the steps | [template_method/](template_method/) | `python -m template_method.main` |
| **Visitor** | Add new operations to an object tree without touching it | [visitor/](visitor/) | `python -m visitor.main` |

## How each tutorial is structured

Every pattern directory follows the same layout, so once you've read one you can navigate them all:

```
<pattern_name>/
├── README.md      # tutorial: problem → analogy → diagram → walkthrough → use cases → exercises
├── main.py        # runnable demo (python -m <pattern_name>.main)
├── <sub-package>/ # abstract vs concrete side, each with its own README explaining its GoF role
└── tests/         # the pattern's guarantees as an executable specification (stdlib unittest)
```

And every README walks the same 11 sections: the problem it solves, a real-world analogy, structure (with a Mermaid class diagram), a code walkthrough, how to run the demo (with exact expected output), how to run the tests, **real-world use cases**, when to use it — and when a plain Python idiom is better, related patterns, exercises, and references.

## Running

All commands are executed from the repository root:

```bash
# any pattern's demo
python -m observer.main

# one pattern's tests
python -m unittest discover -s strategy -t .

# the entire suite (all 23 patterns)
python -m unittest discover -s . -t .
```

## Suggested learning path

1. **Start here:** [template_method/](template_method/) → [factory_method/](factory_method/) — the pair teaches the single most reused idea (fixed skeleton, swappable steps).
2. **Everyday workhorses:** [strategy/](strategy/), [observer/](observer/), [decorator/](decorator/), [adapter/](adapter/), [facade/](facade/).
3. **Structure at scale:** [composite/](composite/), [iterator/](iterator/), [visitor/](visitor/), [bridge/](bridge/), [proxy/](proxy/).
4. **State & history:** [state/](state/), [command/](command/), [memento/](memento/), [chain_of_responsibility/](chain_of_responsibility/), [mediator/](mediator/).
5. **Creation, completed:** [abstract_factory/](abstract_factory/), [builder/](builder/), [prototype/](prototype/), [singleton/](singleton/).
6. **The curiosity:** [interpreter/](interpreter/) — rarely hand-rolled today, but it demystifies how parsers and `ast` work.

## Who is this for?

- Developers learning design patterns who want **runnable, tested, idiomatic-Python** examples rather than Java translations.
- Anyone preparing for interviews or code reviews who needs a quick, concrete refresher on when a pattern helps — and when it's overkill (each tutorial has a "when *not* to use it" section).

## References

- Gamma, Helm, Johnson, Vlissides — *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF)
- Hiroshi Yuki — *An Introduction to Design Patterns Learned in the Java Language*
- [Refactoring.Guru](https://refactoring.guru/design-patterns)

## License

MIT — use freely for learning and teaching.
