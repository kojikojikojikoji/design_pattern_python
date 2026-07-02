"""subsystem — the complicated machinery hidden behind the Facade.

These classes are fully usable on their own (the Facade pattern never
forbids direct access); they are just fiddly to choreograph correctly.
"""

from .analyzer import SalesAnalyzer, SalesSummary
from .database import SalesDatabase
from .mailer import ReportMailer
from .renderer import ReportRenderer

__all__ = [
    "ReportMailer",
    "ReportRenderer",
    "SalesAnalyzer",
    "SalesDatabase",
    "SalesSummary",
]
