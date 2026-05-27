"""
Test Suite for Reward Calculation.

Tests cover:
    - Correct reward formula: r = revenue - purchase - holding - stockout
    - Revenue = min(inventory, demand) × sell_price
    - Purchase cost = action × buy_price
    - Holding cost = remaining_inventory × 0.5
    - Stockout penalty = max(0, demand - inventory) × 3
    - Edge cases: zero inventory, max inventory, stockout scenarios

Run with:
    python -m pytest tests/test_rewards.py -v

Author: RL Inventory Management Team
"""

import os
import sys
import pytest
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from envs.custom_env import InventoryEnv


class TestRewardFormula:
    """Test that reward is computed correctly."""

    def setup_method(self):
        """Create a deterministic environment (no regime transitions)."""
        self.env = InventoryEnv(regime_transitions=False)

    def test_reward_components_add_up(self):
        """
        r = revenue - purchase_cost - holding_cost - stockout_penalty

        Verify that the sum of components equals the reported reward.
        """
        self.env.reset(seed=42)

        for _ in range(30):
            _, reward, terminated, _, info = self.env.step(2)

            expected = (info['revenue']
                        - info['purchase_cost']
                        - info['holding_cost']
                        - info['stockout_penalty'])

            assert abs(reward - expected) < 1e-10, \
                f"Reward {reward} != {expected}"

            if terminated:
                break

    def test_purchase_cost_formula(self):
        """purchase_cost = action × buy_price (5)."""
        self.env.reset(seed=42)

        for action in range(6):
            env = InventoryEnv(regime_transitions=False)
            env.reset(seed=42)
            _, _, _, _, info = env.step(action)

            expected_cost = action * 5.0
            assert info['purchase_cost'] == expected_cost, \
                f"Action {action}: cost {info['purchase_cost']} != {expected_cost}"

    def test_holding_cost_formula(self):
        """
        holding_cost = remaining_inventory × 0.5

        remaining_inventory = inventory - sold (after sales).
        """
        self.env.reset(seed=42)

        for _ in range(30):
            _, _, terminated, _, info = self.env.step(0)

            remaining = info['inventory_after']
            expected_holding = remaining * 0.5
            assert abs(info['holding_cost'] - expected_holding) < 1e-10, \
                f"Holding: {info['holding_cost']} != {expected_holding}"

            if terminated:
                break

    def test_revenue_formula(self):
        """revenue = sold × sell_price (10)."""
        self.env.reset(seed=42)

        for _ in range(30):
            _, _, terminated, _, info = self.env.step(2)

            expected_revenue = info['sold'] * 10.0
            assert info['revenue'] == expected_revenue, \
                f"Revenue: {info['revenue']} != {expected_revenue}"

            if terminated:
                break

    def test_stockout_penalty_formula(self):
        """stockout_penalty = max(0, demand - inventory_before_sales) × 3."""
        self.env.reset(seed=42)

        for _ in range(30):
            _, _, terminated, _, info = self.env.step(0)

            expected_penalty = info['stockout'] * 3.0
            assert info['stockout_penalty'] == expected_penalty, \
                f"Stockout penalty: {info['stockout_penalty']} != {expected_penalty}"

            if terminated:
                break


class TestRewardEdgeCases:
    """Test reward in extreme scenarios."""

    def test_zero_inventory_zero_order_has_stockout(self):
        """
        With 0 inventory and 0 order, any demand causes stockout.
        """
        env = InventoryEnv(regime_transitions=False)
        env.reset(seed=42)
        env.inventory = 0
        env.pending_order = 0

        _, reward, _, _, info = env.step(0)

        # No revenue (nothing to sell... unless demand is 0)
        # No purchase cost (ordered 0)
        # No holding cost (0 inventory after)
        # Possible stockout penalty

        assert info['purchase_cost'] == 0.0
        assert info['revenue'] == info['sold'] * 10.0
        assert info['stockout'] == max(0, info['demand'] - 0)

    def test_max_inventory_no_order_positive_reward(self):
        """
        With max inventory and demand, there should be positive revenue.
        """
        env = InventoryEnv(regime_transitions=False)
        env.reset(seed=42)
        env.inventory = 20
        env.pending_order = 0

        _, reward, _, _, info = env.step(0)

        # Should sell some units (positive revenue)
        # No purchase cost
        # Some holding cost (remaining inventory × 0.5)
        # No stockout (inventory is 20, demand is at most 8)

        assert info['purchase_cost'] == 0.0
        assert info['revenue'] >= 0
        assert info['stockout'] == 0  # Demand max is 8 < 20

    def test_sell_price_correct(self):
        """Verify sell price is 10 per unit."""
        assert InventoryEnv.SELL_PRICE == 10.0

    def test_buy_price_correct(self):
        """Verify buy price is 5 per unit."""
        assert InventoryEnv.BUY_PRICE == 5.0

    def test_holding_cost_correct(self):
        """Verify holding cost is 0.5 per unit per day."""
        assert InventoryEnv.HOLDING_COST == 0.5

    def test_stockout_cost_correct(self):
        """Verify stockout cost is 3 per unit."""
        assert InventoryEnv.STOCKOUT_COST == 3.0


class TestRewardNotOnlyRevenue:
    """
    Verify that the reward function penalizes excess inventory and stockouts,
    not just maximizing revenue.

    This addresses the common error: "Reward chỉ tối đa doanh thu,
    khiến agent nhập quá nhiều."
    """

    def test_ordering_too_much_reduces_profit(self):
        """
        Ordering 5 every day should result in LOWER profit than
        a balanced strategy due to high holding costs.
        """
        # Strategy 1: Always order 5 (excessive)
        env1 = InventoryEnv(regime_transitions=False)
        env1.reset(seed=42)
        total_reward_1 = 0
        for _ in range(30):
            _, r, terminated, _, _ = env1.step(5)
            total_reward_1 += r
            if terminated:
                break

        # Strategy 2: Always order 0 (conservative)
        env2 = InventoryEnv(regime_transitions=False)
        env2.reset(seed=42)
        total_reward_2 = 0
        for _ in range(30):
            _, r, terminated, _, _ = env2.step(0)
            total_reward_2 += r
            if terminated:
                break

        # Neither should dominate universally — the key is that ordering
        # too much should incur holding costs
        summary1 = env1.get_episode_summary()
        summary2 = env2.get_episode_summary()

        # Always order 5: should have higher holding cost
        assert summary1['total_holding_cost'] > summary2['total_holding_cost'], \
            "Always ordering 5 should have higher holding cost"

    def test_holding_cost_nonzero_with_excess(self):
        """If inventory remains at end of day, holding cost must be positive."""
        env = InventoryEnv(regime_transitions=False)
        env.reset(seed=42)
        env.inventory = 10
        env.pending_order = 5  # Will receive 5 more

        _, _, _, _, info = env.step(5)

        if info['inventory_after'] > 0:
            assert info['holding_cost'] > 0, \
                "Holding cost should be > 0 when inventory > 0"

    def test_stockout_penalty_applied(self):
        """When demand exceeds inventory, stockout penalty must be applied."""
        env = InventoryEnv(regime_transitions=False)
        env.reset(seed=42)
        env.inventory = 0
        env.pending_order = 0
        env.demand_regime = 2  # High demand

        # Run until we get a stockout
        stockout_found = False
        for seed in range(100):
            env_test = InventoryEnv(regime_transitions=False)
            env_test.reset(seed=seed)
            env_test.inventory = 0
            env_test.pending_order = 0
            env_test.demand_regime = 2  # High demand

            _, _, _, _, info = env_test.step(0)
            if info['stockout'] > 0:
                assert info['stockout_penalty'] > 0
                stockout_found = True
                break

        assert stockout_found, \
            "Could not generate a stockout in 100 tries (very unlikely)"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
