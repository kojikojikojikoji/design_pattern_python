"""Pythonic alternatives to the classic Singleton class.

The GoF formulated Singleton for languages where *classes* are the only
tool for controlling instantiation. Python has two lighter mechanisms
that deliver "one shared object per process" with no metaclass or
``__new__`` tricks:

1. **A module-level instance.** Modules are themselves singletons:
   Python imports a module once, caches it in ``sys.modules``, and every
   subsequent import returns the cached module. An object created at
   module level is therefore created exactly once per process.

2. **A cached factory function.** ``functools.cache`` memoises the
   factory, so the first call creates the object and every later call
   returns that same object. Bonus: creation is *lazy* (nothing happens
   until first use) and *resettable* (``cache_clear()`` — handy in tests).

Note that :class:`Settings` itself is a completely ordinary class — the
"singleton-ness" lives in *how it is exposed*, not in the class. That is
the Pythonic shift in mindset.
"""

import functools
from typing import Any


class Settings:
    """A plain key-value settings object. No singleton machinery at all —
    which is exactly the point: it stays trivially constructible in tests
    (``Settings()`` gives you a fresh, isolated one whenever you want)."""

    def __init__(self) -> None:
        self._values: "dict[str, Any]" = {
            "app_name": "PatternsDemo",
            "debug": False,
        }

    def get(self, key: str, default: Any = None) -> Any:
        """Return the setting stored under ``key`` (or ``default``)."""
        return self._values.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Store ``value`` under ``key``."""
        self._values[key] = value


#: Alternative 1 — the module-level instance.
#: Created once, when this module is first imported; shared by every
#: importer thereafter (the import system guarantees it).
module_config: Settings = Settings()


@functools.cache
def get_config() -> Settings:
    """Alternative 2 — the cached factory.

    The first call constructs a :class:`Settings`; every subsequent call
    returns that same object. ``functools.cache`` is thread-safe for this
    purpose in CPython, lazy by nature, and ``get_config.cache_clear()``
    resets it — three things the classic Singleton has to hand-build.
    """
    return Settings()
