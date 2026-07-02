"""supports — the concrete (application) side of the Chain of Responsibility example."""

from .limit_support import LimitSupport
from .no_support import NoSupport
from .odd_support import OddSupport
from .special_support import SpecialSupport

__all__ = ["LimitSupport", "NoSupport", "OddSupport", "SpecialSupport"]
