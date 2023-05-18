from cycler import cycler
import seaborn as sns
import matplotlib.pyplot as plt

colors = ['#2E75B6', '#763870', '#C8191A', '#101073', '#6A7A94', '#66968C', '#385765']
line_cycler   = (cycler(color=colors) +
                 cycler(linestyle=['-', '-', '-', '-', '-', '-', '-']))


sns.set(rc={'font.size': 20,
            'legend.fontsize': 20,
            'axes.titlesize': 25,
            'axes.labelsize': 25,
            'axes.titleweight': 'bold',
            'lines.linewidth': 3,
            'xtick.labelsize': 20,
            'ytick.labelsize': 20,
            'axes.prop_cycle': line_cycler})