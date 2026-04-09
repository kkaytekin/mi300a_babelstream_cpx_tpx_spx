"""Head-to-head plot 3: Per-APU Triad — consistency across APUs.
Shows CPX delivers uniform ~4.1 TB/s per APU; others are lower.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _common import *

cpx_apu = apu_totals(CPX_H2H, CPX_APU_MAP)
tpx_apu = apu_totals(TPX_H2H, TPX_APU_MAP)
spx_apu = apu_totals(SPX_H2H, SPX_APU_MAP)

triad_idx = 3

fig, (ax_abs, ax_pct) = plt.subplots(1, 2, figsize=(12, 5))

x = np.arange(4)
w = 0.25

# Absolute per-APU Triad
for i, (mode, apu_dict) in enumerate([('CPX', cpx_apu), ('TPX', tpx_apu), ('SPX', spx_apu)]):
    vals = [apu_dict[a][triad_idx] / MB_TO_TB for a in range(4)]
    ax_abs.bar(x + (i - 1) * w, vals, w, color=MODE_COLORS[mode],
               edgecolor='white', linewidth=0.5, label=mode, zorder=3)

ax_abs.axhline(THEO_APU, color='red', ls=':', lw=1.2, alpha=0.5,
               label=f'APU peak: {THEO_APU} TB/s')
ax_abs.set_xticks(x)
ax_abs.set_xticklabels([f'APU {a}' for a in range(4)], fontsize=11)
ax_abs.set_ylim(0, THEO_APU * 1.15)
style_ax(ax_abs, ylabel='TB/s (per APU)', title='Triad per APU — Absolute')
ax_abs.legend(fontsize=9)

# % of peak per APU
for i, (mode, apu_dict) in enumerate([('CPX', cpx_apu), ('TPX', tpx_apu), ('SPX', spx_apu)]):
    pcts = [apu_dict[a][triad_idx] / MB_TO_TB / THEO_APU * 100 for a in range(4)]
    ax_pct.bar(x + (i - 1) * w, pcts, w, color=MODE_COLORS[mode],
               edgecolor='white', linewidth=0.5, label=mode, zorder=3)

ax_pct.axhline(100, color='red', ls=':', lw=1.2, alpha=0.4)
ax_pct.set_xticks(x)
ax_pct.set_xticklabels([f'APU {a}' for a in range(4)], fontsize=11)
ax_pct.set_ylim(40, 110)
style_ax(ax_pct, ylabel='% of APU peak (5.3 TB/s)', title='Triad per APU — % of Peak')
ax_pct.legend(fontsize=9)

fig.suptitle('Per-APU Triad Consistency',
             fontsize=14, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.93])
savefig(fig, 'h2h_03_per_apu_triad.png')
