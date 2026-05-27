"""
Inventory Management Environment for Reinforcement Learning.

MDP Design:
===========
State:  s = (inventory, demand_regime, day_of_week, pending_order)
    - inventory       ∈ {0, ..., 20}       (21 values)
    - demand_regime   ∈ {0=low, 1=medium, 2=high}  (3 values)
    - day_of_week     ∈ {0=Mon, ..., 6=Sun}  (7 values)
    - pending_order   ∈ {0, ..., 5}        (6 values)
    → Total states: 21 × 3 × 7 × 6 = 2,646

Action: order ∈ {0, 1, 2, 3, 4, 5}  (6 actions)

Dynamics (each day):
    1. Start of day: pending_order → inventory (capped at 20)
    2. Agent places new order → becomes next pending_order
    3. Demand generated from discrete distribution by demand_regime
    4. Sales = min(inventory, demand)
    5. Stockout = max(0, demand - inventory)
    6. inventory -= sales

Reward:
    r = revenue - purchase_cost - holding_cost - stockout_penalty
    revenue          = sold × 10  (sell price)
    purchase_cost    = order × 5  (buy price)
    holding_cost     = remaining_inventory × 0.5
    stockout_penalty = unmet_demand × 3

Episode: 30 days (1 month). Terminal when day_count >= 30.

Author: RL Inventory Management Team
"""

import numpy as np
from envs.base_env import BaseEnv


# ═══════════════════════════════════════════════════════════════
# DEMAND CONFIGURATION
# ═══════════════════════════════════════════════════════════════

# Human-readable regime labels
DEMAND_REGIMES = {0: 'low', 1: 'medium', 2: 'high'}
DEMAND_REGIME_IDS = {'low': 0, 'medium': 1, 'high': 2}

# Discrete demand distributions for each regime
# Each regime maps demand values to their probabilities
DEMAND_DISTRIBUTIONS = {
    0: {  # Low demand: centered around 1–2 units/day
        'values': np.array([0, 1, 2, 3, 4]),
        'probs':  np.array([0.10, 0.30, 0.30, 0.20, 0.10])
    },
    1: {  # Medium demand: centered around 3–4 units/day
        'values': np.array([0, 1, 2, 3, 4, 5, 6]),
        'probs':  np.array([0.05, 0.08, 0.15, 0.25, 0.22, 0.15, 0.10])
    },
    2: {  # High demand: centered around 5–6 units/day
        'values': np.array([0, 1, 2, 3, 4, 5, 6, 7, 8]),
        'probs':  np.array([0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.22, 0.18, 0.10])
    }
}

# Demand regime transition matrix (Markov chain)
# REGIME_TRANSITION_PROBS[current][next] = probability
REGIME_TRANSITION_PROBS = {
    0: np.array([0.90, 0.08, 0.02]),  # Low   → mostly stays low
    1: np.array([0.05, 0.85, 0.10]),  # Medium → mostly stays medium
    2: np.array([0.02, 0.08, 0.90])   # High  → mostly stays high
}

# Day names for display
DAY_NAMES = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']


class InventoryEnv(BaseEnv):
    """
    Inventory Management RL Environment.

    The agent manages a warehouse and decides how many units to order each day
    to maximize long-term profit while minimizing stockouts and excess inventory.

    Attributes:
        MAX_INVENTORY (int): Maximum stock capacity (20 units).
        EPISODE_LENGTH (int): Number of days per episode (30).
        SELL_PRICE (float): Revenue per unit sold (10).
        BUY_PRICE (float): Cost per unit ordered (5).
        HOLDING_COST (float): Cost per unit remaining at end of day (0.5).
        STOCKOUT_COST (float): Penalty per unit of unmet demand (3).
    """

    # ─── Environment constants ─────────────────────────────────
    MAX_INVENTORY = 20
    NUM_REGIMES = 3
    NUM_DAYS = 7
    MAX_ORDER = 5
    EPISODE_LENGTH = 30  # 30 days per episode

    # ─── Cost parameters ───────────────────────────────────────
    SELL_PRICE = 10.0
    BUY_PRICE = 5.0
    HOLDING_COST = 0.5   # per unit per day
    STOCKOUT_COST = 3.0  # per unit of unmet demand

    # ─── State space dimensions ────────────────────────────────
    N_INVENTORY = MAX_INVENTORY + 1  # 0..20 → 21 values
    N_REGIME = NUM_REGIMES           # 3 values
    N_DOW = NUM_DAYS                 # 7 values
    N_PENDING = MAX_ORDER + 1        # 0..5  → 6 values

    # ─── Derived constants ─────────────────────────────────────
    N_STATES = N_INVENTORY * N_REGIME * N_DOW * N_PENDING   # 2646
    N_ACTIONS = MAX_ORDER + 1                                # 6

    def __init__(self, regime_transitions=True, weekend_surge=False):
        """
        Initialize the Inventory Environment.

        Args:
            regime_transitions (bool): If True, demand regime transitions
                stochastically each day according to a Markov chain.
                If False, regime stays fixed for the entire episode.
            weekend_surge (bool): If True, demand regime is shifted up by 1
                on weekends (Sat=5, Sun=6). This creates an unseen demand
                pattern for generalization testing.
        """
        self.regime_transitions = regime_transitions
        self.weekend_surge = weekend_surge

        # Current state variables
        self.inventory = 0
        self.demand_regime = 0
        self.day_of_week = 0
        self.pending_order = 0
        self.day_count = 0

        # Random number generator (seeded for reproducibility)
        self.rng = np.random.RandomState()

        # Episode history for analysis
        self.episode_history = []

    # ═══════════════════════════════════════════════════════════
    # CORE API
    # ═══════════════════════════════════════════════════════════

    def reset(self, seed=None):
        """
        Reset the environment to a random initial state.

        Args:
            seed (int, optional): Random seed for reproducibility.

        Returns:
            state (int): Encoded initial state index.
            info (dict): Dictionary with initial state details.
        """
        # Reseed the RNG if a seed is provided
        if seed is not None:
            self.rng = np.random.RandomState(seed)

        # Random initial state
        self.inventory = self.rng.randint(5, 15)       # Start with some stock
        self.demand_regime = self.rng.randint(0, self.NUM_REGIMES)
        self.day_of_week = self.rng.randint(0, self.NUM_DAYS)
        self.pending_order = 0   # No pending orders at start
        self.day_count = 0

        # Clear episode history
        self.episode_history = []

        state = self._get_state_tuple()
        info = self._get_info()
        return self.state_encoder(state), info

    def step(self, action):
        """
        Execute one day in the inventory simulation.

        Daily dynamics:
            1. Receive pending order → inventory (capped at MAX_INVENTORY)
            2. Agent places new order → becomes tomorrow's pending_order
            3. Generate demand from current regime's distribution
            4. Process sales: sold = min(inventory, demand)
            5. Compute reward = revenue − purchase − holding − stockout
            6. Advance calendar (day_of_week, day_count)
            7. Optionally transition demand regime

        Args:
            action (int): Units to order, must be in {0, 1, 2, 3, 4, 5}.

        Returns:
            next_state (int): Encoded next state.
            reward (float): Immediate reward.
            terminated (bool): True if episode ended (day_count >= 30).
            truncated (bool): Always False (no early truncation).
            info (dict): Detailed step information.
        """
        # Validate action
        assert 0 <= action <= self.MAX_ORDER, \
            f"Invalid action {action}. Must be in {{0, ..., {self.MAX_ORDER}}}."

        # ── Step 1: Receive yesterday's pending order ──────────
        self.inventory = min(
            self.inventory + self.pending_order,
            self.MAX_INVENTORY
        )

        # ── Step 2: Agent places new order ─────────────────────
        purchase_cost = action * self.BUY_PRICE
        self.pending_order = action  # Arrives tomorrow

        # ── Step 3: Generate today's demand ────────────────────
        effective_regime = self.demand_regime

        # Weekend surge: shift demand regime up on Sat/Sun
        if self.weekend_surge and self.day_of_week in (5, 6):
            effective_regime = min(effective_regime + 1, 2)

        dist = DEMAND_DISTRIBUTIONS[effective_regime]
        demand = int(self.rng.choice(dist['values'], p=dist['probs']))

        # ── Step 4: Process sales ──────────────────────────────
        sold = min(self.inventory, demand)
        stockout = max(0, demand - self.inventory)
        self.inventory -= sold  # Remove sold units from stock

        # ── Step 5: Compute reward ─────────────────────────────
        revenue = sold * self.SELL_PRICE
        holding_cost = self.inventory * self.HOLDING_COST
        stockout_penalty = stockout * self.STOCKOUT_COST
        reward = revenue - purchase_cost - holding_cost - stockout_penalty

        # ── Step 6: Advance calendar ───────────────────────────
        self.day_of_week = (self.day_of_week + 1) % self.NUM_DAYS
        self.day_count += 1

        # ── Step 7: Demand regime transition ───────────────────
        if self.regime_transitions:
            trans_probs = REGIME_TRANSITION_PROBS[self.demand_regime]
            self.demand_regime = int(
                self.rng.choice([0, 1, 2], p=trans_probs)
            )

        # ── Step 8: Check episode termination ──────────────────
        terminated = (self.day_count >= self.EPISODE_LENGTH)
        truncated = False

        # ── Record step details ────────────────────────────────
        step_info = {
            'day': self.day_count,
            'action': action,
            'demand': demand,
            'sold': sold,
            'stockout': stockout,
            'revenue': revenue,
            'purchase_cost': purchase_cost,
            'holding_cost': holding_cost,
            'stockout_penalty': stockout_penalty,
            'reward': reward,
            'inventory_after': self.inventory,
            'demand_regime': self.demand_regime,
            'effective_regime': effective_regime,
        }
        self.episode_history.append(step_info)

        next_state = self._get_state_tuple()
        info = {**self._get_info(), **step_info}

        return self.state_encoder(next_state), reward, terminated, truncated, info

    def render(self):
        """
        Render the current state as a formatted ASCII box.

        Returns:
            str: Formatted state display.
        """
        regime_name = DEMAND_REGIMES[self.demand_regime]
        day_name = DAY_NAMES[self.day_of_week]

        # Build inventory bar visualization
        bar_filled = '█' * self.inventory
        bar_empty = '░' * (self.MAX_INVENTORY - self.inventory)
        bar = bar_filled + bar_empty

        output = (
            f"╔══════════════════════════════════════╗\n"
            f"║   INVENTORY MANAGEMENT — Day {self.day_count:3d}/30  ║\n"
            f"╠══════════════════════════════════════╣\n"
            f"║  Inventory:     {self.inventory:3d}/{self.MAX_INVENTORY}  [{bar}] ║\n"
            f"║  Demand Regime: {regime_name:>6s}              ║\n"
            f"║  Day of Week:   {day_name:>3s}                 ║\n"
            f"║  Pending Order: {self.pending_order:3d} units            ║\n"
            f"╚══════════════════════════════════════╝"
        )
        print(output)
        return output

    # ═══════════════════════════════════════════════════════════
    # STATE ENCODING / DECODING
    # ═══════════════════════════════════════════════════════════

    def state_encoder(self, state):
        """
        Encode state tuple → single integer index.

        Formula:
            index = inventory × (N_REGIME × N_DOW × N_PENDING)
                  + regime   × (N_DOW × N_PENDING)
                  + dow      × N_PENDING
                  + pending

        Encodes to range [0, 2645].

        Args:
            state (tuple): (inventory, demand_regime, day_of_week, pending_order)

        Returns:
            int: Unique state index in [0, N_STATES-1].
        """
        inventory, demand_regime, day_of_week, pending_order = state
        encoded = (inventory * (self.N_REGIME * self.N_DOW * self.N_PENDING)
                   + demand_regime * (self.N_DOW * self.N_PENDING)
                   + day_of_week * self.N_PENDING
                   + pending_order)
        return int(encoded)

    def state_decoder(self, encoded_state):
        """
        Decode integer index → state tuple.

        Inverse of state_encoder().

        Args:
            encoded_state (int): State index in [0, N_STATES-1].

        Returns:
            tuple: (inventory, demand_regime, day_of_week, pending_order)
        """
        pending_order = encoded_state % self.N_PENDING
        remainder = encoded_state // self.N_PENDING

        day_of_week = remainder % self.N_DOW
        remainder = remainder // self.N_DOW

        demand_regime = remainder % self.N_REGIME
        inventory = remainder // self.N_REGIME

        return (int(inventory), int(demand_regime),
                int(day_of_week), int(pending_order))

    # ═══════════════════════════════════════════════════════════
    # HELPER METHODS
    # ═══════════════════════════════════════════════════════════

    def _get_state_tuple(self):
        """Get the current state as a tuple."""
        return (self.inventory, self.demand_regime,
                self.day_of_week, self.pending_order)

    def _get_info(self):
        """Get current environment info dictionary."""
        return {
            'inventory': self.inventory,
            'demand_regime': self.demand_regime,
            'demand_regime_name': DEMAND_REGIMES[self.demand_regime],
            'day_of_week': self.day_of_week,
            'day_of_week_name': DAY_NAMES[self.day_of_week],
            'pending_order': self.pending_order,
            'day_count': self.day_count,
            'state_encoded': self.state_encoder(self._get_state_tuple()),
        }

    def get_episode_summary(self):
        """
        Compute summary statistics for the completed episode.

        Returns:
            dict: Episode-level metrics including total profit, stockout rate,
                holding cost, order frequency, and average inventory.
        """
        if not self.episode_history:
            return {}

        # Aggregate step-level metrics
        total_revenue = sum(s['revenue'] for s in self.episode_history)
        total_purchase = sum(s['purchase_cost'] for s in self.episode_history)
        total_holding = sum(s['holding_cost'] for s in self.episode_history)
        total_stockout_pen = sum(s['stockout_penalty'] for s in self.episode_history)
        total_reward = sum(s['reward'] for s in self.episode_history)
        total_demand = sum(s['demand'] for s in self.episode_history)
        total_sold = sum(s['sold'] for s in self.episode_history)
        total_stockout = sum(s['stockout'] for s in self.episode_history)
        total_ordered = sum(s['action'] for s in self.episode_history)

        n_days = len(self.episode_history)
        days_with_stockout = sum(1 for s in self.episode_history if s['stockout'] > 0)
        days_with_order = sum(1 for s in self.episode_history if s['action'] > 0)
        avg_inventory = float(np.mean(
            [s['inventory_after'] for s in self.episode_history]
        ))

        return {
            'total_profit': total_reward,
            'total_revenue': total_revenue,
            'total_purchase_cost': total_purchase,
            'total_holding_cost': total_holding,
            'total_stockout_penalty': total_stockout_pen,
            'total_demand': total_demand,
            'total_sold': total_sold,
            'total_stockout_units': total_stockout,
            'total_ordered': total_ordered,
            'stockout_rate': days_with_stockout / n_days,
            'order_frequency': days_with_order / n_days,
            'avg_inventory': avg_inventory,
            'episode_length': n_days,
        }
