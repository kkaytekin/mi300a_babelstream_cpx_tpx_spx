"""Head-to-head plot 4: The Dot penalty.
Dot reduction hits SPX hardest — 47% of peak vs 64% for CPX.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _common import *

cpx_node = node_total(CPX_H2H) / MB_TO_TB
tpx_node = node_total(TPX_H2H) / MB_TO_TB
spx_node = node_total(SPX_H2H) / MB_TO_TB

cpx_apu = apu_totals(CPX_H2H, CPX_APU_MAP)
tpx_apu = apu_totals(TPX_H2H, TPX_APU_MAP)
spx_apu = apu_totals(SPX_H2H, SPX_APU_MAP)

triad_idx = 3
dot_idx = 4

fig, (ax_compare, ax_apu) = plt.subplots(1, 2, figsize=(13, 5))

# Left: Triad vs Dot whole-node comparison
modes = ['CPX', 'TPX', 'SPX']
x = np.arange(len(modes))
w = 0.3

triad_pcts = [cpx_node[triad_idx] / THEO_NODE * 100,
              tpx_node[triad_idx] / THEO_NODE * 100,
              spx_node[triad_idx] / THEO_NODE * 100]
dot_pcts = [cpx_node[dot_idx] / THEO_NODE * 100,
            tpx_node[dot_idx] / THEO_NODE * 100,
            spx_node[dot_idx] / THEO_NODE * 100]

bars_t = ax_compare.bar(x - w/2, triad_pcts, w, color='#1565C0', edgecolor='white',
                        linewidth=0.5, label='Triad', zorder=3)
bars_d = ax_compare.bar(x + w/2, dot_pcts, w, color='#E65100', edgecolor='white',
                        linewidth=0.5, label='Dot', zorder=3)

# Annotate the gap
for i in range(3):
    gap = triad_pcts[i] - dot_pcts[i]
    mid_y = (triad_pcts[i] + dot_pcts[i]) / 2
    ax_compare.annotate(f'−{gap:.0f}pp', xy=(x[i] + w/2 + 0.05, mid_y),
                        fontsize=9, fontweight='bold', color='#B71C1C',
                        ha='left', va='center')

ax_compare.axhline(100, color='red', ls=':', lw=1.2, alpha=0.4)
ax_compare.set_xticks(x)
ax_compare.set_xticklabels(modes, fontsize=12, fontweight='bold')
ax_compare.set_ylim(30, 110)
style_ax(ax_compare, ylabel='% of theoretical peak',
         title='Triad vs Dot — The Reduction Penalty')
ax_compare.legend(fontsize=10)

# Right: Dot % of peak per APU
x4 = np.arange(4)
w4 = 0.25
for i, (mode, apu_dict) in enumerate([('CPX', cpx_apu), ('TPX', tpx_apu), ('SPX', spx_apu)]):
    pcts = [apu_dict[a][dot_idx] / MB_TO_TB / THEO_APU * 100 for a in range(4)]
    ax_apu.bar(x4 + (i - 1) * w4, pcts, w4, color=MODE_COLORS[mode],
               edgecolor='white', linewidth=0.5, label=mode, zorder=3)

ax_apu.axhline(100, color='red', ls=':', lw=1.2, alpha=0.4)
ax_apu.set_xticks(x4)
ax_apu.set_xticklabels([f'APU {a}' for a in range(4)], fontsize=11)
ax_apu.set_ylim(30, 110)
style_ax(ax_apu, ylabel='% of APU peak (5.3 TB/s)', title='Dot per APU — SPX Suffers Most')
ax_apu.legend(fontsize=9)

fig.suptitle('The Dot Reduction Penalty', fontsize=14, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.93])
savefig(fig, 'h2h_04_dot_penalty.png')
