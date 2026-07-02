"""Demo client for the Singleton pattern.

Run from the repository root:

    python -m singleton.main

The demo shows the classic ``__new__``-guarded Singleton (identity,
shared state, and a 32-thread construction race), then the two Pythonic
alternatives: a module-level instance and a ``functools.cache`` factory.
"""

import threading

from . import alternatives
from .alternatives import get_config, module_config
from .app_config import AppConfig


def race_to_construct(thread_count: int = 32) -> int:
    """Have ``thread_count`` threads construct ``AppConfig()`` at once
    and return how many distinct instances came out (should be 1)."""
    barrier = threading.Barrier(thread_count)
    instances: list[AppConfig] = []
    record = threading.Lock()

    def construct() -> None:
        barrier.wait()  # line everyone up so they hit __new__ together
        instance = AppConfig()
        with record:
            instances.append(instance)

    threads = [threading.Thread(target=construct) for _ in range(thread_count)]
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join()
    return len({id(instance) for instance in instances})


def main() -> None:
    print("=== 1. Classic Singleton: every call returns the same object ===")
    config_a = AppConfig()
    config_b = AppConfig()
    print(f"config_a is config_b: {config_a is config_b}")

    config_a.set("debug", True)  # write through one reference...
    print(f"config_b.get('debug'): {config_b.get('debug')}  (state is shared)")
    print()

    print("=== 2. Thread safety: 32 threads race to construct AppConfig() ===")
    print(f"distinct instances created: {race_to_construct()}")
    print()

    print("=== 3. Pythonic alternative: a module-level instance ===")
    # 'alternatives.module_config' and the directly imported name are the
    # same object because the module itself is imported exactly once.
    print(f"module_config is alternatives.module_config: "
          f"{module_config is alternatives.module_config}")
    print()

    print("=== 4. Pythonic alternative: a functools.cache factory ===")
    print(f"get_config() is get_config(): {get_config() is get_config()}")
    print()

    print("One process, one instance - however you ask for it.")


if __name__ == "__main__":
    main()
