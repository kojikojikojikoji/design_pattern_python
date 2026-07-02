"""Tests for the Singleton example.

Run from the repository root:

    python -m unittest discover -s singleton -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import importlib
import threading
import unittest

from singleton.alternatives import get_config, module_config
from singleton.app_config import AppConfig


class TestClassicSingleton(unittest.TestCase):
    def setUp(self) -> None:
        # Global state is the Singleton's biggest liability; the explicit
        # reset hook keeps these tests independent of each other.
        AppConfig._reset_for_testing()

    def test_every_construction_returns_the_same_instance(self) -> None:
        """AppConfig() is an access point, not a constructor."""
        self.assertIs(AppConfig(), AppConfig())

    def test_state_is_shared_across_all_references(self) -> None:
        """A write through one reference is visible through every other."""
        AppConfig().set("debug", True)
        self.assertTrue(AppConfig().get("debug"))

    def test_reconstruction_does_not_reset_state(self) -> None:
        """The classic __init__ trap is avoided: state is initialised
        exactly once, in __new__, so later calls can't wipe it."""
        AppConfig().set("retries", 5)
        again = AppConfig()  # would call __init__ if one were defined
        self.assertEqual(again.get("retries"), 5)

    def test_defaults_are_present_on_first_use(self) -> None:
        """The single instance is born fully initialised."""
        config = AppConfig()
        self.assertEqual(config.get("app_name"), "PatternsDemo")
        self.assertFalse(config.get("debug"))

    def test_concurrent_construction_yields_exactly_one_instance(self) -> None:
        """The lock in __new__ closes the check-then-create race."""
        thread_count = 32
        barrier = threading.Barrier(thread_count)
        instances: list[AppConfig] = []
        record = threading.Lock()

        def construct() -> None:
            barrier.wait()  # maximise contention on __new__
            instance = AppConfig()
            with record:
                instances.append(instance)

        threads = [
            threading.Thread(target=construct) for _ in range(thread_count)
        ]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()

        self.assertEqual(len(instances), thread_count)
        self.assertEqual(len({id(instance) for instance in instances}), 1)


class TestPythonicAlternatives(unittest.TestCase):
    def test_module_level_instance_is_shared_via_the_import_system(self) -> None:
        """Modules are cached in sys.modules, so a module attribute is
        created once and shared by every importer."""
        reimported = importlib.import_module("singleton.alternatives")
        self.assertIs(module_config, reimported.module_config)

    def test_cached_factory_returns_the_same_object_every_call(self) -> None:
        """functools.cache memoises creation — a lazy singleton in one line."""
        self.assertIs(get_config(), get_config())

    def test_cached_factory_is_resettable_for_tests(self) -> None:
        """cache_clear() swaps in a fresh instance — the test-isolation
        escape hatch the classic Singleton must hand-build."""
        before = get_config()
        get_config.cache_clear()
        after = get_config()
        self.assertIsNot(before, after)


if __name__ == "__main__":
    unittest.main()
