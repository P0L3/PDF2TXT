from matplotlib import pyplot as plt
import numpy as np


# Generating random data for the bar plots
np.random.seed(0)


data = [
    [2406799, 875841],
    [6.735, 8.709],
    [0.744, 2.045],
    [5529110, 480114]
]

labels = [
    ["POS", "NER"],
    ["POS", "NER"],
    ["Average number of\n entites per sentence", "Average number of\n entites per sentence"],
    ["Number of triples", "Number of unique verbs"]
]

titles = [
    "Total Sentences", 
    "Average number of\n noun phrases\n per sentence", 
    "Average number of\n entites per sentence",
    "Number of unique verbs\n vs number of triples"
]

# Generating x values for the bars
x = np.arange(len(labels[0]))

# Creating the subplots
fig, axs = plt.subplots(2, 2, figsize=(10, 8))

# Flatten the axs array to loop over the subplots
axs = axs.flatten()

# Loop over each subplot and plot the data
for i, ax in enumerate(axs):
    ax.bar(x, data[i], color=['#1f77b4', '#ff7f0e'])
    ax.set_xticks(x)
    ax.set_xticklabels(labels[i])
    ax.set_title(titles[i])
    ax.set_yticks(np.linspace(0, max(data[i][0], data[i][1]), 10))

# Adjust layout and display the plots
plt.tight_layout()
plt.show()

