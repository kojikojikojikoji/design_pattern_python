"""Demo client for the Adapter pattern.

Run from the repository root:

    python -m adapter.main

The point to notice: ``announce_maintenance`` is written purely against
the abstract ``Notifier`` interface. It has no idea that, behind the
adapter, a legacy service with a completely different API does the work.
"""

from .adapters.class_adapter import LegacyEmailClassAdapter
from .adapters.object_adapter import LegacyEmailAdapter
from .legacy.legacy_email_service import LegacyEmailService
from .target.notifier import NotificationError, Notifier


def announce_maintenance(notifier: Notifier) -> None:
    """Client code: depends only on the Target interface."""
    notifier.notify(
        recipient="dev-team@example.com",
        subject="Scheduled maintenance",
        body="The API will be offline 02:00-03:00 UTC.",
    )


def main() -> None:
    print("=== Object adapter (composition, preferred) ===")
    # The adaptee is created independently and *injected* into the adapter.
    legacy_service = LegacyEmailService()
    announce_maintenance(LegacyEmailAdapter(legacy_service))

    print()
    print("=== Class adapter (multiple inheritance) ===")
    # The adapter IS the adaptee here - no separate service object exists.
    announce_maintenance(LegacyEmailClassAdapter())

    print()
    print("=== Failure translation (status code -> exception) ===")
    faulty: Notifier = LegacyEmailAdapter(LegacyEmailService())
    try:
        faulty.notify("not-an-address", "Hello", "This cannot be delivered.")
    except NotificationError as error:
        print(f"NotificationError caught: {error}")


if __name__ == "__main__":
    main()
