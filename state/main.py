"""Demo client for the State pattern.

Run from the repository root:

    python -m state.main

One simulated day. The client fires the SAME events (use the safe, make
a phone call, press the alarm) at different hours — and gets different
behaviour, because a different State object is answering. Watch the
``[State]`` lines: every transition is requested by a state, never by
the client or the context.
"""

from .securitysystem.security_system import SecuritySystem


def main() -> None:
    system = SecuritySystem()
    print(f"System starts in {system.state} mode.")

    print()
    print("== Morning: business as usual ==")
    system.set_clock(9)
    system.use_safe()
    system.phone_call()

    print()
    print("== Afternoon: a drill ==")
    system.set_clock(14)
    system.press_alarm()

    print()
    print("== Evening: the office closes ==")
    system.set_clock(17)
    system.phone_call()

    print()
    print("== Late night: an intruder tries the safe ==")
    system.set_clock(23)
    system.use_safe()

    print()
    print("== Next morning: the office reopens ==")
    system.set_clock(9)
    system.use_safe()


if __name__ == "__main__":
    main()
