"""
Plotting Utilities for RL Inventory Management.

Generates publication-quality plots:
    - Learning curves (reward per episode, smoothed)
    - Agent comparison bar charts (mean ± std)
    - Inventory level time series
    - Policy heatmaps
    - Stockout rate comparison
    - Epsilon decay visualization

Author: RL Inventory Management Team
"""

import os
import sys
import json
import numpy as np
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend for saving
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ─── Plot Style ────────────────────────────────────────────────
plt.style.use('seaborn-v0_8-darkgrid')
COLORS = {
    'random': '#FF6B6B',
    'always_order_2': '#FFA94D',
    'reorder_threshold': '#FFD93D',
    'q_learning': '#51CF66',
    'sarsa': '#339AF0',
    'double_q_learning': '#845EF7',
}
AGENT_DISPLAY_NAMES = {
    'random': 'Random',
    'always_order_2': 'Always Order 2',
    'reorder_threshold': 'Reorder Threshold',
    'q_learning': 'Q-Learning',
    'sarsa': 'SARSA',
    'double_q_learning': 'Double Q-Learning',
}


def smooth(values, window=50):
    """Apply moving average smoothing to a 1D array."""
    if len(values) < window:
        return values
    kernel = np.ones(window) / window
    return np.convolve(values, kernel, mode='valid')


def plot_learning_curves(results_dir, output_dir=None):
    """
    Plot learning curves for all trained RL agents.

    Shows reward per episode with smoothing, averaged across seeds
    with std shading.

    Args:
        results_dir (str): Directory containing *_history.json files.
        output_dir (str, optional): Where to save figures. Defaults to
            results_dir/../reports/figures.
    """
    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(results_dir), 'reports', 'figures'
        )
    os.makedirs(output_dir, exist_ok=True)

    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('Learning Curves — Reward per Episode',
                 fontsize=16, fontweight='bold')

    agent_names = ['q_learning', 'sarsa', 'double_q_learning']

    for idx, agent_name in enumerate(agent_names):
        history_path = os.path.join(
            results_dir, f'{agent_name}_history.json'
        )
        if not os.path.exists(history_path):
            continue

        with open(history_path, 'r') as f:
            histories = json.load(f)

        # Collect rewards across all seeds
        all_rewards = []
        for seed_key, seed_data in histories.items():
            rewards = seed_data['episode_rewards']
            all_rewards.append(rewards)

        if not all_rewards:
            continue

        # Align lengths (trim to shortest)
        min_len = min(len(r) for r in all_rewards)
        all_rewards = np.array([r[:min_len] for r in all_rewards])

        # Smooth each seed
        window = 50
        smoothed = np.array([smooth(r, window) for r in all_rewards])
        mean_curve = np.mean(smoothed, axis=0)
        std_curve = np.std(smoothed, axis=0)
        x = np.arange(len(mean_curve)) + window // 2

        ax = axes[idx]
        color = COLORS.get(agent_name, '#999')
        display_name = AGENT_DISPLAY_NAMES.get(agent_name, agent_name)

        ax.plot(x, mean_curve, color=color, linewidth=2, label='Mean')
        ax.fill_between(x, mean_curve - std_curve, mean_curve + std_curve,
                        alpha=0.2, color=color, label='± 1 Std')
        ax.set_title(display_name, fontsize=14)
        ax.set_xlabel('Episode')
        ax.set_ylabel('Total Reward')
        ax.legend(loc='lower right')
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(output_dir, 'learning_curves.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  [OK] Saved: {path}")
    return path


def plot_agent_comparison(eval_results, output_dir):
    """
    Bar chart comparing all agents on key metrics.

    Args:
        eval_results (dict): {agent_name: {metric_mean, metric_std, ...}}
        output_dir (str): Where to save the figure.
    """
    os.makedirs(output_dir, exist_ok=True)

    agents = list(eval_results.keys())
    # Filter out weekend_surge variants for main comparison
    agents = [a for a in agents if 'weekend_surge' not in a]

    metrics = ['profits_mean', 'stockout_rates_mean',
               'holding_costs_mean', 'avg_inventories_mean']
    metric_labels = ['Profit (↑)', 'Stockout Rate (↓)',
                     'Holding Cost (↓)', 'Avg Inventory']
    metric_stds = ['profits_std', 'stockout_rates_std',
                   'holding_costs_std', 'avg_inventories_std']

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('Agent Comparison — Evaluation Metrics',
                 fontsize=16, fontweight='bold')

    for idx, (metric, label, std_key) in enumerate(
            zip(metrics, metric_labels, metric_stds)):
        ax = axes[idx // 2][idx % 2]

        values = []
        errors = []
        colors = []
        labels = []

        for agent in agents:
            res = eval_results[agent]
            val = res.get(metric, 0)
            err = res.get(std_key, 0)
            values.append(val)
            errors.append(err)
            colors.append(COLORS.get(agent, '#999'))
            labels.append(AGENT_DISPLAY_NAMES.get(agent, agent))

        bars = ax.bar(labels, values, yerr=errors, capsize=5,
                      color=colors, alpha=0.8, edgecolor='white',
                      linewidth=1.5)

        ax.set_title(label, fontsize=13)
        ax.set_ylabel(label.split('(')[0].strip())

        # Rotate labels if many agents
        if len(labels) > 4:
            ax.set_xticklabels(labels, rotation=30, ha='right')

        ax.grid(axis='y', alpha=0.3)

    plt.tight_layout()
    path = os.path.join(output_dir, 'agent_comparison.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  [OK] Saved: {path}")
    return path


def plot_policy_heatmap(agent, env, regime=1, dow=0, output_dir=None):
    """
    Plot policy heatmap: inventory (rows) × pending_order (cols) → action.

    Fixed demand_regime and day_of_week to show a 2D slice of the policy.

    Args:
        agent: Trained agent with get_policy() or Q attribute.
        env: InventoryEnv instance (for state encoding).
        regime (int): Demand regime to fix (0=low, 1=medium, 2=high).
        dow (int): Day of week to fix (0=Mon, ..., 6=Sun).
        output_dir (str, optional): Where to save.

    Returns:
        str: Path to saved figure.
    """
    from envs.custom_env import DEMAND_REGIMES

    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'reports', 'figures'
        )
    os.makedirs(output_dir, exist_ok=True)

    # Build policy matrix: inventory × pending_order → action
    policy_matrix = np.zeros((env.N_INVENTORY, env.N_PENDING), dtype=int)

    # Get policy from agent
    if hasattr(agent, 'get_policy'):
        full_policy = agent.get_policy()
    elif hasattr(agent, 'Q'):
        full_policy = np.argmax(agent.Q, axis=1)
    else:
        raise ValueError("Agent must have get_policy() or Q attribute")

    for inv in range(env.N_INVENTORY):
        for pending in range(env.N_PENDING):
            state_idx = env.state_encoder((inv, regime, dow, pending))
            policy_matrix[inv, pending] = full_policy[state_idx]

    regime_name = DEMAND_REGIMES[regime]

    fig, ax = plt.subplots(figsize=(8, 10))
    im = ax.imshow(policy_matrix, cmap='YlOrRd', aspect='auto',
                   origin='lower', vmin=0, vmax=5)

    # Annotate cells with action values
    for inv in range(env.N_INVENTORY):
        for pending in range(env.N_PENDING):
            ax.text(pending, inv, str(policy_matrix[inv, pending]),
                    ha='center', va='center', fontsize=9,
                    color='white' if policy_matrix[inv, pending] >= 3
                    else 'black')

    ax.set_xlabel('Pending Order', fontsize=12)
    ax.set_ylabel('Inventory Level', fontsize=12)
    ax.set_title(f'Policy Heatmap — {agent.name}\n'
                 f'(Regime: {regime_name}, Day: {dow})',
                 fontsize=14, fontweight='bold')

    ax.set_xticks(range(env.N_PENDING))
    ax.set_yticks(range(0, env.N_INVENTORY, 2))

    cbar = plt.colorbar(im, ax=ax, label='Order Amount')
    cbar.set_ticks(range(6))

    plt.tight_layout()
    path = os.path.join(output_dir,
                        f'policy_heatmap_{agent.name.lower().replace(" ", "_")}'
                        f'_regime{regime}.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  [OK] Saved: {path}")
    return path


def plot_episode_details(episode_history, agent_name="Agent",
                         output_dir=None):
    """
    Plot detailed episode visualization: inventory, actions, demand, reward.

    Args:
        episode_history (list[dict]): Step-by-step history from env.
        agent_name (str): Agent name for title.
        output_dir (str, optional): Where to save.

    Returns:
        str: Path to saved figure.
    """
    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'reports', 'figures'
        )
    os.makedirs(output_dir, exist_ok=True)

    days = [s['day'] for s in episode_history]
    inventories = [s['inventory_after'] for s in episode_history]
    actions = [s['action'] for s in episode_history]
    demands = [s['demand'] for s in episode_history]
    rewards = [s['reward'] for s in episode_history]
    stockouts = [s['stockout'] for s in episode_history]

    fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
    fig.suptitle(f'Episode Details — {agent_name}',
                 fontsize=16, fontweight='bold')

    # 1. Inventory level
    ax = axes[0]
    ax.fill_between(days, inventories, alpha=0.3, color='#51CF66')
    ax.plot(days, inventories, 'o-', color='#2B8A3E',
            linewidth=2, markersize=4)
    ax.set_ylabel('Inventory')
    ax.set_title('Inventory Level Over Time')
    ax.axhline(y=5, color='red', linestyle='--', alpha=0.5,
               label='Reorder point (5)')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Actions (orders)
    ax = axes[1]
    ax.bar(days, actions, color='#339AF0', alpha=0.8, edgecolor='white')
    ax.set_ylabel('Order Amount')
    ax.set_title('Daily Order Actions')
    ax.set_yticks(range(6))
    ax.grid(True, alpha=0.3)

    # 3. Demand and stockout
    ax = axes[2]
    ax.bar(days, demands, color='#FFA94D', alpha=0.7,
           label='Demand', edgecolor='white')
    ax.bar(days, stockouts, color='#FF6B6B', alpha=0.9,
           label='Stockout', edgecolor='white')
    ax.set_ylabel('Units')
    ax.set_title('Daily Demand & Stockouts')
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 4. Cumulative reward
    ax = axes[3]
    cum_rewards = np.cumsum(rewards)
    ax.plot(days, cum_rewards, 'o-', color='#845EF7',
            linewidth=2, markersize=4)
    ax.fill_between(days, cum_rewards, alpha=0.2, color='#845EF7')
    ax.set_ylabel('Cumulative Reward')
    ax.set_xlabel('Day')
    ax.set_title('Cumulative Reward Over Episode')
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(output_dir,
                        f'episode_{agent_name.lower().replace(" ", "_")}.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  [OK] Saved: {path}")
    return path


def plot_epsilon_schedule(histories, output_dir=None):
    """
    Plot epsilon decay schedule across training.

    Args:
        histories (dict): Training histories loaded from JSON.
        output_dir (str): Where to save.
    """
    if output_dir is None:
        output_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'reports', 'figures'
        )
    os.makedirs(output_dir, exist_ok=True)

    fig, ax = plt.subplots(figsize=(10, 5))

    # Use first seed
    first_seed = list(histories.keys())[0]
    epsilons = histories[first_seed].get('epsilons', [])

    if epsilons:
        ax.plot(epsilons, color='#FF6B6B', linewidth=2)
        ax.set_xlabel('Training Step', fontsize=12)
        ax.set_ylabel('Epsilon (ε)', fontsize=12)
        ax.set_title('Epsilon Decay Schedule', fontsize=14,
                      fontweight='bold')
        ax.axhline(y=0.05, color='gray', linestyle='--',
                   alpha=0.5, label='ε_min = 0.05')
        ax.legend()
        ax.grid(True, alpha=0.3)

    plt.tight_layout()
    path = os.path.join(output_dir, 'epsilon_schedule.png')
    fig.savefig(path, dpi=150, bbox_inches='tight')
    plt.close(fig)
    print(f"  [OK] Saved: {path}")
    return path


def generate_all_plots(results_dir=None):
    """
    Generate all plots from training results and evaluation.

    Args:
        results_dir (str): Path to results/ directory.
    """
    if results_dir is None:
        results_dir = os.path.join(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
            'results'
        )

    output_dir = os.path.join(
        os.path.dirname(results_dir), 'reports', 'figures'
    )
    os.makedirs(output_dir, exist_ok=True)

    print(f"\n{'='*60}")
    print("  GENERATING PLOTS")
    print(f"{'='*60}")

    # 1. Learning curves
    print("\n  > Learning Curves")
    plot_learning_curves(results_dir, output_dir)

    # 2. Epsilon schedule
    print("\n  > Epsilon Schedule")
    for agent_name in ['q_learning', 'sarsa', 'double_q_learning']:
        history_path = os.path.join(
            results_dir, f'{agent_name}_history.json'
        )
        if os.path.exists(history_path):
            with open(history_path, 'r') as f:
                histories = json.load(f)
            plot_epsilon_schedule(histories, output_dir)
            break  # One plot is enough

    # 3. Agent comparison (requires evaluation_results.json)
    eval_path = os.path.join(results_dir, 'evaluation_results.json')
    if os.path.exists(eval_path):
        print("\n  > Agent Comparison")
        with open(eval_path, 'r') as f:
            eval_results = json.load(f)
        plot_agent_comparison(eval_results, output_dir)

    # 4. Policy heatmaps for trained agents
    print("\n  > Policy Heatmaps")
    from envs.custom_env import InventoryEnv
    env = InventoryEnv()

    for agent_name in ['q_learning', 'double_q_learning']:
        model_path = os.path.join(results_dir, agent_name, 'seed_0.npz')
        if os.path.exists(model_path):
            if agent_name == 'q_learning':
                from agents.q_learning import QLearningAgent
                agent = QLearningAgent(env.N_STATES, env.N_ACTIONS)
            else:
                from agents.double_q_learning import DoubleQLearningAgent
                agent = DoubleQLearningAgent(env.N_STATES, env.N_ACTIONS)

            agent.load(model_path)

            for regime in [0, 1, 2]:
                plot_policy_heatmap(agent, env, regime=regime,
                                   dow=0, output_dir=output_dir)

    print(f"\n  All plots saved -> {output_dir}")


if __name__ == '__main__':
    generate_all_plots()
