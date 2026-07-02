"""Tests for the Observer example.

Run from the repository root:

    python -m unittest discover -s observer -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from observer.framework.observer import Observer
from observer.framework.subject import Subject
from observer.stock.stock_price import StockPrice


class RecordingObserver(Observer):
    """A minimal observer that logs every price it is shown (pull style)."""

    def __init__(self, name: str = "rec") -> None:
        self.name = name
        self.seen: list[int] = []

    def update(self, subject: StockPrice) -> None:
        self.seen.append(subject.price)


class TestSubscriptionMechanics(unittest.TestCase):
    def setUp(self) -> None:
        self.feed = StockPrice("ACME", 100)

    def test_all_attached_observers_are_notified(self) -> None:
        """One state change fans out to every subscriber."""
        a, b = RecordingObserver("a"), RecordingObserver("b")
        self.feed.attach(a)
        self.feed.attach(b)
        self.feed.set_price(105)
        self.assertEqual(a.seen, [105])
        self.assertEqual(b.seen, [105])

    def test_detached_observers_stop_receiving_updates(self) -> None:
        """Subscriptions can end at runtime; no lingering callbacks."""
        obs = RecordingObserver()
        self.feed.attach(obs)
        self.feed.set_price(105)
        self.feed.detach(obs)
        self.feed.set_price(110)
        self.assertEqual(obs.seen, [105])

    def test_attach_is_idempotent(self) -> None:
        """Subscribing twice must not mean being notified twice."""
        obs = RecordingObserver()
        self.feed.attach(obs)
        self.feed.attach(obs)
        self.feed.set_price(105)
        self.assertEqual(obs.seen, [105])

    def test_notification_follows_subscription_order(self) -> None:
        """Order is deterministic: first subscribed, first notified."""
        calls: list[str] = []

        class Named(Observer):
            def __init__(self, name: str) -> None:
                self._name = name

            def update(self, subject: Subject) -> None:
                calls.append(self._name)

        for name in ("first", "second", "third"):
            self.feed.attach(Named(name))
        self.feed.set_price(105)
        self.assertEqual(calls, ["first", "second", "third"])


class TestDecoupling(unittest.TestCase):
    def test_subject_knows_observers_only_through_the_interface(self) -> None:
        """Any Observer subclass works — the feed never checks concrete types."""
        feed = StockPrice("ACME", 100)
        obs = RecordingObserver()  # defined in THIS test module, not in stock/
        feed.attach(obs)
        feed.set_price(123)
        self.assertEqual(obs.seen, [123])

    def test_pull_style_update_receives_the_subject_itself(self) -> None:
        """Observers pull state from the subject, so one observer can
        watch several subjects and tell them apart."""
        seen: list[str] = []

        class MultiWatcher(Observer):
            def update(self, subject: StockPrice) -> None:
                seen.append(f"{subject.symbol}@{subject.price}")

        watcher = MultiWatcher()
        acme, misc = StockPrice("ACME", 1), StockPrice("MISC", 2)
        acme.attach(watcher)
        misc.attach(watcher)
        acme.set_price(10)
        misc.set_price(20)
        self.assertEqual(seen, ["ACME@10", "MISC@20"])

    def test_observer_may_detach_itself_during_notification(self) -> None:
        """notify iterates a snapshot, so self-removal mid-broadcast is safe
        and later observers in the same round are still notified."""

        class OneShot(Observer):
            def __init__(self) -> None:
                self.calls = 0

            def update(self, subject: StockPrice) -> None:
                self.calls += 1
                subject.detach(self)

        feed = StockPrice("ACME", 100)
        one_shot, bystander = OneShot(), RecordingObserver()
        feed.attach(one_shot)
        feed.attach(bystander)   # subscribed AFTER the self-detaching one

        feed.set_price(105)      # must not raise, must reach the bystander
        feed.set_price(110)
        self.assertEqual(one_shot.calls, 1)
        self.assertEqual(bystander.seen, [105, 110])

    def test_abstract_observer_cannot_be_instantiated(self) -> None:
        """Observer is a pure interface — update() must be supplied."""
        with self.assertRaises(TypeError):
            Observer()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
