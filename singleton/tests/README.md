# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Singleton pattern (or its Pythonic alternatives) gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s singleton -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_every_construction_returns_the_same_instance` | `AppConfig()` is an *access point*, not a constructor — identity, not equality. |
| `test_state_is_shared_across_all_references` | One instance means one state: a write through any reference is visible through every other. |
| `test_reconstruction_does_not_reset_state` | The classic Python trap is avoided: state lives in `__new__`, so calling `AppConfig()` again can't wipe it (an `__init__` would). |
| `test_defaults_are_present_on_first_use` | The single instance is born fully initialised — no separate "setup" call to forget. |
| `test_concurrent_construction_yields_exactly_one_instance` | The lock + double-check in `__new__` closes the check-then-create race: 32 threads released by a `Barrier` still produce exactly one instance. |
| `test_module_level_instance_is_shared_via_the_import_system` | Modules are cached in `sys.modules`, so a module-level object is Python's native singleton. |
| `test_cached_factory_returns_the_same_object_every_call` | `functools.cache` memoises a factory into a lazy one-line singleton. |
| `test_cached_factory_is_resettable_for_tests` | `cache_clear()` gives the cached-factory approach the test-isolation escape hatch the classic class must hand-build (`_reset_for_testing`). |

## A note for learners

Notice the `setUp` in `TestClassicSingleton`: it must call `AppConfig._reset_for_testing()` because a Singleton is **global state** and would otherwise leak between tests. The Pythonic-alternatives tests need no such ceremony for the module instance, and a one-liner for the cached factory. That asymmetry *is* the trade-off discussed in [`../README.md`](../README.md#8-when-to-use-it-and-when-not-to) — you can read it directly out of the test file.
