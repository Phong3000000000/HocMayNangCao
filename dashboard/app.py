"""
Streamlit Dashboard for RL Inventory Management Demo.

Features:
    - Select demand regime (Low / Medium / High)
    - Select agent (Random, Heuristic, Q-Learning, SARSA, Double Q-Learning)
    - Inventory level chart over time
    - Daily order actions chart
    - Policy Table (inventory → recommended order)
    - Policy Heatmap
    - Learning curves
    - Real-time episode simulation with state/action/reward display

Usage:
    py -m streamlit run dashboard/app.py

Author: RL Inventory Management Team
"""

import os
import sys
import json
import numpy as np
import streamlit as st
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

# Add project root to path
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, PROJECT_ROOT)

from envs.custom_env import InventoryEnv, DEMAND_REGIMES, DAY_NAMES
from agents.random_agent import RandomAgent
from agents.heuristic_agent import AlwaysOrder2Agent, ReorderThresholdAgent
from agents.q_learning import QLearningAgent
from agents.sarsa import SARSAAgent
from agents.double_q_learning import DoubleQLearningAgent


# ═══════════════════════════════════════════════════════════════
# PAGE CONFIGURATION
# ═══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="RL Inventory Management",
    page_icon="📦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ═══════════════════════════════════════════════════════════════
# CUSTOM CSS
# ═══════════════════════════════════════════════════════════════
# ─── Unified color palette ─────────────────────────────────
COLOR_PRIMARY = '#4F46E5'    # Indigo-600
COLOR_SUCCESS = '#059669'    # Emerald-600
COLOR_WARNING = '#D97706'    # Amber-600
COLOR_DANGER  = '#DC2626'    # Red-600
COLOR_INFO    = '#2563EB'    # Blue-600
COLOR_PURPLE  = '#7C3AED'    # Violet-600
COLOR_SLATE   = '#475569'    # Slate-600
COLOR_LIGHT   = '#F8FAFC'    # Slate-50

CHART_COLORS = {
    'inventory': COLOR_SUCCESS,
    'orders': COLOR_INFO,
    'demand': COLOR_WARNING,
    'stockout': COLOR_DANGER,
    'reward': COLOR_PRIMARY,
    'cumulative': COLOR_PURPLE,
}

AGENT_CHART_COLORS = [
    '#EF4444',  # Red-500
    '#F59E0B',  # Amber-500
    '#10B981',  # Emerald-500
    '#3B82F6',  # Blue-500
    '#6366F1',  # Indigo-500
    '#8B5CF6',  # Violet-500
]

st.markdown("""
<style>
    .main-header {
        font-size: 2.2rem;
        font-weight: 700;
        text-align: center;
        padding: 0.8rem 0;
        background: linear-gradient(135deg, #4F46E5 0%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .main-subtitle {
        text-align: center;
        color: #64748B;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 4px;
    }
    .stTabs [data-baseweb="tab"] {
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 0.9rem;
    }
    section[data-testid="stSidebar"] {
        background-color: #F8FAFC;
    }
    section[data-testid="stSidebar"] h1,
    section[data-testid="stSidebar"] h2,
    section[data-testid="stSidebar"] h3 {
        color: #1E293B;
    }
</style>
""", unsafe_allow_html=True)


# ═══════════════════════════════════════════════════════════════
# HELPER FUNCTIONS
# ═══════════════════════════════════════════════════════════════

@st.cache_resource
def load_trained_agent(agent_type, seed=0, results_dir=None):
    """Load a trained agent from saved Q-table."""
    if results_dir is None:
        results_dir = os.path.join(PROJECT_ROOT, 'results')
    env = InventoryEnv()
    n_states = env.N_STATES
    n_actions = env.N_ACTIONS

    if agent_type == 'q_learning':
        agent = QLearningAgent(n_states, n_actions)
        model_path = os.path.join(results_dir, 'q_learning', f'seed_{seed}.npz')
    elif agent_type == 'sarsa':
        agent = SARSAAgent(n_states, n_actions)
        model_path = os.path.join(results_dir, 'sarsa', f'seed_{seed}.npz')
    elif agent_type == 'double_q_learning':
        agent = DoubleQLearningAgent(n_states, n_actions)
        model_path = os.path.join(results_dir, 'double_q_learning',
                                  f'seed_{seed}.npz')
    else:
        return None, False

    if os.path.exists(model_path):
        agent.load(model_path)
        return agent, True
    return agent, False


def get_agent(agent_type, env, results_dir=None):
    """Create or load an agent based on type."""
    if agent_type == 'Random':
        return RandomAgent(env.N_ACTIONS, seed=42), True
    elif agent_type == 'Always Order 2':
        return AlwaysOrder2Agent(), True
    elif agent_type == 'Reorder Threshold':
        return ReorderThresholdAgent(threshold=5, order_amount=5, env=env), True
    elif agent_type == 'Q-Learning':
        agent, loaded = load_trained_agent('q_learning', results_dir=results_dir)
        return agent, loaded
    elif agent_type == 'SARSA':
        agent, loaded = load_trained_agent('sarsa', results_dir=results_dir)
        return agent, loaded
    elif agent_type == 'Double Q-Learning':
        agent, loaded = load_trained_agent('double_q_learning', results_dir=results_dir)
        return agent, loaded
    return None, False


def run_episode(agent, env, seed=42):
    """Run a single episode and collect step data."""
    state, info = env.reset(seed=seed)
    agent.set_eval_mode()

    steps = []
    done = False

    while not done:
        inv, regime, dow, pending = env.state_decoder(state)
        action = agent.select_action(state)
        next_state, reward, terminated, truncated, info = env.step(action)
        done = terminated or truncated

        steps.append({
            'day': info['day'],
            'inventory_before': inv + pending,  # After receiving pending
            'action': action,
            'demand': info['demand'],
            'sold': info['sold'],
            'stockout': info['stockout'],
            'inventory_after': info['inventory_after'],
            'reward': reward,
            'revenue': info['revenue'],
            'purchase_cost': info['purchase_cost'],
            'holding_cost': info['holding_cost'],
            'stockout_penalty': info['stockout_penalty'],
            'regime': DEMAND_REGIMES[info['demand_regime']],
            'day_name': DAY_NAMES[(dow + 1) % 7],  # day_of_week after step
        })

        state = next_state

    agent.set_train_mode()
    return steps, env.get_episode_summary()


def build_policy_table(agent, env, regime=1, dow=0):
    """
    Build the policy table: for each (inventory, pending_order),
    show the recommended order amount.

    Returns a 2D numpy array: rows=inventory (0–20), cols=pending (0–5).
    """
    if hasattr(agent, 'get_policy'):
        policy = agent.get_policy()
    elif hasattr(agent, 'Q'):
        policy = np.argmax(agent.Q, axis=1)
    else:
        # Heuristic agents: simulate
        table = np.zeros((env.N_INVENTORY, env.N_PENDING), dtype=int)
        for inv in range(env.N_INVENTORY):
            for pending in range(env.N_PENDING):
                state_idx = env.state_encoder((inv, regime, dow, pending))
                table[inv, pending] = agent.select_action(state_idx)
        return table

    table = np.zeros((env.N_INVENTORY, env.N_PENDING), dtype=int)
    for inv in range(env.N_INVENTORY):
        for pending in range(env.N_PENDING):
            state_idx = env.state_encoder((inv, regime, dow, pending))
            table[inv, pending] = policy[state_idx]

    return table


# ═══════════════════════════════════════════════════════════════
# MAIN APPLICATION
# ═══════════════════════════════════════════════════════════════

def main():
    # ─── Header ────────────────────────────────────────────────
    st.markdown('<div class="main-header">RL Inventory Management</div>',
                unsafe_allow_html=True)
    st.markdown(
        '<div class="main-subtitle">'
        'Quan ly Ton kho bang Reinforcement Learning'
        '</div>',
        unsafe_allow_html=True
    )

    # ─── Sidebar Controls ─────────────────────────────────────
    with st.sidebar:
        st.header("Controls")

        agent_type = st.selectbox(
            "Select Agent",
            ['Random', 'Always Order 2', 'Reorder Threshold',
             'Q-Learning', 'SARSA', 'Double Q-Learning'],
            index=3  # Default to Q-Learning
        )

        # Training Budget selector
        results_100k_dir = os.path.join(PROJECT_ROOT, 'results_100k')
        budget_options = ['20,000 episodes']
        if os.path.isdir(results_100k_dir):
            budget_options.append('100,000 episodes')

        training_budget = st.selectbox(
            "Training Budget",
            budget_options,
            index=0,
            help="Select which trained model to use (20K or 100K episodes)"
        )

        # Determine results directory based on selection
        if training_budget == '100,000 episodes':
            selected_results_dir = results_100k_dir
        else:
            selected_results_dir = os.path.join(PROJECT_ROOT, 'results')

        weekend_surge = st.checkbox("Weekend Surge (unseen pattern)")
        surge_days = None
        if weekend_surge:
            selected_days = st.multiselect(
                "Select Surge Days",
                options=list(range(7)),
                default=[5, 6],
                format_func=lambda x: DAY_NAMES[x],
                help="Select days of the week when demand surge occurs"
            )
            surge_days = selected_days

        episode_seed = st.number_input("Episode Seed", 0, 999, 42)

        # Khởi tạo môi trường tạm thời để lấy xu hướng nhu cầu ban đầu dựa trên seed
        temp_env = InventoryEnv(
            regime_transitions=True,
            weekend_surge=weekend_surge,
            surge_days=surge_days
        )
        _, temp_info = temp_env.reset(seed=episode_seed)
        initial_regime_name = temp_info['demand_regime_name'].title()

        st.text_input(
            "Initial Demand Regime (from Seed)",
            value=initial_regime_name,
            disabled=True,
            help="The demand regime for Day 1, determined deterministically by the Episode Seed."
        )

        st.divider()
        st.markdown("### About")
        st.markdown("""
        **State**: (inventory, demand_regime, day, pending_order)
        - Inventory: 0-20 units
        - Demand: Low/Medium/High
        - Actions: Order 0-5 units
        - Episode: 30 days
        """)

    # ─── Load Agent ────────────────────────────────────────────
    env = InventoryEnv(
        regime_transitions=True,
        weekend_surge=weekend_surge,
        surge_days=surge_days
    )
    agent, is_loaded = get_agent(agent_type, env,
                                  results_dir=selected_results_dir)

    if agent is None:
        st.error("❌ Could not create agent.")
        return

    if agent_type in ['Q-Learning', 'SARSA', 'Double Q-Learning'] and not is_loaded:
        st.warning(
            f"No trained model found for {agent_type}. "
            f"Please run `py experiments/train.py` first. "
            f"Using untrained (random) Q-table."
        )

    # ─── Run Episode ───────────────────────────────────────────
    env_sim = InventoryEnv(
        regime_transitions=True,
        weekend_surge=weekend_surge,
        surge_days=surge_days
    )
    steps, summary = run_episode(agent, env_sim, seed=episode_seed)

    # ─── Tabs ──────────────────────────────────────────────────
    tab1, tab2, tab3, tab4 = st.tabs([
        "Episode Simulation",
        "Policy & Heatmap",
        "Learning Curves",
        "Agent Comparison"
    ])

    # ═══════════════════════════════════════════════════════════
    # TAB 1: Episode Simulation
    # ═══════════════════════════════════════════════════════════
    with tab1:
        st.subheader(f"Episode Simulation -- {agent_type}")

        # Metric cards
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("Total Profit", f"{summary['total_profit']:.1f}")
        with col2:
            st.metric("Avg Inventory", f"{summary['avg_inventory']:.1f}")
        with col3:
            st.metric("Stockout Rate",
                       f"{summary['stockout_rate']:.1%}")
        with col4:
            st.metric("Holding Cost",
                       f"{summary['total_holding_cost']:.1f}")
        with col5:
            st.metric("Order Frequency",
                       f"{summary['order_frequency']:.1%}")

        # Charts
        days = [s['day'] for s in steps]

        # Inventory chart
        fig_inv, ax_inv = plt.subplots(figsize=(12, 4))
        inventories = [s['inventory_after'] for s in steps]
        ax_inv.fill_between(days, inventories, alpha=0.2,
                            color=CHART_COLORS['inventory'])
        ax_inv.plot(days, inventories, 'o-',
                    color=CHART_COLORS['inventory'],
                    linewidth=2, markersize=4)
        ax_inv.axhline(y=5, color=COLOR_DANGER, linestyle='--',
                       alpha=0.5, label='Reorder point')
        ax_inv.set_xlabel('Day')
        ax_inv.set_ylabel('Inventory')
        ax_inv.set_title('Inventory Level Over Time')
        
        # Detail X and Y axes
        ax_inv.set_xticks(range(1, 31))
        ax_inv.set_yticks(range(0, max(inventories) + 2))
        ax_inv.tick_params(axis='both', labelsize=9)
        
        ax_inv.legend()
        ax_inv.grid(True, alpha=0.3)
        st.pyplot(fig_inv)
        plt.close(fig_inv)

        # Action + Demand charts
        col_a, col_b = st.columns(2)

        with col_a:
            fig_act, ax_act = plt.subplots(figsize=(10, 4))
            actions = [s['action'] for s in steps]
            ax_act.bar(days, actions, color=CHART_COLORS['orders'],
                       alpha=0.8, edgecolor='white')
            ax_act.set_xlabel('Day')
            ax_act.set_ylabel('Order Amount')
            ax_act.set_title('Daily Orders')
            
            # Detail X and Y axes
            ax_act.set_xticks(range(1, 31))
            ax_act.set_yticks(range(6))
            ax_act.tick_params(axis='both', labelsize=9)
            
            ax_act.grid(True, alpha=0.3)
            st.pyplot(fig_act)
            plt.close(fig_act)

        with col_b:
            fig_dem, ax_dem = plt.subplots(figsize=(10, 4))
            demands = [s['demand'] for s in steps]
            stockouts = [s['stockout'] for s in steps]
            ax_dem.bar(days, demands, color=CHART_COLORS['demand'],
                       alpha=0.7, label='Demand')
            ax_dem.bar(days, stockouts, color=CHART_COLORS['stockout'],
                       alpha=0.9, label='Stockout')
            ax_dem.set_xlabel('Day')
            ax_dem.set_ylabel('Units')
            ax_dem.set_title('Demand & Stockouts')
            
            # Detail X and Y axes
            ax_dem.set_xticks(range(1, 31))
            ax_dem.set_yticks(range(0, max(demands) + 2))
            ax_dem.tick_params(axis='both', labelsize=9)
            
            ax_dem.legend()
            ax_dem.grid(True, alpha=0.3)
            st.pyplot(fig_dem)
            plt.close(fig_dem)

        # Reward per day (instant reward) + Cumulative reward
        col_r1, col_r2 = st.columns(2)

        with col_r1:
            fig_rd, ax_rd = plt.subplots(figsize=(10, 4))
            rewards_daily = [s['reward'] for s in steps]
            bar_colors = [COLOR_SUCCESS if r >= 0 else COLOR_DANGER
                          for r in rewards_daily]
            ax_rd.bar(days, rewards_daily, color=bar_colors, alpha=0.8,
                      edgecolor='white')
            ax_rd.axhline(y=0, color=COLOR_SLATE, linestyle='-',
                          linewidth=0.8)
            ax_rd.set_xlabel('Day')
            ax_rd.set_ylabel('Reward')
            ax_rd.set_title('Daily Reward (Instant)')
            
            # Detail X and Y axes
            ax_rd.set_xticks(range(1, 31))
            min_r = int(np.floor(min(rewards_daily) / 10) * 10)
            max_r = int(np.ceil(max(rewards_daily) / 10) * 10)
            ax_rd.set_yticks(range(min_r, max_r + 1, 10))
            ax_rd.tick_params(axis='both', labelsize=9)
            
            ax_rd.grid(True, alpha=0.3)
            st.pyplot(fig_rd)
            plt.close(fig_rd)

        with col_r2:
            fig_rew, ax_rew = plt.subplots(figsize=(10, 4))
            cum_rewards = np.cumsum(rewards_daily)
            ax_rew.plot(days, cum_rewards, 'o-',
                        color=CHART_COLORS['cumulative'],
                        linewidth=2, markersize=4)
            ax_rew.fill_between(days, cum_rewards, alpha=0.15,
                                color=CHART_COLORS['cumulative'])
            ax_rew.set_xlabel('Day')
            ax_rew.set_ylabel('Cumulative Reward')
            ax_rew.set_title('Cumulative Reward')
            
            # Detail X and Y axes
            ax_rew.set_xticks(range(1, 31))
            min_cr = int(np.floor(min(cum_rewards) / 25) * 25)
            max_cr = int(np.ceil(max(cum_rewards) / 25) * 25)
            ax_rew.set_yticks(range(min_cr, max_cr + 1, 25))
            ax_rew.tick_params(axis='both', labelsize=9)
            
            ax_rew.grid(True, alpha=0.3)
            st.pyplot(fig_rew)
            plt.close(fig_rew)

        # Step-by-step table
        with st.expander("Step-by-Step Details", expanded=False):
            import pandas as pd
            df = pd.DataFrame(steps)
            st.dataframe(df, use_container_width=True, height=400)

    # ═══════════════════════════════════════════════════════════
    # TAB 2: Policy Table & Heatmap
    # ═══════════════════════════════════════════════════════════
    with tab2:
        st.subheader(f"Policy -- {agent_type}")

        pol_col1, pol_col2 = st.columns([1, 2])

        with pol_col1:
            st.markdown("#### Settings")

            pol_regime = st.selectbox(
                "Demand Regime for Policy",
                ['Low', 'Medium', 'High'],
                index=1,
                key='pol_regime'
            )
            pol_regime_id = {'Low': 0, 'Medium': 1, 'High': 2}[pol_regime]

            pol_dow = st.selectbox(
                "Day of Week",
                list(range(7)),
                format_func=lambda x: DAY_NAMES[x],
                key='pol_dow'
            )

        # Build policy table
        policy_table = build_policy_table(
            agent, env, regime=pol_regime_id, dow=pol_dow
        )

        with pol_col2:
            st.markdown("#### Policy Table")
            st.markdown(
                "*Rows = Inventory level (0–20), "
                "Columns = Pending order (0–5), "
                "Values = Recommended order amount*"
            )

            import pandas as pd
            df_policy = pd.DataFrame(
                policy_table,
                index=[f"Inv={i}" for i in range(21)],
                columns=[f"Pend={p}" for p in range(6)]
            )
            st.dataframe(df_policy, use_container_width=True, height=500)

        # Policy Heatmap
        st.markdown("#### Policy Heatmap")
        fig_heat, ax_heat = plt.subplots(figsize=(10, 12))
        im = ax_heat.imshow(policy_table, cmap='Blues', aspect='auto',
                            origin='lower', vmin=0, vmax=5)

        for inv in range(21):
            for pending in range(6):
                val = policy_table[inv, pending]
                color = 'white' if val >= 3 else '#1E293B'
                ax_heat.text(pending, inv, str(val),
                             ha='center', va='center',
                             fontsize=9, fontweight='bold', color=color)

        ax_heat.set_xlabel('Pending Order', fontsize=12)
        ax_heat.set_ylabel('Inventory Level', fontsize=12)
        ax_heat.set_title(
            f'Policy: {agent_type} | '
            f'Regime: {pol_regime} | Day: {DAY_NAMES[pol_dow]}',
            fontsize=14, fontweight='bold'
        )
        ax_heat.set_xticks(range(6))
        ax_heat.set_yticks(range(21))

        cbar = plt.colorbar(im, ax=ax_heat, label='Order Amount')
        cbar.set_ticks(range(6))

        plt.tight_layout()
        st.pyplot(fig_heat)
        plt.close(fig_heat)

    # ═══════════════════════════════════════════════════════════
    # TAB 3: Learning Curves
    # ═══════════════════════════════════════════════════════════
    with tab3:
        st.subheader("Learning Curves")
        st.caption(f"Showing results for: **{training_budget}**")

        results_dir = selected_results_dir
        agent_names = ['q_learning', 'sarsa', 'double_q_learning']
        colors = {
            'q_learning': '#3B82F6',
            'sarsa': '#6366F1',
            'double_q_learning': '#8B5CF6'
        }
        display_names = {
            'q_learning': 'Q-Learning',
            'sarsa': 'SARSA',
            'double_q_learning': 'Double Q-Learning'
        }

        has_any = False
        fig_lc, ax_lc = plt.subplots(figsize=(14, 6))

        for aname in agent_names:
            history_path = os.path.join(
                results_dir, f'{aname}_history.json'
            )
            if not os.path.exists(history_path):
                continue
            has_any = True

            with open(history_path, 'r') as f:
                histories = json.load(f)

            # Collect rewards across seeds
            all_rewards = []
            for seed_key, seed_data in histories.items():
                rewards = seed_data.get('episode_rewards', [])
                if rewards:
                    all_rewards.append(rewards)

            if not all_rewards:
                continue

            min_len = min(len(r) for r in all_rewards)
            all_rewards = np.array([r[:min_len] for r in all_rewards])

            # Smoothing (Adjusted window size for downsampled data)
            window = 20 if training_budget == '100,000 episodes' else 10
            if min_len > window:
                smoothed = np.array([
                    np.convolve(r, np.ones(window)/window, mode='valid')
                    for r in all_rewards
                ])
                mean_c = np.mean(smoothed, axis=0)
                std_c = np.std(smoothed, axis=0)
                
                # Scale X-axis to display correct episode numbers (factor of 50)
                budget_eps = 100000 if training_budget == '100,000 episodes' else 20000
                scale_factor = budget_eps / len(all_rewards[0])
                x = (np.arange(len(mean_c)) + window // 2) * scale_factor

                color = colors.get(aname, '#999')
                label = display_names.get(aname, aname)
                ax_lc.plot(x, mean_c, color=color, linewidth=2, label=label)
                ax_lc.fill_between(x, mean_c - std_c, mean_c + std_c,
                                   alpha=0.15, color=color)

        if has_any:
            ax_lc.set_xlabel('Episode', fontsize=12)
            ax_lc.set_ylabel('Total Reward', fontsize=12)
            ax_lc.set_title('Learning Curves (Mean ± Std across Seeds)',
                            fontsize=14, fontweight='bold')
            ax_lc.legend(fontsize=12)
            ax_lc.grid(True, alpha=0.3)
            st.pyplot(fig_lc)
            plt.close(fig_lc)
        else:
            st.info(
                "No training history found. "
                "Run `py experiments/train.py` first."
            )
            plt.close(fig_lc)

        # Epsilon schedule
        st.markdown("#### Epsilon Decay Schedule")
        for aname in agent_names:
            history_path = os.path.join(
                results_dir, f'{aname}_history.json'
            )
            if os.path.exists(history_path):
                with open(history_path, 'r') as f:
                    histories = json.load(f)
                first_seed = list(histories.keys())[0]
                epsilons = histories[first_seed].get('epsilons', [])
                if epsilons:
                    budget_eps = 100000 if training_budget == '100,000 episodes' else 20000
                    scale_factor = budget_eps / len(epsilons)
                    eps_x = np.arange(len(epsilons)) * scale_factor

                    fig_eps, ax_eps = plt.subplots(figsize=(10, 3))
                    ax_eps.plot(eps_x, epsilons, color='#FF6B6B', linewidth=1.5)
                    ax_eps.axhline(y=0.05, color='gray', linestyle='--',
                                   alpha=0.5, label='ε_min')
                    ax_eps.set_xlabel('Episode')
                    ax_eps.set_ylabel('Epsilon (ε)')
                    ax_eps.set_title(f'Epsilon Schedule — '
                                     f'{display_names.get(aname, aname)}')
                    ax_eps.legend()
                    ax_eps.grid(True, alpha=0.3)
                    st.pyplot(fig_eps)
                    plt.close(fig_eps)
                    break

    # ═══════════════════════════════════════════════════════════
    # TAB 4: Agent Comparison
    # ═══════════════════════════════════════════════════════════
    with tab4:
        st.subheader("Agent Comparison")
        st.caption(f"Showing results for: **{training_budget}**")

        eval_path = os.path.join(selected_results_dir,
                                 'evaluation_results.json')

        if os.path.exists(eval_path):
            with open(eval_path, 'r') as f:
                eval_results = json.load(f)

            # Filter out weekend surge for main comparison
            main_agents = {k: v for k, v in eval_results.items()
                           if 'weekend_surge' not in k}

            if main_agents:
                import pandas as pd

                # Build comparison dataframe
                comp_data = []
                for aname, metrics in main_agents.items():
                    comp_data.append({
                        'Agent': aname.replace('_', ' ').title(),
                        'Profit': f"{metrics.get('profits_mean', 0):.1f} "
                                  f"± {metrics.get('profits_std', 0):.1f}",
                        'Stockout Rate': f"{metrics.get('stockout_rates_mean', 0):.3f}",
                        'Holding Cost': f"{metrics.get('holding_costs_mean', 0):.1f}",
                        'Avg Inventory': f"{metrics.get('avg_inventories_mean', 0):.1f}",
                        'Order Freq': f"{metrics.get('order_frequencies_mean', 0):.3f}",
                    })

                df_comp = pd.DataFrame(comp_data)
                st.dataframe(df_comp, use_container_width=True)

                # Bar charts
                agent_labels = list(main_agents.keys())
                display_labels = [a.replace('_', ' ').title()
                                  for a in agent_labels]
                bar_colors = AGENT_CHART_COLORS

                fig_comp, axes = plt.subplots(2, 2, figsize=(14, 10))
                fig_comp.suptitle('Agent Comparison — Key Metrics',
                                  fontsize=16, fontweight='bold')

                metric_configs = [
                    ('profits_mean', 'profits_std', 'Profit ↑'),
                    ('stockout_rates_mean', 'stockout_rates_std',
                     'Stockout Rate ↓'),
                    ('holding_costs_mean', 'holding_costs_std',
                     'Holding Cost ↓'),
                    ('avg_inventories_mean', 'avg_inventories_std',
                     'Avg Inventory'),
                ]

                for idx, (mean_key, std_key, title) in enumerate(
                        metric_configs):
                    ax = axes[idx // 2][idx % 2]
                    vals = [main_agents[a].get(mean_key, 0)
                            for a in agent_labels]
                    errs = [main_agents[a].get(std_key, 0)
                            for a in agent_labels]
                    colors_list = bar_colors[:len(agent_labels)]

                    ax.bar(display_labels, vals, yerr=errs, capsize=5,
                           color=colors_list, alpha=0.8, edgecolor='white')
                    ax.set_title(title, fontsize=13)
                    ax.tick_params(axis='x', rotation=30)
                    ax.grid(axis='y', alpha=0.3)

                plt.tight_layout()
                st.pyplot(fig_comp)
                plt.close(fig_comp)
        else:
            st.info(
                "No evaluation results found. Run:\n\n"
                "```bash\n"
                "py experiments/train.py\n"
                "py experiments/evaluate.py\n"
                "```"
            )


if __name__ == '__main__':
    main()
