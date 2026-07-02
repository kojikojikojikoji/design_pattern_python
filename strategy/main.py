"""Demo client for the Strategy pattern.

Run from the repository root:

    python -m strategy.main

The point to notice: one ``ShippingQuoter`` (the Context) prices the same
orders three different ways, just by swapping the strategy object at
runtime. The quoter itself contains no pricing logic and never changes.
"""

from .carriers.flat_rate import FlatRateShipping
from .carriers.free_over_threshold import FreeShippingOverThreshold
from .carriers.weight_based import WeightBasedShipping
from .shipping.order import Order
from .shipping.quoter import ShippingQuoter
from .shipping.strategy import ShippingStrategy


def dollars(cents: int) -> str:
    """Format integer cents as a dollar string (display concern only)."""
    return f"${cents / 100:.2f}"


def main() -> None:
    orders = [
        Order(weight_kg=1.5, subtotal_cents=3000),  # light, small order
        Order(weight_kg=4.0, subtotal_cents=8000),  # heavy, big order
    ]

    # The only lines that mention concrete classes. Everything below
    # depends solely on the abstract ShippingStrategy interface.
    strategies: list[ShippingStrategy] = [
        FlatRateShipping(rate_cents=599),
        WeightBasedShipping(base_cents=300, per_kg_cents=150),
        FreeShippingOverThreshold(
            threshold_cents=5000, fallback=WeightBasedShipping(300, 150)
        ),
    ]

    quoter = ShippingQuoter(strategies[0])

    for order in orders:
        print(
            f"Order: {order.weight_kg} kg, "
            f"subtotal {dollars(order.subtotal_cents)}"
        )
        for strategy in strategies:
            quoter.strategy = strategy  # <-- the runtime swap
            cost = quoter.quote(order)
            name = type(strategy).__name__
            print(f"  {name:<26} {dollars(cost):>7}")
        print()

    # A context can also *use* the interchangeability, e.g. to find the
    # best deal for the customer — still without knowing any formula.
    best = min(strategies, key=lambda s: s.calculate(orders[1]))
    print(
        f"Cheapest option for the 4.0 kg order: "
        f"{type(best).__name__} ({dollars(best.calculate(orders[1]))})"
    )


if __name__ == "__main__":
    main()
