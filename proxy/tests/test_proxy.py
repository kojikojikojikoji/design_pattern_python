"""Tests for the Proxy example.

Run from the repository root:

    python -m unittest discover -s proxy -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it. Loading is proved
(not assumed) via the ``RealImage.loads`` counter; tests snapshot it in
``setUp`` so they stay independent of execution order.
"""

import io
import unittest
from contextlib import redirect_stdout

from proxy.image_proxy import ImageProxy
from proxy.protected_image import ProtectedImage
from proxy.real_image import RealImage
from proxy.subject import Image


class ProxyTestCase(unittest.TestCase):
    """Shared plumbing: count loads relative to the start of each test."""

    def setUp(self) -> None:
        self._loads_before = RealImage.loads

    def loads(self) -> int:
        """Real-image loads performed since this test started."""
        return RealImage.loads - self._loads_before

    def quiet_render(self, image: Image) -> str:
        """Render while swallowing the '(disk) loading' narration."""
        with redirect_stdout(io.StringIO()):
            return image.render()


class TestVirtualProxy(ProxyTestCase):
    def test_proxy_implements_the_same_subject_interface(self) -> None:
        """A proxy is substitutable: clients typed against Image accept it."""
        self.assertIsInstance(ImageProxy("a.png"), Image)
        with redirect_stdout(io.StringIO()):
            self.assertIsInstance(RealImage("b.png"), Image)

    def test_creating_a_proxy_loads_nothing(self) -> None:
        """Construction is free — that is the virtual proxy's promise."""
        proxy = ImageProxy("cat.png")
        self.assertEqual(self.loads(), 0)
        self.assertFalse(proxy.loaded)

    def test_cheap_questions_are_answered_without_loading(self) -> None:
        """The proxy handles what it can itself (the filename) and only
        delegates what truly needs the real subject."""
        proxy = ImageProxy("cat.png")
        self.assertEqual(proxy.filename, "cat.png")
        self.assertEqual(self.loads(), 0)

    def test_first_render_loads_exactly_once_then_reuses(self) -> None:
        """The expensive object is created lazily, and only ever once."""
        proxy = ImageProxy("cat.png")
        self.quiet_render(proxy)
        self.quiet_render(proxy)
        self.quiet_render(proxy)
        self.assertEqual(self.loads(), 1)

    def test_proxy_renders_exactly_what_the_real_subject_renders(self) -> None:
        """Transparency: going through the proxy changes when work
        happens, never what the client receives."""
        via_proxy = self.quiet_render(ImageProxy("cat.png"))
        with redirect_stdout(io.StringIO()):
            direct = RealImage("cat.png")
        self.assertEqual(via_proxy, direct.render())


class TestProtectionProxy(ProxyTestCase):
    def test_unauthorised_viewer_is_refused(self) -> None:
        """The protection proxy controls WHO reaches the real subject."""
        guarded = ProtectedImage(ImageProxy("salaries.png"), "mallory", "guest")
        with self.assertRaises(PermissionError):
            guarded.render()

    def test_denied_access_never_touches_the_expensive_resource(self) -> None:
        """Proxies compose: protection around a virtual proxy means a
        denied request costs nothing — the image is never even loaded."""
        guarded = ProtectedImage(ImageProxy("salaries.png"), "mallory", "guest")
        with self.assertRaises(PermissionError):
            guarded.render()
        self.assertEqual(self.loads(), 0)

    def test_every_attempt_is_recorded_in_the_access_log(self) -> None:
        """A proxy is the natural interception point for cross-cutting
        concerns like auditing — the real subject stays untouched."""
        inner = ImageProxy("salaries.png")
        denied = ProtectedImage(inner, "mallory", "guest")
        granted = ProtectedImage(inner, "alice", "admin")
        with self.assertRaises(PermissionError):
            denied.render()
        self.quiet_render(granted)
        self.assertEqual(denied.access_log, ("DENIED  mallory (guest)",))
        self.assertEqual(granted.access_log, ("granted alice (admin)",))


if __name__ == "__main__":
    unittest.main()
