"""Tests for the Strategy example.

Run from the repository root:

    python -m unittest discover -s strategy -t .

Each test doubles as documentation: it states one guarantee the pattern
gives you and proves the code actually provides it.
"""

import unittest

from strategy.carriers.flat_rate import FlatRateShipping
from strategy.carriers.free_over_threshold import FreeShippingOverThreshold
from strategy.carriers.weight_based import WeightBasedShipping
from strategy.shipping.order import Order
from strategy.shipping.quoter import ShippingQuoter
from strategy.shipping.strategy import ShippingStrategy


class TestShippingQuoter(unittest.TestCase):
    def setUp(self) -> None:
        self.order = Order(weight_kg=2.0, subtotal_cents=4000)

    def test_context_delegates_to_its_strategy(self) -> None:
        """The context computes nothing itself — the strategy's answer IS
        the context's answer."""
        quoter = ShippingQuoter(FlatRateShipping(rate_cents=750))
        self.assertEqual(quoter.quote(self.order), 750)

    def test_strategy_can_be_swapped_at_runtime(self) -> None:
        """The same context object prices the same order differently after
        a one-line strategy swap — no context code changes."""
        quoter = ShippingQuoter(FlatRateShipping(rate_cents=599))
        self.assertEqual(quoter.quote(self.order), 599)

        quoter.strategy = WeightBasedShipping(base_cents=300, per_kg_cents=150)
        self.assertEqual(quoter.quote(self.order), 600)  # 300 + 150*2.0

    def test_all_strategies_are_interchangeable(self) -> None:
        """Every concrete strategy satisfies the same contract: an Order in,
        integer cents out."""
        strategies: list[ShippingStrategy] = [
            FlatRateShipping(),
            WeightBasedShipping(),
            FreeShippingOverThreshold(5000, fallback=FlatRateShipping()),
        ]
        for strategy in strategies:
            with self.subTest(strategy=type(strategy).__name__):
                cost = strategy.calculate(self.order)
                self.assertIsInstance(cost, int)
                self.assertGreaterEqual(cost, 0)


class TestConcreteStrategies(unittest.TestCase):
    def test_weight_based_charges_proportionally_to_weight(self) -> None:
        """A strategy encapsulates one complete formula, knobs included."""
        strategy = WeightBasedShipping(base_cents=200, per_kg_cents=100)
        light = Order(weight_kg=1.0, subtotal_cents=1000)
        heavy = Order(weight_kg=3.0, subtotal_cents=1000)
        self.assertEqual(strategy.calculate(light), 300)
        self.assertEqual(strategy.calculate(heavy), 500)

    def test_strategies_compose_like_ordinary_objects(self) -> None:
        """A strategy can wrap another strategy — the promotion applies its
        own rule and otherwise defers to the fallback's formula."""
        promo = FreeShippingOverThreshold(
            threshold_cents=5000, fallback=FlatRateShipping(rate_cents=599)
        )
        small = Order(weight_kg=1.0, subtotal_cents=4999)
        large = Order(weight_kg=1.0, subtotal_cents=5000)
        self.assertEqual(promo.calculate(small), 599)  # fallback's price
        self.assertEqual(promo.calculate(large), 0)  # promotion kicks in


class TestStrategyContract(unittest.TestCase):
    def test_abstract_strategy_cannot_be_instantiated(self) -> None:
        """ShippingStrategy is a pure interface."""
        with self.assertRaises(TypeError):
            ShippingStrategy()  # type: ignore[abstract]

    def test_incomplete_strategy_cannot_be_instantiated(self) -> None:
        """Forgetting to implement calculate() fails at construction time,
        not in the middle of a checkout."""

        class HalfStrategy(ShippingStrategy):
            pass  # calculate intentionally missing

        with self.assertRaises(TypeError):
            HalfStrategy()  # type: ignore[abstract]


if __name__ == "__main__":
    unittest.main()
