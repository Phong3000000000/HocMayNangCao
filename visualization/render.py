"""
Text-based Renderer for Inventory Environment.

Provides detailed step-by-step rendering of agent-environment interaction
for debugging and demonstration.

Author: RL Inventory Management Team
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from envs.custom_env import InventoryEnv, DEMAND_REGIMES, DAY_NAMES


def render_episode(agent, env, seed=42, max_steps=None):
    """
    Render a full episode step-by-step in the terminal.

    Displays state, action, demand, reward, and inventory bar chart
    for each day of the episode.

    Args:
        agent: Agent with select_action() method.
        env: InventoryEnv instance.
        seed (int): Random seed for the episode.
        max_steps (int, optional): Limit rendering to first N steps.

    Returns:
        list[dict]: Episode history (step details).
    """
    state, info = env.reset(seed=seed)
    agent.set_eval_mode()

    step = 0
    total_reward = 0.0
    done = False

    print(f"\n{'╔' + '═'*58 + '╗'}")
    print(f"║{'INVENTORY MANAGEMENT — EPISODE RENDER':^58s}║")
    print(f"║{'Agent: ' + agent.name:^58s}║")
    print(f"{'╚' + '═'*58 + '╝'}")

    while not done:
        # Decode current state for display
        inv, regime, dow, pending = env.state_decoder(state)
        regime_name = DEMAND_REGIMES[regime]
        day_name = DAY_NAMES[dow]

        # Agent selects action
        action = agent.select_action(state)

        # Environment step
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated
        total_reward += reward

        step += 1

        # ── Render this step ───────────────────────────────────
        # Inventory bar
        bar_filled = '█' * min(info['inventory_after'], 20)
        bar_empty = '░' * (20 - min(info['inventory_after'], 20))

        print(f"\n  Day {step:2d} ({day_name}) │ Regime: {regime_name}")
        print(f"  {'─'*50}")
        print(f"  Inventory (start): {inv:2d} + Pending: {pending} "
              f"→ {min(inv + pending, 20):2d}")
        print(f"  Action:  Order {action} units  "
              f"(cost: {info['purchase_cost']:.0f})")
        print(f"  Demand:  {info['demand']} units  │  "
              f"Sold: {info['sold']}  │  "
              f"Stockout: {info['stockout']}")
        print(f"  Inventory (end): [{bar_filled}{bar_empty}] "
              f"{info['inventory_after']:2d}/20")
        print(f"  Reward:  {reward:+.1f}  "
              f"(Rev: {info['revenue']:.0f}, "
              f"Hold: -{info['holding_cost']:.1f}, "
              f"Stkout: -{info['stockout_penalty']:.1f})")

        state = next_state

        if max_steps and step >= max_steps:
            print(f"\n  ... (truncated at step {max_steps})")
            break

    # ── Episode summary ────────────────────────────────────────
    summary = env.get_episode_summary()
    print(f"\n{'═'*58}")
    print(f"  EPISODE SUMMARY ({step} days)")
    print(f"{'─'*58}")
    print(f"  Total Profit:        {summary['total_profit']:8.2f}")
    print(f"  Total Revenue:       {summary['total_revenue']:8.2f}")
    print(f"  Total Purchase Cost: {summary['total_purchase_cost']:8.2f}")
    print(f"  Total Holding Cost:  {summary['total_holding_cost']:8.2f}")
    print(f"  Total Stockout Pen.: {summary['total_stockout_penalty']:8.2f}")
    print(f"  Stockout Rate:       {summary['stockout_rate']:8.2%}")
    print(f"  Order Frequency:     {summary['order_frequency']:8.2%}")
    print(f"  Avg Inventory:       {summary['avg_inventory']:8.2f}")
    print(f"{'═'*58}")

    agent.set_train_mode()
    return env.episode_history


def compare_agents_render(agents, env_class=InventoryEnv, seed=42):
    """
    Render episodes for multiple agents side by side (sequential).

    Args:
        agents (list): List of agent instances.
        env_class: Environment class to instantiate.
        seed (int): Common seed for fair comparison.
    """
    for agent in agents:
        env = env_class(regime_transitions=True)
        render_episode(agent, env, seed=seed)
        print("\n")


if __name__ == '__main__':
    from agents.random_agent import RandomAgent
    from agents.heuristic_agent import AlwaysOrder2Agent

    env = InventoryEnv(regime_transitions=True)

    print("="*60)
    print("  RANDOM AGENT DEMO")
    print("="*60)
    render_episode(RandomAgent(6, seed=0), env, seed=42)

    print("\n\n")
    print("="*60)
    print("  ALWAYS ORDER 2 AGENT DEMO")
    print("="*60)
    env2 = InventoryEnv(regime_transitions=True)
    render_episode(AlwaysOrder2Agent(), env2, seed=42)
