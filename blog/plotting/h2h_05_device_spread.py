"""Head-to-head plot 5: Device-level spread — Triad + Dot boxplots.
Shows per-device variance within each mode.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _common import *

triad_idx = 3
dot_idx = 4
modes = ['CPX', 'TPX', 'SPX']

fig, (ax_t, ax_d) = plt.subplots(1, 2, figsize=(12, 5))

for ax, kernel_idx, kernel_name in [(ax_t, triad_idx, 'Triad'), (ax_d, dot_idx, 'Dot')]:
    all_devs = []
    for data_dict in [CPX_H2H, TPX_H2H, SPX_H2H]:
        devs = [data_dict[d][kernel_idx] / MB_TO_TB for d in data_dict]
        all_devs.append(devs)

    n_devs_labels = ['CPX\n(24 dev)', 'TPX\n(12 dev)', 'SPX\n(4 dev)']
    bp = ax.boxplot(all_devs, tick_labels=n_devs_labels,
                    patch_artist=True, widths=0.5)

    for patch, mode in zip(bp['boxes'], modes):
        patch.set_facecolor(MODE_COLORS[mode])
        patch.set_alpha(0.5)

    # Overlay individual points
    rng = np.random.default_rng(42)
    for i, (devs, mode) in enumerate(zip(all_devs, modes)):
        jitter = rng.uniform(-0.12, 0.12, len(devs))
        ax.scatter(np.full(len(devs), i + 1) + jitter, devs,
                   c=MODE_COLORS[mode], s=30, alpha=0.7,
                   edgecolors='white', linewidths=0.5, zorder=4)

    style_ax(ax, ylabel='TB/s (per device)',
             title=f'{kernel_name}: Per-Device Distribution')

fig.suptitle('Device-Level Bandwidth Spread — Triad & Dot',
             fontsize=14, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.93])
savefig(fig, 'h2h_05_device_spread.png')
