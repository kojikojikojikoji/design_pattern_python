# `tests/` — the pattern's guarantees, as executable code

These tests are deliberately written as an **executable specification**: each test name states one guarantee the Observer pattern gives you, and the test body proves the code delivers it. If you have read the tutorial in [`../README.md`](../README.md), reading these tests is the fastest comprehension check.

## Run

From the **repository root** (standard library only — no pytest required):

```bash
python -m unittest discover -s observer -t .
```

## What each test teaches

| Test | Guarantee it demonstrates |
| --- | --- |
| `test_all_attached_observers_are_notified` | One state change fans out to every subscriber — the one-to-many core of the pattern. |
| `test_detached_observers_stop_receiving_updates` | Subscriptions are dynamic; unsubscribing really severs the link. |
| `test_attach_is_idempotent` | Double-subscribing does not cause double notifications — a common production bug, prevented in `attach`. |
| `test_notification_follows_subscription_order` | Ordering is deterministic (subscription order), so demos and logs are reproducible. |
| `test_subject_knows_observers_only_through_the_interface` | An observer class the subject has never heard of works immediately — the subject is closed for modification, open for extension. |
| `test_pull_style_update_receives_the_subject_itself` | Pull style lets a single observer watch multiple subjects and tell them apart. |
| `test_observer_may_detach_itself_during_notification` | `notify_observers` iterates a snapshot: self-removal mid-broadcast neither crashes nor starves later subscribers. |
| `test_abstract_observer_cannot_be_instantiated` | `Observer` is a pure interface; forgetting `update` fails at construction time. |

## A note for learners

`RecordingObserver` at the top of the test file is the essential Observer-testing trick: a subscriber that just logs what it saw. Because subjects depend only on the abstract interface, such probes can be attached to *any* subject — you will write one every time you test event-driven code.
