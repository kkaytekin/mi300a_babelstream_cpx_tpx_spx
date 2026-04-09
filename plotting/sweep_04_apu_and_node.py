"""Sweep plot 4: Per-APU + whole-node Triad — where modes diverge.
Small per-XCD differences compound at aggregate scale.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _common import *

fig, (ax_apu, ax_node) = plt.subplots(1, 2, figsize=(14, 5))

configs = [
    ('CPX', 'cpx', CPX_APU_MAP),
    ('TPX', 'tpx', TPX_APU_MAP),
    ('SPX', 'spx', SPX_APU_MAP),
]

# Compute common x-axis: per-XCD buffer × 6 = per-APU buffer
cpx_df = load_sweep('cpx')
exps = sorted(cpx_df['exp'].unique())
xcd_buf = np.array([cpx_df[cpx_df.exp == e]['arraysize_elements'].iloc[0] * 8 / 1e6 for e in exps])
apu_buf = xcd_buf * 6

for mode, key, apu_map in configs:
    df = load_sweep(key)

    # Per-APU stats
    apu_means, apu_mins, apu_maxs = [], [], []
    for e in exps:
        rows = df[df.exp == e]
        apu_bws = [rows[rows.device.isin(apu_map[a])]['Triad_MBs'].sum() / MB_TO_TB
                    for a in range(4)]
        apu_means.append(np.mean(apu_bws))
        apu_mins.append(np.min(apu_bws))
        apu_maxs.append(np.max(apu_bws))
    apu_means = np.array(apu_means)
    apu_mins = np.array(apu_mins)
    apu_maxs = np.array(apu_maxs)

    ax_apu.plot(apu_buf, apu_means, '-o', color=MODE_COLORS[mode],
                markersize=4, linewidth=2.2, label=mode, zorder=3)
    ax_apu.fill_between(apu_buf, apu_mins, apu_maxs, alpha=0.13, color=MODE_COLORS[mode])

    # Whole-node
    node_bw = np.array([df[df.exp == e]['Triad_MBs'].sum() / MB_TO_TB for e in exps])
    ax_node.plot(xcd_buf, node_bw, '-o', color=MODE_COLORS[mode],
                 markersize=4, linewidth=2.2, label=mode, zorder=3)

# APU panel
ax_apu.axhline(THEO_APU, color='red', ls='--', lw=1.2, alpha=0.7,
               label=f'APU peak ({THEO_APU} TB/s)')
ax_apu.set_xscale('log')
style_ax(ax_apu, ylabel='TB/s (per APU)', xlabel='Per-APU buffer size per array (MB)',
         title='Triad per APU\nModes separate at aggregate scale')
ax_apu.legend(fontsize=9)

# Node panel
ax_node.axhline(THEO_NODE, color='red', ls='--', lw=1.2, alpha=0.7,
                label=f'Node peak ({THEO_NODE:.1f} TB/s)')
ax_node.set_xscale('log')
style_ax(ax_node, ylabel='TB/s (whole node)', xlabel='Per-XCD buffer size per array (MB)',
         title='Triad Whole-Node\nCPX consistently highest')
ax_node.legend(fontsize=9)

fig.suptitle('Aggregate Triad Bandwidth — Where Partition Modes Diverge',
             fontsize=14, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.93])
savefig(fig, 'sweep_04_apu_and_node.png')
