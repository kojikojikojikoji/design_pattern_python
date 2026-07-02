"""SecuritySystem — the concrete Context.

The context is the object clients talk to. It holds a reference to *the
current* State object and forwards every event to it, adding no opinion
of its own. Look closely: this file contains **no** ``if day ... else
night ...`` anywhere — mode-dependent behaviour is entirely the states'
business, and transitions happen because a state asks for them.
"""

from ..states.context import Context
from ..states.day_state import DayState
from ..states.state import State


class SecuritySystem(Context):
    """A building's alarm panel, delegating every event to its State."""

    def __init__(self) -> None:
        # The initial mode is the only state decision the context makes.
        self._state: State = DayState()

    @property
    def state(self) -> State:
        """The current mode (handy for demos and tests)."""
        return self._state

    # ------------------------------------------------------------------
    # Events from the outside world — every one is a blind delegation.
    # ------------------------------------------------------------------

    def set_clock(self, hour: int) -> None:
        """Advance the wall clock; the state decides if the mode flips."""
        print(f"[Clock] {hour:02d}:00")
        self._state.on_clock(self, hour)

    def use_safe(self) -> None:
        """Someone opens the safe."""
        self._state.on_use_safe(self)

    def press_alarm(self) -> None:
        """Someone presses the emergency bell."""
        self._state.on_alarm(self)

    def phone_call(self) -> None:
        """The office phone is used."""
        self._state.on_phone(self)

    # ------------------------------------------------------------------
    # Context interface — services the states call back into.
    # ------------------------------------------------------------------

    def change_state(self, state: State) -> None:
        """Swap behaviour by swapping the state object (called by states)."""
        print(f"[State] {self._state} -> {state}")
        self._state = state

    def call_security(self, message: str) -> None:
        print(f"[CALL!] security company: {message}")

    def record_log(self, message: str) -> None:
        print(f"[ log ] {message}")
