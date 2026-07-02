"""AppConfig — the classic Singleton, done carefully.

In the Singleton pattern, a class guarantees it has **at most one
instance** and provides a global access point to it. Python's hook for
intercepting instance creation is ``__new__``, so that is where the guard
lives. Two details separate a correct implementation from a folklore one:

* **Thread safety.** Two threads calling ``AppConfig()`` at the same
  moment could both see ``_instance is None`` and build two instances.
  A lock (with the *double-checked locking* idiom, so the common path
  stays lock-free) closes that race.

* **No ``__init__``.** Python calls ``__init__`` on the result of
  ``__new__`` **every** time the class is called — so a Singleton that
  initialises state in ``__init__`` silently wipes its own state on every
  ``AppConfig()`` call. State is therefore initialised exactly once,
  inside the locked section of ``__new__``.

See ``alternatives.py`` for the more Pythonic ways to get "one shared
object per process" without any of this machinery.
"""

import threading
from typing import Any, ClassVar, Optional


class AppConfig:
    """Process-wide application configuration; ``AppConfig()`` always
    returns the same instance.

    The public API is an ordinary key-value store (:meth:`get` /
    :meth:`set`). The Singleton machinery is confined to ``__new__`` and
    the two class attributes below.
    """

    _instance: ClassVar[Optional["AppConfig"]] = None
    _lock: ClassVar[threading.Lock] = threading.Lock()

    _settings: "dict[str, Any]"  # created once, in __new__

    def __new__(cls) -> "AppConfig":
        if cls._instance is None:  # fast path: no locking once created
            with cls._lock:
                # Double-checked: another thread may have won the race
                # between our first check and acquiring the lock.
                if cls._instance is None:
                    instance = super().__new__(cls)
                    instance._settings = {
                        "app_name": "PatternsDemo",
                        "debug": False,
                    }
                    cls._instance = instance
        return cls._instance

    def get(self, key: str, default: Any = None) -> Any:
        """Return the setting stored under ``key`` (or ``default``)."""
        return self._settings.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Store ``value`` under ``key`` — visible to every holder of
        the (single) instance, i.e. to the whole process."""
        self._settings[key] = value

    @classmethod
    def _reset_for_testing(cls) -> None:
        """Discard the instance so each test starts from a clean slate.

        Global state is the Singleton's biggest liability (see README
        section 8); an explicit, clearly-named escape hatch for tests is
        the least-bad way to live with it.
        """
        with cls._lock:
            cls._instance = None

    def __repr__(self) -> str:
        return f"AppConfig(id=0x{id(self):x}, settings={self._settings})"
