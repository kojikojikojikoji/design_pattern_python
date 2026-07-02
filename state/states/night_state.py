"""NightState — how the security system behaves outside business hours.

Night is paranoid: the *same events* that were routine in daytime now
escalate. Opening the safe means calling the security company; the phone
goes to the answering machine. The state also knows its own exit
condition — at opening time, *this class* hands control to
:class:`DayState`.
"""

from typing import Optional

from .context import Context
from .day_state import CLOSING_HOUR, OPENING_HOUR, DayState
from .state import State


class NightState(State):
    """Night-time behaviour. A singleton — ``NightState() is NightState()``."""

    _instance: Optional["NightState"] = None

    def __new__(cls) -> "NightState":
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def on_clock(self, context: Context, hour: int) -> None:
        """Leave night mode when business hours begin."""
        if OPENING_HOUR <= hour < CLOSING_HOUR:
            context.change_state(DayState())

    def on_use_safe(self, context: Context) -> None:
        context.call_security("EMERGENCY: safe opened at night!")

    def on_alarm(self, context: Context) -> None:
        context.call_security("emergency bell pressed at night!")

    def on_phone(self, context: Context) -> None:
        context.record_log("night call recorded by the answering machine")

    def __str__(self) -> str:
        return "Night"
