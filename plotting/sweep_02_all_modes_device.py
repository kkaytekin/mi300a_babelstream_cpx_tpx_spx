"""Sweep plot 2: All three modes per-device, side by side.
Shows the same S-curve at different absolute scales (1, 2, 6 XCDs).
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _common import *

fig, axes = plt.subplots(1, 3, figsize=(16, 5), sharey=False)

configs = [
    ('CPX', 'cpx', 1, THEO_XCD,     '1 XCD per device — 24 devices'),
    ('TPX', 'tpx', 2, THEO_XCD * 2, '2 XCDs per device — 12 devices'),
    ('SPX', 'spx', 6, THEO_APU,     '6 XCDs per device — 4 devices'),
]

for ax, (mode, key, n_xcds, peak, subtitle) in zip(axes, configs):
    df = load_sweep(key)
    exps = sorted(df['exp'].unique())
    buf = np.array([df[df.exp == e]['arraysize_elements'].iloc[0] * 8 / 1e6 for e in exps])

    for op, col in zip(OPS, OP_COLS):
        means = np.array([df[df.exp == e][col].mean() / MB_TO_TB for e in exps])
        ax.plot(buf, means, '-o', color=OP_COLORS[op], markersize=3, linewidth=1.8, label=op, zorder=3)

    # Triad spread
    t_min = np.array([df[df.exp == e]['Triad_MBs'].min() / MB_TO_TB for e in exps])
    t_max = np.array([df[df.exp == e]['Triad_MBs'].max() / MB_TO_TB for e in exps])
    ax.fill_between(buf, t_min, t_max, alpha=0.12, color=MODE_COLORS[mode])

    ax.axhline(peak, color='red', ls='--', lw=1.2, alpha=0.7,
               label=f'Peak {peak:.3f} TB/s')

    # Saturation marker
    t_mean = np.array([df[df.exp == e]['Triad_MBs'].mean() / MB_TO_TB for e in exps])
    sat_idx = int(np.argmax(t_mean >= np.nanmax(t_mean) * 0.90))
    sat_mb = buf[sat_idx]
    ax.axvline(sat_mb, color='steelblue', ls=':', lw=1.3, alpha=0.85,
               label=f'Sat. ~{sat_mb:.0f} MB')

    ax.set_xscale('log')
    style_ax(ax, ylabel='TB/s' if ax == axes[0] else None,
             xlabel='Buffer size per array (MB)',
             title=f'{mode} — {subtitle}')
    ax.legend(fontsize=7, ncol=2, loc='upper left')

fig.suptitle('Per-Device Bandwidth Sweep — All Three Partition Modes',
             fontsize=14, fontweight='bold')
fig.tight_layout(rect=[0, 0, 1, 0.94])
savefig(fig, 'sweep_02_all_modes_device.png')
