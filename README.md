# Design Patterns in Python

Classic (GoF) design patterns implemented in modern, dependency-free Python — written as **hands-on tutorials**, not just code dumps. Each pattern comes with a runnable demo, tests, and a README that explains the problem, the solution, real-world use cases, and exercises.

## Requirements

- Python **3.9+** (standard library only — nothing to install)

## Patterns

| Pattern | Category | Tutorial | Run the demo |
| --- | --- | --- | --- |
| **Factory Method** | Creational | [factory_method/README.md](factory_method/README.md) | `python -m factory_method.main` |
| **Template Method** | Behavioral | [template_pattern.py](template_pattern.py) *(single file — tutorial format coming)* | `python template_pattern.py` |

More patterns will be added over time, each following the same structure:

```
<pattern_name>/
├── README.md      # tutorial: problem → solution → walkthrough → use cases → exercises
├── main.py        # runnable demo (python -m <pattern_name>.main)
├── .../README.md  # every sub-package documents its role in the pattern
└── tests/         # the pattern's guarantees as executable tests
```

## Running

All commands are executed from the repository root:

```bash
# demo
python -m factory_method.main

# tests
python -m unittest discover -s factory_method -t .
```

## Who is this for?

- Developers learning design patterns who want **runnable, tested, idiomatic-Python** examples rather than Java translations.
- Anyone preparing for interviews or code reviews who needs a quick, concrete refresher on when a pattern helps — and when it's overkill (each tutorial has a "when *not* to use it" section).

## References

- Gamma, Helm, Johnson, Vlissides — *Design Patterns: Elements of Reusable Object-Oriented Software* (GoF)
- Hiroshi Yuki — *An Introduction to Design Patterns Learned in the Java Language*
- [Refactoring.Guru](https://refactoring.guru/design-patterns)

## License

MIT — use freely for learning and teaching.
