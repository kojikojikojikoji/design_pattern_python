"""Tests for the State example.

Run from the repository root:

    python -m unittest discover -s state -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import contextlib
import io
import unittest

from state.securitysystem.security_system import SecuritySystem
from state.states.context import Context
from state.states.day_state import DayState
from state.states.night_state import NightState
from state.states.state import State


class RecordingContext(Context):
    """A stub context that records what a state asked it to do.

    Because states depend only on the abstract Context, each state can be
    specified in complete isolation from the real SecuritySystem.
    """

    def __init__(self) -> None:
        self.transitions: list[State] = []
        self.calls: list[str] = []
        self.logs: list[str] = []

    def change_state(self, state: State) -> None:
        self.transitions.append(state)

    def call_security(self, message: str) -> None:
        self.calls.append(message)

    def record_log(self, message: str) -> None:
        self.logs.append(message)


def quiet(callable_, *args):
    """Run ``callable_`` with the demo's console output suppressed."""
    with contextlib.redirect_stdout(io.StringIO()):
        return callable_(*args)


class TestStateSpecificBehaviour(unittest.TestCase):
    def test_the_same_event_behaves_differently_per_state(self) -> None:
        """Opening the safe is routine by day, an emergency by night —
        with zero conditionals anywhere."""
        day, night = RecordingContext(), RecordingContext()
        DayState().on_use_safe(day)
        NightState().on_use_safe(night)
        self.assertEqual(len(day.logs), 1)      # daytime: just logged
        self.assertEqual(day.calls, [])
        self.assertEqual(len(night.calls), 1)   # night: security called
        self.assertEqual(night.logs, [])

    def test_transitions_are_requested_by_the_states_themselves(self) -> None:
        """The clock handler of DayState — not the context — decides that
        17:00 means switching to NightState."""
        context = RecordingContext()
        DayState().on_clock(context, 17)
        self.assertEqual(context.transitions, [NightState()])

    def test_no_transition_while_still_inside_business_hours(self) -> None:
        """A state knows its own exit condition — and when it is NOT met."""
        context = RecordingContext()
        DayState().on_clock(context, 12)
        self.assertEqual(context.transitions, [])


class TestSecuritySystemLifecycle(unittest.TestCase):
    def setUp(self) -> None:
        self.system = SecuritySystem()

    def test_clock_moves_the_system_between_day_and_night(self) -> None:
        """A full day round-trip through the context."""
        self.assertIs(self.system.state, DayState())
        quiet(self.system.set_clock, 17)
        self.assertIs(self.system.state, NightState())
        quiet(self.system.set_clock, 9)
        self.assertIs(self.system.state, DayState())

    def test_the_context_contains_no_mode_conditionals(self) -> None:
        """The if-else ladder is really gone: the context's source never
        branches on day/night — it only delegates to self._state."""
        import inspect

        from state.securitysystem import security_system

        source = inspect.getsource(security_system)
        self.assertNotIn("== DayState", source)
        self.assertNotIn("isinstance(self._state", source)
        self.assertNotIn("is_day", source)

    def test_states_are_singletons(self) -> None:
        """One instance per mode: identity checks and allocation-free
        transitions come for free."""
        self.assertIs(DayState(), DayState())
        self.assertIs(NightState(), NightState())
        self.assertIsNot(DayState(), NightState())

    def test_abstract_state_cannot_be_instantiated(self) -> None:
        """State is a pure interface: a new mode must answer EVERY event."""
        with self.assertRaises(TypeError):
            State()  # type: ignore[abstract]

        class HalfMode(State):
            def on_clock(self, context: Context, hour: int) -> None:
                pass
            # on_use_safe / on_alarm / on_phone intentionally missing

        with self.assertRaises(TypeError):
            HalfMode()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
