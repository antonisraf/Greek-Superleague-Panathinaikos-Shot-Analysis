import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import os

bg_color = '#1b2721' 
plt.rcParams['text.color'] = 'white'

images = [
    'plots/actual_vs_expected_dark.png',
    'plots/player_efficiency_dark.png',
    'plots/Shot Map.png',
    'plots/goal_density_heatmap.png'
]

titles = [
    'Actual vs Expected Goals', 
    'Player Efficiency (Actual - xG)', 
    'Shot Map Locations', 
    'Goal Density Heatmap'
]


fig = plt.figure(figsize=(22, 14), facecolor=bg_color)


gs = fig.add_gridspec(2, 2, hspace=0.3, wspace=0.15)
axs = gs.subplots()


fig.suptitle('Panathinaikos Shot Analysis - 4/3/26', fontsize=28, fontweight='bold', y=0.97)

for i, ax in enumerate(axs.flat):
    if os.path.exists(images[i]):
        img = mpimg.imread(images[i])
        ax.imshow(img)
       
        ax.set_title(titles[i], fontsize=16, fontweight='bold', pad=20)
    else:
        ax.text(0.5, 0.5, f'Missing:\n{images[i]}', ha='center', va='center', color='red', fontsize=14)
    
    ax.axis('off')


line_style = dict(color='white', linewidth=1, alpha=0.2)
fig.add_artist(plt.Line2D((0.5, 0.5), (0.05, 0.88), **line_style))

fig.add_artist(plt.Line2D((0.05, 0.95), (0.47, 0.47), **line_style))

plt.tight_layout(rect=[0, 0.03, 1, 0.92])

output_path = 'plots/Panathinaikos_Dashboard.png'
plt.savefig(output_path, facecolor=fig.get_facecolor(), dpi=300, bbox_inches='tight')

