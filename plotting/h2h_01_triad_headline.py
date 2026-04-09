"""Head-to-head plot 1: Triad whole-node — the hero chart.
Single bar chart with annotated TB/s and % of peak.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _common import *

cpx_node = node_total(CPX_H2H) / MB_TO_TB
tpx_node = node_total(TPX_H2H) / MB_TO_TB
spx_node = node_total(SPX_H2H) / MB_TO_TB

triad_idx = 3

fig, ax = plt.subplots(figsize=(7, 5))

modes = ['CPX', 'TPX', 'SPX']
triad_vals = [cpx_node[triad_idx], tpx_node[triad_idx], spx_node[triad_idx]]
bars = ax.bar(modes, triad_vals,
              color=[MODE_COLORS[m] for m in modes],
              edgecolor='white', linewidth=1, width=0.55, zorder=3)

ax.axhline(THEO_NODE, color='red', ls=':', lw=1.4, alpha=0.6,
           label=f'Theoretical peak: {THEO_NODE:.1f} TB/s')

for bar, val in zip(bars, triad_vals):
    pct = val / THEO_NODE * 100
    ax.text(bar.get_x() + bar.get_width() / 2, val + 0.3,
            f'{val:.1f} TB/s\n({pct:.0f}% of peak)',
            ha='center', va='bottom', fontsize=11, fontweight='bold')

ax.set_ylim(0, THEO_NODE * 1.22)
style_ax(ax, ylabel='TB/s (whole node)',
         title='Whole-Node Triad Bandwidth\nCPX vs TPX vs SPX (Normalised Array Size)')
ax.legend(fontsize=10, loc='upper right')

fig.tight_layout()
savefig(fig, 'h2h_01_triad_headline.png')
