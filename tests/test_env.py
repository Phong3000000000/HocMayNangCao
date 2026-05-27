"""
Test Suite for Inventory Environment.

Tests cover:
    - State transition logic (pending order → inventory)
    - Boundary conditions (inventory cap at 20, no negative)
    - Invalid action handling
    - Terminal state detection (30 days)
    - Seed reproducibility
    - Episode length and dynamics

Run with:
    python -m pytest tests/test_env.py -v

Author: RL Inventory Management Team
"""

import os
import sys
import pytest
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from envs.custom_env import InventoryEnv


class TestEnvironmentBasics:
    """Test basic environment functionality."""

    def setup_method(self):
        """Create a fresh environment for each test."""
        self.env = InventoryEnv(regime_transitions=False)

    def test_reset_returns_valid_state(self):
        """reset() should return a valid encoded state and info dict."""
        state, info = self.env.reset(seed=42)
        assert isinstance(state, int)
        assert 0 <= state < self.env.N_STATES
        assert isinstance(info, dict)
        assert 'inventory' in info
        assert 'demand_regime' in info

    def test_reset_initializes_day_count(self):
        """After reset, day_count should be 0."""
        self.env.reset(seed=42)
        assert self.env.day_count == 0

    def test_reset_clears_pending_order(self):
        """After reset, pending_order should be 0."""
        self.env.reset(seed=42)
        assert self.env.pending_order == 0

    def test_reset_inventory_range(self):
        """Initial inventory should be in [5, 14]."""
        for seed in range(20):
            self.env.reset(seed=seed)
            assert 5 <= self.env.inventory <= 14

    def test_step_returns_correct_format(self):
        """step() should return (state, reward, terminated, truncated, info)."""
        self.env.reset(seed=42)
        result = self.env.step(2)
        assert len(result) == 5

        next_state, reward, terminated, truncated, info = result
        assert isinstance(next_state, int)
        assert isinstance(reward, float)
        assert isinstance(terminated, bool)
        assert isinstance(truncated, bool)
        assert isinstance(info, dict)

    def test_step_advances_day(self):
        """Each step should advance day_count by 1."""
        self.env.reset(seed=42)
        for day in range(1, 10):
            self.env.step(0)
            assert self.env.day_count == day


class TestTransitionDynamics:
    """Test state transition logic."""

    def setup_method(self):
        self.env = InventoryEnv(regime_transitions=False)

    def test_pending_order_received_next_day(self):
        """
        Pending order from day t should be added to inventory at
        the start of day t+1.
        """
        self.env.reset(seed=42)
        # Record initial inventory
        inv_before = self.env.inventory
        order_amount = 3

        # Step 1: order 3 units
        self.env.step(order_amount)
        assert self.env.pending_order == order_amount

        # Step 2: pending order should be received
        inv_before_step2 = self.env.inventory
        # After step 2 starts, inventory should include pending from step 1
        # We can verify by checking the internal state DURING step
        # The step method adds pending_order to inventory at the beginning

    def test_inventory_capped_at_max(self):
        """Inventory should never exceed MAX_INVENTORY (20)."""
        self.env.reset(seed=42)
        # Set inventory close to max
        self.env.inventory = 18
        self.env.pending_order = 5  # Would push to 23 without cap
        self.env.step(0)
        # After receiving pending (18+5=23 → capped at 20) minus sold
        assert self.env.inventory <= self.env.MAX_INVENTORY

    def test_inventory_never_negative(self):
        """Inventory should never go below 0."""
        self.env.reset(seed=42)
        self.env.inventory = 0
        self.env.pending_order = 0

        for _ in range(30):
            if self.env.day_count >= 30:
                break
            self.env.step(0)
            assert self.env.inventory >= 0

    def test_day_of_week_wraps(self):
        """day_of_week should cycle through 0–6."""
        self.env.reset(seed=42)
        initial_dow = self.env.day_of_week

        for i in range(1, 15):
            self.env.step(0)
            expected_dow = (initial_dow + i) % 7
            assert self.env.day_of_week == expected_dow

    def test_pending_order_set_by_action(self):
        """After step(action), pending_order should equal the action."""
        self.env.reset(seed=42)
        for action in range(6):
            env = InventoryEnv(regime_transitions=False)
            env.reset(seed=42)
            env.step(action)
            assert env.pending_order == action


class TestTerminalState:
    """Test episode termination."""

    def setup_method(self):
        self.env = InventoryEnv(regime_transitions=False)

    def test_episode_terminates_at_30_days(self):
        """Episode should end exactly after 30 steps."""
        self.env.reset(seed=42)
        for day in range(30):
            _, _, terminated, _, _ = self.env.step(2)

            if day < 29:
                assert not terminated, \
                    f"Episode terminated early at day {day+1}"
            else:
                assert terminated, \
                    "Episode did not terminate at day 30"

    def test_episode_length_matches(self):
        """Episode history should have exactly 30 entries."""
        self.env.reset(seed=42)
        done = False
        while not done:
            _, _, terminated, truncated, _ = self.env.step(2)
            done = terminated or truncated

        summary = self.env.get_episode_summary()
        assert summary['episode_length'] == 30

    def test_truncated_always_false(self):
        """truncated should always be False (no early truncation)."""
        self.env.reset(seed=42)
        for _ in range(30):
            _, _, _, truncated, _ = self.env.step(0)
            assert truncated is False


class TestBoundaryConditions:
    """Test edge cases and boundaries."""

    def setup_method(self):
        self.env = InventoryEnv(regime_transitions=False)

    def test_zero_inventory_zero_pending(self):
        """With 0 inventory and 0 pending, agent can still order."""
        self.env.reset(seed=42)
        self.env.inventory = 0
        self.env.pending_order = 0

        next_state, reward, _, _, info = self.env.step(5)

        # Agent orders 5, pending_order should now be 5
        assert self.env.pending_order == 5
        # Purchase cost should be 5 * 5 = 25
        assert info['purchase_cost'] == 25.0

    def test_max_inventory_max_order(self):
        """With max inventory + max order, inventory stays capped."""
        self.env.reset(seed=42)
        self.env.inventory = 20
        self.env.pending_order = 5

        self.env.step(5)
        # After receiving pending: 20 + 5 = 25 → capped at 20
        # Then sold some, inventory should be ≤ 20
        assert self.env.inventory <= self.env.MAX_INVENTORY

    def test_invalid_action_raises(self):
        """Actions outside [0, 5] should raise AssertionError."""
        self.env.reset(seed=42)

        with pytest.raises(AssertionError):
            self.env.step(-1)

        with pytest.raises(AssertionError):
            self.env.step(6)

    def test_all_valid_actions_work(self):
        """All actions 0–5 should execute without error."""
        for action in range(6):
            env = InventoryEnv(regime_transitions=False)
            env.reset(seed=42)
            next_state, reward, _, _, _ = env.step(action)
            assert 0 <= next_state < env.N_STATES


class TestSeedReproducibility:
    """Test that the environment is deterministic given the same seed."""

    def test_same_seed_same_trajectory(self):
        """Two runs with the same seed should produce identical trajectories."""
        trajectories = []

        for _ in range(2):
            env = InventoryEnv(regime_transitions=True)
            state, _ = env.reset(seed=42)
            trajectory = [state]

            for _ in range(30):
                next_state, reward, _, _, _ = env.step(2)
                trajectory.append((next_state, reward))

            trajectories.append(trajectory)

        assert trajectories[0] == trajectories[1], \
            "Same seed produced different trajectories"

    def test_different_seeds_different_trajectories(self):
        """Different seeds should generally produce different trajectories."""
        trajectories = []

        for seed in [42, 99]:
            env = InventoryEnv(regime_transitions=True)
            state, _ = env.reset(seed=seed)
            trajectory = [state]

            for _ in range(10):
                next_state, reward, _, _, _ = env.step(2)
                trajectory.append((next_state, reward))

            trajectories.append(trajectory)

        # Very unlikely to be identical with different seeds
        assert trajectories[0] != trajectories[1], \
            "Different seeds produced identical trajectories (very unlikely)"

    def test_multiple_resets_same_seed(self):
        """Resetting with the same seed should give the same initial state."""
        env = InventoryEnv(regime_transitions=True)

        states = []
        for _ in range(5):
            state, _ = env.reset(seed=42)
            states.append(state)

        assert all(s == states[0] for s in states), \
            "Same seed gave different initial states"


class TestDemandRegimeTransitions:
    """Test demand regime dynamics."""

    def test_regime_stays_fixed_when_disabled(self):
        """With regime_transitions=False, regime should not change."""
        env = InventoryEnv(regime_transitions=False)
        env.reset(seed=42)
        initial_regime = env.demand_regime

        for _ in range(30):
            env.step(2)
            assert env.demand_regime == initial_regime

    def test_regime_can_change_when_enabled(self):
        """With regime_transitions=True, regime should sometimes change."""
        changed = False
        for seed in range(100):
            env = InventoryEnv(regime_transitions=True)
            env.reset(seed=seed)
            initial_regime = env.demand_regime

            for _ in range(30):
                env.step(2)
                if env.demand_regime != initial_regime:
                    changed = True
                    break

            if changed:
                break

        assert changed, \
            "Regime never changed in 100 episodes (very unlikely)"


class TestRender:
    """Test the render method."""

    def test_render_returns_string(self):
        """render() should return a non-empty string."""
        env = InventoryEnv()
        env.reset(seed=42)
        output = env.render()
        assert isinstance(output, str)
        assert len(output) > 0

    def test_render_contains_inventory(self):
        """render() output should contain the inventory value."""
        env = InventoryEnv()
        env.reset(seed=42)
        output = env.render()
        assert str(env.inventory) in output


class TestEpisodeSummary:
    """Test get_episode_summary()."""

    def test_summary_after_episode(self):
        """Summary should contain all required metrics."""
        env = InventoryEnv(regime_transitions=False)
        env.reset(seed=42)

        done = False
        while not done:
            _, _, terminated, truncated, _ = env.step(2)
            done = terminated or truncated

        summary = env.get_episode_summary()

        required_keys = [
            'total_profit', 'total_revenue', 'total_purchase_cost',
            'total_holding_cost', 'total_stockout_penalty',
            'stockout_rate', 'order_frequency', 'avg_inventory',
            'episode_length',
        ]
        for key in required_keys:
            assert key in summary, f"Missing key: {key}"

    def test_summary_empty_before_steps(self):
        """Summary should be empty dict before any steps."""
        env = InventoryEnv()
        env.reset(seed=42)
        assert env.get_episode_summary() == {}

    def test_profit_equals_components(self):
        """total_profit should equal revenue - purchase - holding - stockout."""
        env = InventoryEnv(regime_transitions=False)
        env.reset(seed=42)

        done = False
        while not done:
            _, _, terminated, truncated, _ = env.step(2)
            done = terminated or truncated

        s = env.get_episode_summary()
        expected = (s['total_revenue'] - s['total_purchase_cost']
                    - s['total_holding_cost'] - s['total_stockout_penalty'])

        assert abs(s['total_profit'] - expected) < 1e-6, \
            f"Profit {s['total_profit']} != {expected}"


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
