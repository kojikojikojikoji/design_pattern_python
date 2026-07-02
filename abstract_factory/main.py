"""Demo client for the Abstract Factory pattern.

Run from the repository root:

    python -m abstract_factory.main

The point to notice: ``build_login_form`` is written once, against the
abstract ``UIFactory`` / ``Button`` / ``Checkbox`` types. Rendering the
same form in a completely different theme requires zero changes to it —
only a different factory is passed in.
"""

from .dark_theme.factory import DarkThemeFactory
from .light_theme.factory import LightThemeFactory
from .ui.factory import UIFactory


def build_login_form(factory: UIFactory) -> str:
    """Assemble a small login form using whatever family ``factory`` makes.

    This function is the pattern's client. It never mentions a concrete
    widget class, so it works — unchanged — for every theme, including
    themes written years after it.
    """
    remember_me = factory.create_checkbox("Remember me")
    sign_in = factory.create_button("Sign in")
    remember_me.toggle()  # the user ticks the box

    lines = [
        f"--- {factory.theme_name} login form ---",
        remember_me.render(),
        sign_in.render(),
    ]
    return "\n".join(lines)


def main() -> None:
    # The only lines that mention concrete classes: choosing the factories.
    factories: list[UIFactory] = [LightThemeFactory(), DarkThemeFactory()]

    for factory in factories:
        print(build_login_form(factory))
        print()

    print("Same client code, two coherent widget families. No theme mixing.")


if __name__ == "__main__":
    main()
