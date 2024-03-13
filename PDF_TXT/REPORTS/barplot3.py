from matplotlib import pyplot as plt
import numpy as np
from random import shuffle


# Generating random data for the bar plots
np.random.seed(0)

colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']

data = [
    [16209808, 875841, 5934949],
    [3727803, 475841, 486632],
    [5529110, 486632],
    [6.735, 8.709, 2.466],
    [0.744, 2.045],
    [5529110, 480114]
]

labels = [
    ["Detected noun phrases", "Detected named entities", "Detected verb phrases"],
    ["Noun phrases / \nEntities\n(P)", "Noun phrases / \nEntities\n(E)", "Verbs\n(P)"],
    ["Total triples", "Unique verb phrases"],
    ["Number of triples", "Number of unique verbs"]
]

titles = [
    "Number of sentences", 
    "Average occurance per sentence\nAveraged by (P/E)", 
    "-",
    "Number of possible triples & \nnumber of unique verbs"
]



# Creating the subplots
fig, axs = plt.subplots(1, 2, figsize=(10, 8))#, dpi=1000)

# Flatten the axs array to loop over the subplots
axs = axs.flatten()

# Loop over each subplot and plot the data
for i, ax in enumerate(axs):
    shuffle(colors)
    # Generating x values for the bars
    
    if i == 0: # First plot - Total sentences
        n_values = len(data[i])
        x = np.arange(n_values)
        bars = ax.bar(x, data[i], color=colors[:n_values])
        bars[0].set_label("Total number")
        # ax.axhline(y=2406637, color='#f4f1bb', linewidth=2)
        ax.set_xticks(x)
        ax.set_xticklabels(labels[i])
        ax.set_title(titles[i])
        ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))
        
        for bar in bars:
            height = bar.get_height()
            if height >= 1000:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:,}", ha='center', va='bottom')
            else:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}", ha='center', va='bottom')
        #shuffle(colors)
        i = 1
        bars2 = ax.bar(x, data[i], color=colors[:n_values], hatch='..')
        bars2[0].set_label("Unique")
        # ax.axhline(y=2406637, color='#f4f1bb', linewidth=2)
        # ax.set_xticks(x)
        # ax.set_xticklabels(labels[i])
        # ax.set_title(titles[i])
        # ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))
        
        for bar in bars2:
            height = bar.get_height()
            if height >= 1000:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:,}", ha='center', va='bottom')
            else:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}", ha='center', va='bottom')
        i = 0
        ax.legend()
                
                
    if i == 1: # Secound plot - Average number of things
        i = 2
        n_values = len(data[i])
        x = np.arange(n_values)
        bars = ax.bar(x, data[i], color=colors[:n_values])
        bars[0].set_label("Total triples")
        ax.bar(x[-1], data[i][-1], color=colors[3], hatch='**', label="Verb Unique verb phrases")
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels[i])
        ax.set_title(titles[i])
        ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))
        
        # i = 3
        # # x = np.arange(len(data[i]))
        # bars2 = ax.bar(x, data[i], color=['#9bc1bc', '#9bc1bc'], hatch="/")
        # bars2[0].set_label("Entities")
        # # ax.set_xticks(x)
        # # ax.set_xticklabels(labels[i])
        # # ax.set_title(titles[i])
        # # ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))
        # for bar in bars2:
        #     height = bar.get_height()
        #     if height >= 1000:
        #         ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:,}", ha='center', va='bottom')
        #     else:
        #         ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}", ha='center', va='bottom')
        
        for bar in bars:
            height = bar.get_height()
            if height >= 1000:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:,}", ha='center', va='bottom')
            else:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}", ha='center', va='bottom')
        i = 1     
        ax.legend()

       
    
plt.tight_layout()
# plt.savefig('./IMAGES/10ksample_stats_3.png', dpi=300)
plt.show()

