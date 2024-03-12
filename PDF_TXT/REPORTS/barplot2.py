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
        
        ax.bar(x[-1], data[i][-1], color=['#f4f1bb'], hatch='\\')
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels[i])
        ax.set_title(titles[i])
        ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))
        
        i = 2
        x = np.arange(len(data[i]))
        bars2 = ax.bar(x, data[i], color=['#9bc1bc', '#9bc1bc'], hatch="/")
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
        t2rr = [(10, 10), (100, 89), (1000, 751), (10000, 4753), (100000, 25176), (1000000, 138506), (5529110, 480114)]
        ax.set_title("Number of unique relations vs number of triples")
        ax.set_xlabel("X Axis Label")
        ax.set_ylabel("Y Axis Label") 
        
        ax.plot(range(len(t2rr)), [i[0] for i in t2rr], color='#ed6a5a', label="Number of Triples")
        ax.plot(range(len(t2rr)), [i[1] for i in t2rr], color='#9bc1bc', label="Number of Unique Relations")
        
        # ax.set_yticks(range(len(t2rr)))
        # ax.set_yticklabels([i[0] for i in t2rr])

        y_ticks = [i[0] for i in t2rr]
        ax.set_yticks(y_ticks)
        ax.set_yticklabels(y_ticks)        
        ax.set_xticks(range(len(t2rr)))
        ax.set_xticklabels([i[1] for i in t2rr])
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
plt.show()

