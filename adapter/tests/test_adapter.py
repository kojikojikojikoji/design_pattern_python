"""Tests for the Adapter pattern example.

Run from the repository root:

    python -m unittest discover -s adapter -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it. The legacy service
prints to stdout, so tests capture it to keep the run quiet.
"""

import contextlib
import io
import unittest

from adapter.adapters.class_adapter import LegacyEmailClassAdapter
from adapter.adapters.object_adapter import LegacyEmailAdapter
from adapter.legacy.legacy_email_service import LegacyEmailService
from adapter.target.notifier import NotificationError, Notifier


def quiet(callable_, *args, **kwargs):
    """Run ``callable_`` with stdout captured; return its result."""
    with contextlib.redirect_stdout(io.StringIO()):
        return callable_(*args, **kwargs)


class TestObjectAdapter(unittest.TestCase):
    def setUp(self) -> None:
        self.service = LegacyEmailService()
        self.adapter = LegacyEmailAdapter(self.service)

    def test_object_adapter_is_a_notifier(self) -> None:
        """The adapter satisfies the Target interface clients depend on."""
        self.assertIsInstance(self.adapter, Notifier)

    def test_object_adapter_does_not_expose_the_adaptee_api(self) -> None:
        """Composition hides the legacy API - clients can't bypass it."""
        self.assertFalse(hasattr(self.adapter, "send_mail"))

    def test_call_is_translated_to_the_legacy_signature(self) -> None:
        """notify(recipient, subject, body) becomes send_mail(to, msg, headers)."""
        quiet(self.adapter.notify, "alice@example.com", "Hi", "Hello Alice!")
        (to_address, message, headers), = self.service.outbox
        self.assertEqual(to_address, "alice@example.com")
        self.assertEqual(message, "Hello Alice!")
        self.assertEqual(headers, {"X-Subject": "Hi"})

    def test_failure_status_code_becomes_an_exception(self) -> None:
        """The adapter converts the legacy False return into an exception."""
        with self.assertRaises(NotificationError):
            quiet(self.adapter.notify, "not-an-address", "Hi", "Hello!")


class TestClassAdapter(unittest.TestCase):
    def test_class_adapter_is_both_target_and_adaptee(self) -> None:
        """Multiple inheritance: IS-A Notifier and IS-A LegacyEmailService."""
        adapter = LegacyEmailClassAdapter()
        self.assertIsInstance(adapter, Notifier)
        self.assertIsInstance(adapter, LegacyEmailService)

    def test_class_adapter_translates_the_call_too(self) -> None:
        """Both variants perform the exact same interface translation."""
        adapter = LegacyEmailClassAdapter()
        quiet(adapter.notify, "bob@example.com", "Hi", "Hello Bob!")
        (to_address, message, headers), = adapter.outbox
        self.assertEqual(
            (to_address, message, headers),
            ("bob@example.com", "Hello Bob!", {"X-Subject": "Hi"}),
        )


class TestPatternContracts(unittest.TestCase):
    def test_client_code_works_with_any_notifier(self) -> None:
        """Code written against the Target runs unchanged with either adapter."""

        def client(notifier: Notifier) -> None:  # knows only the Target
            notifier.notify("team@example.com", "Ping", "Still alive?")

        for notifier in (
            LegacyEmailAdapter(LegacyEmailService()),
            LegacyEmailClassAdapter(),
        ):
            with self.subTest(adapter=type(notifier).__name__):
                quiet(client, notifier)  # must not raise

    def test_the_adaptee_is_never_modified(self) -> None:
        """Adaptation adds a wrapper; the legacy class itself stays untouched."""
        self.assertFalse(hasattr(LegacyEmailService, "notify"))

    def test_target_interface_cannot_be_instantiated(self) -> None:
        """Notifier is a pure interface - only adapters/implementations exist."""
        with self.assertRaises(TypeError):
            Notifier()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
