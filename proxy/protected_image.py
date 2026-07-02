"""ProtectedImage — a protection proxy (the pattern's second flavour).

Where the virtual proxy controls *when* the real subject is created,
a **protection proxy** controls *who* may reach it. This one checks
the viewer's role before delegating and records every attempt —
granted or denied — in an access log.

Because it wraps the abstract :class:`~proxy.subject.Image`, it
composes with the other proxy: wrap an ``ImageProxy`` and a denied
viewer not only gets a :class:`PermissionError` — the expensive image
is never even loaded. Proxies stack, each adding one access policy.
"""

from .subject import Image


class ProtectedImage(Image):
    """Allows :meth:`render` only for authorised roles, and logs everything."""

    def __init__(
        self,
        inner: Image,
        viewer: str,
        role: str,
        allowed_roles: frozenset[str] = frozenset({"admin"}),
    ) -> None:
        self._inner = inner          # may be a RealImage or another proxy
        self._viewer = viewer
        self._role = role
        self._allowed_roles = allowed_roles
        self._access_log: list[str] = []

    @property
    def filename(self) -> str:
        # Reading the name is harmless — no permission check needed.
        return self._inner.filename

    @property
    def access_log(self) -> tuple[str, ...]:
        """Every render attempt so far, granted or denied (read-only view)."""
        return tuple(self._access_log)

    def render(self) -> str:
        """Delegate to the wrapped image — but only for authorised roles."""
        if self._role not in self._allowed_roles:
            self._access_log.append(f"DENIED  {self._viewer} ({self._role})")
            raise PermissionError(
                f"{self._viewer} ({self._role}) may not view {self.filename}"
            )
        self._access_log.append(f"granted {self._viewer} ({self._role})")
        return self._inner.render()
