"""Head-to-head plot 2: All 5 kernels — absolute + % of peak.
Shows the full picture; Dot stands out as the outlier.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _common import *

cpx_node = node_total(CPX_H2H) / MB_TO_TB
tpx_node = node_total(TPX_H2H) / MB_TO_TB
spx_node = node_total(SPX_H2H) / MB_TO_TB

fig, (ax_abs, ax_pct) = plt.subplots(1, 2, figsize=(13, 5))

x = np.arange(len(OPS))
w = 0.25

# Absolute bars
for i, (mode, vals) in enumerate([('CPX', cpx_node), ('TPX', tpx_node), ('SPX', spx_node)]):
    ax_abs.bar(x + (i - 1) * w, vals, w, color=MODE_COLORS[mode],
               edgecolor='white', linewidth=0.5, label=mode, zorder=3)

ax_abs.axhline(THEO_NODE, color='red', ls=':', lw=1.2, alpha=0.5,
               label=f'Peak: {THEO_NODE:.1f} TB/s')
ax_abs.set_xticks(x)
ax_abs.set_xticklabels(OPS, fontsize=11, fontweight='bold')
ax_abs.set_ylim(0, THEO_NODE * 1.12)
style_ax(ax_abs, ylabel='TB/s (whole node)', title='Whole-Node Bandwidth — All Kernels')
ax_abs.legend(fontsize=9)

# % of peak lines
for mode, vals in [('CPX', cpx_node), ('TPX', tpx_node), ('SPX', spx_node)]:
    pcts = vals / THEO_NODE * 100
    ax_pct.plot(OPS, pcts, '-o', color=MODE_COLORS[mode],
                markersize=8, linewidth=2.5, label=mode)

ax_pct.axhline(100, color='red', ls=':', lw=1.2, alpha=0.4)
ax_pct.set_ylim(40, 105)
style_ax(ax_pct, ylabel='% of theoretical peak',
         title='Efficiency — Dot Drops Sharply', grid_axis='both')
ax_pct.legend(fontsize=10)

fig.suptitle('All Five BabelStream Kernels — CPX vs TPX vs SPX',
             fontsize=14, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.93])
savefig(fig, 'h2h_02_all_kernels.png')
