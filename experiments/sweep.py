"""
Hyperparameter Sweep for RL Inventory Management.

Performs grid search over key hyperparameters (α, γ, ε_decay) for Q-Learning
to find optimal settings.

Usage:
    python experiments/sweep.py

Output:
    results/sweep_results.json — Grid search results sorted by profit

Author: RL Inventory Management Team
"""

import os
import sys
import numpy as np
import itertools
import json
import yaml

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from envs.custom_env import InventoryEnv
from agents.q_learning import QLearningAgent
from experiments.evaluate import evaluate_agent


def load_config(config_path=None):
    """Load sweep configuration."""
    if config_path is None:
        config_path = os.path.join(os.path.dirname(__file__), 'configs.yaml')
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def sweep_hyperparameters(config=None):
    """
    Grid search over hyperparameters for Q-Learning.

    Tests all combinations of α × γ × ε_decay and ranks by
    mean evaluation profit.

    Returns:
        list[dict]: Results sorted by profit (descending).
    """
    if config is None:
        config = load_config()

    sweep_cfg = config.get('sweep', {})
    alphas = sweep_cfg.get('alphas', [0.05, 0.1, 0.2])
    gammas = sweep_cfg.get('gammas', [0.9, 0.95, 0.99])
    epsilon_decays = sweep_cfg.get('epsilon_decays',
                                   [0.999, 0.9995, 0.9999])
    n_train = sweep_cfg.get('n_train_episodes', 3000)
    n_eval = sweep_cfg.get('n_eval_episodes', 50)

    env = InventoryEnv(regime_transitions=True)
    n_states = env.N_STATES
    n_actions = env.N_ACTIONS

    total = len(alphas) * len(gammas) * len(epsilon_decays)
    results = []
    count = 0

    print(f"\n{'='*60}")
    print(f"  HYPERPARAMETER SWEEP")
    print(f"  {total} configurations x {n_train} episodes each")
    print(f"{'='*60}")

    for alpha, gamma, eps_decay in itertools.product(
            alphas, gammas, epsilon_decays):

        count += 1
        print(f"\n  [{count:2d}/{total}] alpha={alpha}, gamma={gamma}, "
              f"eps_decay={eps_decay}")

        # Create and train Q-Learning agent
        env_train = InventoryEnv(regime_transitions=True)
        agent = QLearningAgent(
            n_states=n_states, n_actions=n_actions,
            alpha=alpha, gamma=gamma,
            epsilon_start=1.0, epsilon_end=0.05,
            epsilon_decay=eps_decay, seed=42
        )

        # Training loop
        for ep in range(n_train):
            state, _ = env_train.reset()
            done = False

            while not done:
                action = agent.select_action(state)
                next_state, reward, terminated, truncated, _ = \
                    env_train.step(action)
                done = terminated or truncated
                agent.update(state, action, reward, next_state, done)
                state = next_state

        # Evaluate
        env_eval = InventoryEnv(regime_transitions=True)
        eval_results, _ = evaluate_agent(agent, env_eval, n_eval)

        result = {
            'alpha': alpha,
            'gamma': gamma,
            'epsilon_decay': eps_decay,
            'profit_mean': eval_results['profits_mean'],
            'profit_std': eval_results['profits_std'],
            'stockout_rate': eval_results['stockout_rates_mean'],
            'avg_inventory': eval_results['avg_inventories_mean'],
        }
        results.append(result)

        print(f"    Profit: {result['profit_mean']:.2f} "
              f"+- {result['profit_std']:.2f} | "
              f"Stockout: {result['stockout_rate']:.3f}")

    # Sort by profit (descending)
    results.sort(key=lambda x: x['profit_mean'], reverse=True)

    # Print top results
    print(f"\n{'='*60}")
    print("  TOP 5 CONFIGURATIONS")
    print(f"{'='*60}")
    print(f"  {'Rank':<5s} {'alpha':>6s} {'gamma':>6s} {'eps_dec':>8s}  "
          f"{'Profit':>12s}  {'Stockout':>8s}")
    print(f"  {'-'*5} {'-'*6} {'-'*6} {'-'*8}  {'-'*12}  {'-'*8}")

    for i, r in enumerate(results[:5]):
        print(f"  {i+1:<5d} {r['alpha']:6.3f} {r['gamma']:6.3f} "
              f"{r['epsilon_decay']:8.4f}  "
              f"{r['profit_mean']:6.2f}+-{r['profit_std']:5.2f}  "
              f"{r['stockout_rate']:8.3f}")

    # Save results
    output_dir = os.path.join(
        os.path.dirname(os.path.dirname(__file__)), 'results'
    )
    os.makedirs(output_dir, exist_ok=True)
    sweep_path = os.path.join(output_dir, 'sweep_results.json')

    with open(sweep_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)

    print(f"\n  Results saved -> {sweep_path}")

    return results


if __name__ == '__main__':
    sweep_hyperparameters()
