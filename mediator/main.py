"""Demo client for the Mediator pattern.

Run from the repository root:

    python -m mediator.main

Watch the ``[widget] enabled/disabled`` lines: every one of them is
printed because the *mediator* pushed new state to a widget — never
because one widget poked another.
"""

from .logindialog.login_dialog import LoginDialog


def main() -> None:
    print("== Opening the login dialog (guest mode by default) ==")
    dialog = LoginDialog()

    print()
    print("== A guest tries to type a username ==")
    dialog.username.set_text("alice")

    print()
    print("== Switching to Member login ==")
    dialog.mode.set_guest(False)

    print()
    print("== Typing the username ==")
    dialog.username.set_text("alice")

    print()
    print("== Typing the password ==")
    dialog.password.set_text("correct horse battery staple")

    print()
    print("== Pressing OK ==")
    dialog.ok.press()

    print()
    print("== Switching back to Guest login ==")
    dialog.mode.set_guest(True)
    dialog.password.set_text("let me in anyway")


if __name__ == "__main__":
    main()
