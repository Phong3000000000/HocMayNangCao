import os
import matplotlib.pyplot as plt
import matplotlib.patches as patches

def main():
    # Set up dark slide size: 16:9 ratio
    fig, ax = plt.subplots(figsize=(13.333, 7.5), facecolor='#0F172A')
    ax.set_facecolor('#0F172A')
    
    # Hide axes
    ax.axis('off')
    ax.set_xlim(0, 16)
    ax.set_ylim(0, 9)
    
    # Add title (Vietnamese & English)
    ax.text(8, 8.0, "TẦNG 1: MA TRẬN CHUYỂN ĐỔI XU HƯỚNG NHU CẦU", 
            color='#F8FAFC', fontsize=24, fontweight='bold', ha='center', va='center')
    ax.text(8, 7.4, "Markov Chain Transition Matrix -- Mô phỏng tính quán tính của thị trường", 
            color='#38BDF8', fontsize=14, fontweight='semibold', ha='center', va='center')
    
    # Draw table outline / panel (glassmorphism effect with translucent grey background)
    rect = patches.FancyBboxPatch((1.2, 1.8), 13.6, 4.8, boxstyle="round,pad=0.2",
                                  linewidth=1.5, edgecolor='#334155', facecolor='#1E293B', alpha=0.9)
    ax.add_patch(rect)
    
    # Define table data
    headers = ["Hôm nay \\ Ngày mai", "Low (Thấp)", "Medium (Vừa)", "High (Cao)"]
    row_labels = ["Low (Thấp)", "Medium (Vừa)", "High (Cao)"]
    data = [
        ["90%", "8%", "2%"],
        ["5%", "85%", "10%"],
        ["2%", "8%", "90%"]
    ]
    
    # Colors for transition cells
    cell_colors = [
        ['#475569', '#334155', '#334155'],  # Slate for Low (staying low is 90%)
        ['#334155', '#D97706', '#334155'],  # Amber for Medium (staying medium is 85%)
        ['#334155', '#334155', '#DC2626']   # Red for High (staying high is 90%)
    ]
    
    # Column X coordinates
    col_x = [2.2, 5.8, 9.2, 12.6]
    # Row Y coordinates
    row_y = [5.6, 4.4, 3.2, 2.0]
    
    # Draw headers
    for idx, h in enumerate(headers):
        color = '#F8FAFC' if idx > 0 else '#94A3B8'
        ax.text(col_x[idx] + 1.2, 6.1, h, color=color, fontsize=16, fontweight='bold', ha='center', va='center')
        
    # Draw horizontal line under header
    ax.plot([1.5, 14.5], [5.8, 5.8], color='#475569', linewidth=1.5)
    
    # Draw table rows
    for r_idx, label in enumerate(row_labels):
        # Draw Row Label
        ax.text(col_x[0] + 1.2, row_y[r_idx+1], label, color='#38BDF8', fontsize=15, fontweight='bold', ha='center', va='center')
        
        # Draw cells
        for c_idx, val in enumerate(data[r_idx]):
            x = col_x[c_idx+1]
            y = row_y[r_idx+1]
            bg_color = cell_colors[r_idx][c_idx]
            
            # Draw cell background card
            cell_box = patches.FancyBboxPatch((x - 1.2, y - 0.42), 2.4, 0.84, boxstyle="round,pad=0.1",
                                             edgecolor='#475569', facecolor=bg_color, linewidth=1.2)
            ax.add_patch(cell_box)
            
            # Draw value text
            is_diagonal = (r_idx == c_idx)
            text_color = '#F8FAFC' if is_diagonal else '#94A3B8'
            font_w = 'bold' if is_diagonal else 'normal'
            font_s = 18 if is_diagonal else 15
            ax.text(x, y, val, color=text_color, fontsize=font_s, fontweight=font_w, ha='center', va='center')
            
    # Add footnote explanation at the bottom
    ax.text(8, 1.2, "Đặc điểm: Xu hướng có quán tính từ 85% - 90% (Hôm nay đông khách thì ngày mai rất có thể tiếp tục đông khách).",
            color='#94A3B8', fontsize=13, fontweight='medium', fontstyle='italic', ha='center', va='center')
    
    # Save slide
    os.makedirs('reports/figures', exist_ok=True)
    out_path = 'reports/figures/regime_transition_slide_clean.png'
    plt.savefig(out_path, dpi=300, facecolor=fig.get_facecolor(), edgecolor='none', bbox_inches='tight')
    plt.close()
    print(f"Generated clean transition slide at {out_path}")

if __name__ == '__main__':
    main()
