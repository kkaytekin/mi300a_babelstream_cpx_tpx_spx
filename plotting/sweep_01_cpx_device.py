"""Sweep plot 1: CPX per-device bandwidth vs buffer size.
Introduces the S-curve shape, saturation threshold, and all 5 kernels.
"""
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from _common import *

cpx = load_sweep('cpx')
exps = sorted(cpx['exp'].unique())
buf = np.array([cpx[cpx.exp == e]['arraysize_elements'].iloc[0] * 8 / 1e6 for e in exps])

fig, ax = plt.subplots(figsize=(8, 5))

for op, col in zip(OPS, OP_COLS):
    means = np.array([cpx[cpx.exp == e][col].mean() / MB_TO_TB for e in exps])
    ax.plot(buf, means, '-o', color=OP_COLORS[op], markersize=4, linewidth=2, label=op, zorder=3)

# Triad spread (min–max across devices)
t_mean = np.array([cpx[cpx.exp == e]['Triad_MBs'].mean() / MB_TO_TB for e in exps])
t_min  = np.array([cpx[cpx.exp == e]['Triad_MBs'].min()  / MB_TO_TB for e in exps])
t_max  = np.array([cpx[cpx.exp == e]['Triad_MBs'].max()  / MB_TO_TB for e in exps])
ax.fill_between(buf, t_min, t_max, alpha=0.12, color=MODE_COLORS['CPX'], label='Triad device spread')

# Peak line
ax.axhline(THEO_XCD, color='red', ls='--', lw=1.2, alpha=0.7,
           label=f'XCD peak ({THEO_XCD:.3f} TB/s)')

# Saturation marker
thresh = np.nanmax(t_mean) * 0.90
sat_idx = int(np.argmax(t_mean >= thresh))
sat_mb = buf[sat_idx]
ax.axvline(sat_mb, color='steelblue', ls=':', lw=1.3, alpha=0.85,
           label=f'~90% saturation ({sat_mb:.0f} MB)')

ax.set_xscale('log')
style_ax(ax, ylabel='TB/s (per device)', xlabel='Buffer size per array (MB)',
         title='CPX — Per-Device Bandwidth vs Buffer Size\n(1 XCD per device, 24 devices)')
ax.legend(fontsize=8.5, ncol=2, loc='lower right')

fig.tight_layout()
savefig(fig, 'sweep_01_cpx_device.png')
