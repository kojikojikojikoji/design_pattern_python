"""DayState — how the security system behaves between 09:00 and 16:59.

Daytime is relaxed: using the safe is routine, phone calls are normal
business. The state also knows its own exit condition — when the clock
leaves business hours, *this class* hands control to :class:`NightState`.
"""

from typing import Optional

from .context import Context
from .state import State

OPENING_HOUR = 9   # business hours: 09:00 <= hour < 17:00
CLOSING_HOUR = 17


class DayState(State):
    """Daytime behaviour. A singleton — ``DayState() is DayState()``.

    States here carry no per-context data, so one shared instance per
    class suffices (Hiroshi Yuki's version does the same). Identity
    comparison (``state is DayState()``) then works everywhere, and
    transitions allocate nothing.
    """

    _instance: Optional["DayState"] = None

    def __new__(cls) -> "DayState":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def on_clock(self, context: Context, hour: int) -> None:
        """Leave daytime when the clock exits business hours."""
        if not OPENING_HOUR <= hour < CLOSING_HOUR:
            # Imported here (not at module top) because DayState and
            # NightState reference each other — a deliberate, documented
            # cycle: each state names its successor.
            from .night_state import NightState

            context.change_state(NightState())

    def on_use_safe(self, context: Context) -> None:
        context.record_log("safe opened (routine daytime use)")

    def on_alarm(self, context: Context) -> None:
        context.call_security("emergency bell pressed during the day!")

    def on_phone(self, context: Context) -> None:
        context.record_log("phone call handled by reception")

    def __str__(self) -> str:
        return "Day"
