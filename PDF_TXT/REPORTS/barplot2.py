from matplotlib import pyplot as plt
import numpy as np


# Generating random data for the bar plots
np.random.seed(0)


# data = [
#     [2406799, 875841],
#     [6.735, 8.709],
#     [0.744, 2.045],
#     [5529110, 480114]
# ]

data = [
    [2406799, 875841],
    [6.735, 8.709, 2.466],
    [0.744, 2.045],
    [5529110, 480114]
]

labels = [
    ["(P) Detected noun phrases /\nverb phrases", "(E) Detected named entities"],
    ["Noun phrases / \nEntities\n(P)", "Noun phrases / \nEntities\n(E)", "Verbs\n(P)"],
    ["Average number of\n entites per sentence", "Average number of\n entites per sentence"],
    ["Number of triples", "Number of unique verbs"]
]

titles = [
    "Number of sentences", 
    "Average occurance per sentence\nAveraged by (P/E)", 
    "-",
    "Number of possible triples & \nnumber of unique verbs"
]



# Creating the subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Flatten the axs array to loop over the subplots
axs = axs.flatten()

# Loop over each subplot and plot the data
for i, ax in enumerate(axs):
    # Generating x values for the bars
    x = np.arange(len(data[i]))
    if i == 0: # First plot - Total sentences
        bars = ax.bar(x, data[i], color=['#ed6a5a', '#9bc1bc'])
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
                
                
    if i == 1: # Secound plot - Average number of things
        bars = ax.bar(x, data[i], color=['#ed6a5a', '#ed6a5a', '#f4f1bb'])
        bars[0].set_label("Noun phrases")
        ax.bar(x[-1], data[i][-1], color=['#f4f1bb'], hatch='\\', label="Verb phrases")
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels[i])
        ax.set_title(titles[i])
        ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))
        
        i = 2
        x = np.arange(len(data[i]))
        bars2 = ax.bar(x, data[i], color=['#9bc1bc', '#9bc1bc'], hatch="/")
        bars2[0].set_label("Entities")
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
        
        for bar in bars:
            height = bar.get_height()
            if height >= 1000:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:,}", ha='center', va='bottom')
            else:
                ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}", ha='center', va='bottom')
        i = 1     
        ax.legend()

       
    if i == 2:
        i = 3
        bars = ax.bar(x, data[i], color=['#ed6a5a', '#9bc1bc'])
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
        i = 2       
                
    if i == 3:
        t2rr = [(10, 9), (20, 20), (30, 29), (40, 37), (50, 47), (60, 54), (70, 66), (80, 78), (90, 83), (100, 91), (200, 167), (300, 241), (400, 328), (500, 405), (600, 459), (700, 517), (800, 590), (900, 667), (1000, 735), (2000, 1301), (3000, 1807), (4000, 2311), (5000, 2706), (6000, 3119), (7000, 3516), (8000, 3920), (9000, 4354), (10000, 4668), (20000, 7796), (30000, 10436), (40000, 12954), (50000, 15396), (60000, 17425), (70000, 19507), (80000, 21457), (90000, 23344), (100000, 25397), (200000, 42254), (300000, 56962), (400000, 70279), (500000, 83139), (600000, 94896), (700000, 105818), (800000, 117751), (900000, 128039), (1000000, 138711), (2000000, 230211), (3000000, 309080), (4000000, 380852), (5000000, 446691), (5529110, 480114)]
        ax.set_title("Number of unique relations vs number of triples")
        ax.set_xlabel("Triples")
        ax.set_ylabel("Y Axis Label") 
        
        ax.plot(range(len(t2rr)), [i[0] for i in t2rr], color='#ed6a5a', label="Number of triples")
        ax.plot(range(len(t2rr)), [i[1] for i in t2rr], color='#9bc1bc', label="Number of unique verb phrases")
        
        # ax.set_yticks(range(len(t2rr)))
        # ax.set_yticklabels([i[0] for i in t2rr])

        y_ticks = [i[0] for i in t2rr if i[0]>999999 or i[0] == 1000 or i[0] == 500000] # [t2rr[i][0] for i in range(0, len(t2rr), 5)] # [i[0] for i in t2rr if i[0]>999999 or i[0] == 1000 or i[0] == 500000]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_ticks)        
        ax.set_xticks(range(0, len(t2rr), 5))
        ax.set_xticklabels([t2rr[i][1] for i in range(0, len(t2rr), 5)])
        ax.legend()
        ##
        # t2rr = [(10, 10), (100, 89), (1000, 751), (10000, 4753), (100000, 25176), (1000000, 138506), (5529110, 480114)]

        # ax.set_title("Number of unique relations vs number of triples")
        # ax.set_xlabel("Number of Triples")
        # ax.set_ylabel("Number of Unique Relations") 

        # ax.plot([i[0] for i in t2rr], [i[1] for i in t2rr], marker='o', linestyle='-', color='#ed6a5a')

                
                
    # bars = ax.bar(x, data[i], color=['#ed6a5a', '#9bc1bc'])
    # ax.set_xticks(x)
    # ax.set_xticklabels(labels[i])
    # ax.set_title(titles[i])
    # ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))
    
    # if i == 1:
    #     i = 2
    #     bars2 = ax.bar(x, data[i], color=['#f4f1bb', '#f4f1bb'])
    #     ax.set_xticks(x)
    #     ax.set_xticklabels(labels[i])
    #     ax.set_title(titles[i])
    #     # ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))
    #     for bar in bars2:
    #         height = bar.get_height()
    #         if height >= 1000:
    #             ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:,}", ha='center', va='bottom')
    #         else:
    #             ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}", ha='center', va='bottom')

    
    # for bar in bars:
    #     height = bar.get_height()
    #     if height >= 1000:
    #         ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:,}", ha='center', va='bottom')
    #     else:
    #         ax.text(bar.get_x() + bar.get_width() / 2, height, f"{height:.2f}", ha='center', va='bottom')

# Adjust layout and display the plots
plt.tight_layout()
plt.savefig('./IMAGES/10ksample_stats.png', dpi=300)
# plt.show()

