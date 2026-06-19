import os
import numpy as np
import matplotlib.pyplot as plt

# Define distributions matching custom_env.py
DEMAND_DISTRIBUTIONS = {
    'Low': {
        'values': [0, 1, 2, 3, 4],
        'probs':  [0.10, 0.30, 0.30, 0.20, 0.10],
        'color': '#475569'  # Slate (representing low activity)
    },
    'Medium': {
        'values': [0, 1, 2, 3, 4, 5, 6],
        'probs':  [0.05, 0.08, 0.15, 0.25, 0.22, 0.15, 0.10],
        'color': '#D97706'  # Amber (representing moderate activity)
    },
    'High': {
        'values': [0, 1, 2, 3, 4, 5, 6, 7, 8],
        'probs':  [0.02, 0.03, 0.05, 0.08, 0.12, 0.20, 0.22, 0.18, 0.10],
        'color': '#DC2626'  # Red/Crimson (representing high activity)
    }
}

def main():
    fig, axes = plt.subplots(1, 3, figsize=(18, 5.5), sharey=True)
    fig.suptitle('Discrete Demand Probability Distributions by Regime', fontsize=16, fontweight='bold', y=1.02)
    
    for idx, (regime, data) in enumerate(DEMAND_DISTRIBUTIONS.items()):
        ax = axes[idx]
        values = data['values']
        probs = data['probs']
        color = data['color']
        
        # Plot bars
        bars = ax.bar(values, [p * 100 for p in probs], color=color, alpha=0.85, edgecolor='black', linewidth=0.8)
        
        # Styling
        ax.set_title(f'{regime} Regime (Avg: ~{sum(v*p for v, p in zip(values, probs)):.1f}/day)', fontsize=13, fontweight='bold', pad=10)
        ax.set_xlabel('Demand (Units / Customers)', fontsize=11)
        if idx == 0:
            ax.set_ylabel('Probability (%)', fontsize=11)
        
        ax.set_xticks(values)
        ax.set_ylim(0, 35)
        ax.grid(axis='y', alpha=0.3, linestyle='--')
        
        # Add labels on top of bars
        for bar in bars:
            height = bar.get_height()
            if height > 0:
                ax.annotate(f'{height:.0f}%',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),
                            textcoords="offset points",
                            ha='center', va='bottom', fontsize=9.5, fontweight='bold')

    plt.tight_layout()
    
    # Save directory
    os.makedirs('reports/figures', exist_ok=True)
    out_path = 'reports/figures/demand_distributions.png'
    plt.savefig(out_path, dpi=300, bbox_inches='tight')
    plt.close()
    print(f"Saved demand distributions plot to {out_path}")

if __name__ == '__main__':
    main()
