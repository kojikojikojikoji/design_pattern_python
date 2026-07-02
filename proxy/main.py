"""Demo client for the Proxy pattern.

Run from the repository root:

    python -m proxy.main

Watch the "(disk) loading ..." lines: with the real image they appear
immediately at construction; with the virtual proxy they appear only at
the first render — and with the protection proxy denying access, never.
"""

from .image_proxy import ImageProxy
from .protected_image import ProtectedImage
from .real_image import RealImage
from .subject import Image


def main() -> None:
    print("--- 1. RealImage: construction alone pays the loading cost ---")
    real: Image = RealImage("holiday.png")
    print(real.render())
    print()

    print("--- 2. ImageProxy: construction is free ---")
    gallery: list[Image] = [
        ImageProxy("cat.png"),
        ImageProxy("dog.png"),
        ImageProxy("whale.png"),
    ]
    print("Created a gallery of 3 proxies - no loading happened yet.")
    print(f"Filenames (still no loading): {[image.filename for image in gallery]}")
    print()

    print("First render of cat.png - NOW it loads:")
    print(gallery[0].render())
    print("Second render of cat.png - already loaded, no disk line:")
    print(gallery[0].render())
    print("dog.png and whale.png were never rendered, so never loaded.")
    print()

    print("--- 3. ProtectedImage: a protection proxy on top of a virtual one ---")
    secret = ImageProxy("salaries.png")
    print("mallory is denied BEFORE any loading; alice's render loads it:")
    for viewer, role in (("mallory", "guest"), ("alice", "admin")):
        guarded = ProtectedImage(secret, viewer, role)
        try:
            print(guarded.render())
        except PermissionError as error:
            print(f"PermissionError: {error}")
        print(f"  access log: {list(guarded.access_log)}")


if __name__ == "__main__":
    main()
