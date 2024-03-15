from matplotlib import pyplot as plt
import numpy as np
from random import shuffle


# Generating random data for the bar plots
np.random.seed(0)

# colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']

colors = [
    ['#0072B2', '#56B4E9'],
    ['#009E73', '#F0E442']
]

data = [
    [15238265, 1790745],
    [3725121, 313315],
    [5529110, 5934949],
    [5333279, 486632],

    [6.735, 8.709, 2.466],
    [0.744, 2.045],
    [5529110, 480114]
]

labels = [
    ["(a) Detected noun phrases", "(b) Detected named entities"],
    ["Noun phrases / \nEntities\n(P)", "Noun phrases / \nEntities\n(E)", "Verbs\n(P)"],
    ["(a) Possible triples", "(b) Detected verb phrases"],
    ["Number of triples", "Number of unique verbs"]
]

titles = [
    "(1) Number of noun phrases & entites", 
    "Average occurance per sentence\nAveraged by (P/E)", 
    "(2) Number of triples & verb phrases",
    "Number of possible triples & \nnumber of unique verbs"
]



# Creating the subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 8))#, dpi=1000)

# Flatten the axs array to loop over the subplots
axs = axs.flatten()

font_s = 'large'
font_w = 'bold'
font_p_1 = 1.4
font_p_2 = 3.8

# Loop over each subplot and plot the data
for i, ax in enumerate(axs):
    # Generating x values for the bars
    
    if i == 0: # First plot - Total sentences
        n_values = len(data[i])
        x = np.arange(n_values)
        bars = ax.bar(x, data[i], color=colors[i])
        bars[0].set_label("Total number")
        # ax.axhline(y=2406637, color='#f4f1bb', linewidth=2)
        ax.set_xticks(x)
        ax.set_xticklabels(labels[i])
        ax.set_title(titles[i])
        # ax.set_ylim(1.7)
        # ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))
        ax.set_ylim(0, 16500000)
        
        for bar in bars:
            height = bar.get_height()
            if height >= 1000:
                ax.text(bar.get_x() + bar.get_width() / font_p_1, height+200000, f"{height:,}", ha='center', va='bottom', weight=font_w, fontsize=font_s)
            else:
                ax.text(bar.get_x() + bar.get_width() / font_p_1, height, f"{height:.2f}", ha='center', va='bottom', weight=font_w, fontsize=font_s)

        i = 1
        bars2 = ax.bar(x, data[i], color=colors[i-1], hatch='..')
        bars2[0].set_label("Unique")

        
        for bar in bars2:
            height = bar.get_height()
            if height >= 1000:
                ax.text(bar.get_x() + bar.get_width() / font_p_2, height, f"{height:,}", ha='center', va='bottom', weight=font_w, fontsize=font_s)
            else:
                ax.text(bar.get_x() + bar.get_width() / font_p_2, height, f"{height:.2f}", ha='center', va='bottom', weight=font_w, fontsize=font_s)
        i = 0
        
        ax.legend(fontsize=font_s)
                
                
    if i == 1: # Secound plot - Average number of things
        i = 2
        n_values = len(data[i])
        x = np.arange(n_values)
        bars = ax.bar(x, data[i], color=colors[i-1])
        bars[0].set_label("Total number")
        ax.bar(x[-1], data[i][-1], color=colors[1][1])
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels[i])
        ax.set_ylim(0, 16500000)
        ax.set_title(titles[i])
        # ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))

        
        for bar in bars:
            height = bar.get_height()
            if height >= 1000:
                ax.text(bar.get_x() + bar.get_width() / font_p_1, height+200000, f"{height:,}", ha='center', va='bottom', weight=font_w, fontsize=font_s)
            else:
                ax.text(bar.get_x() + bar.get_width() / font_p_1, height, f"{height:.2f}", ha='center', va='bottom', weight=font_w, fontsize=font_s)  

        i = 3
        bars2 = ax.bar(x, data[i], color=colors[i-2], hatch='..')
        bars2[0].set_label("Unique")

        
        for bar in bars2:
            height = bar.get_height()
            if height >= 1000:
                ax.text(bar.get_x() + bar.get_width() / font_p_2, height, f"{height:,}", ha='center', va='bottom', weight=font_w, fontsize=font_s)
            else:
                ax.text(bar.get_x() + bar.get_width() / font_p_2, height, f"{height:.2f}", ha='center', va='bottom', weight=font_w, fontsize=font_s)
        i = 1
        
        ax.legend(fontsize=font_s)
       
    
plt.tight_layout()
plt.savefig('./IMAGES/10ksample_stats_4.png', dpi=300)
plt.show()

