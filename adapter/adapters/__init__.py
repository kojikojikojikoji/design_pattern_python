"""The Adapter side of the pattern — where the two worlds meet.

This sub-package contains the only code that knows about *both* the modern
:class:`~adapter.target.notifier.Notifier` interface and the legacy
:class:`~adapter.legacy.legacy_email_service.LegacyEmailService`. Two
variants are shown: an **object adapter** (composition, preferred) and a
**class adapter** (multiple inheritance).
"""
