from matplotlib import pyplot as plt
import numpy as np

data = [
    [2.406799, 6.735, 0.744],
    [0.875841, 8.709, 2.045]
]

scaled_data = [
    2.406799, 0.875841, 5.529110, 0.480114
]

labels = [
    ["Total Sentences", "Total Sentences"],
    ["Average number of\n noun phrases\n per sentence", "Average number of\n noun phrases\n per sentence"],
    ["Average number of\n entites per sentence", "Average number of\n entites per sentence"],
    ["Number of unique verbs\n vs number of triples", "Number of unique verbs\n vs number of triples"]
]

X = np.arange(len(data[0]) + 1)


bar1 = plt.bar(X[:3] + 0.00, data[0], color = '#ed6a5a', width = 0.25)
bar2 = plt.bar(X[:3] + 0.25, data[1], color = '#f4f1bb', width = 0.25, hatch='/')

for bar in bar1:
    xval = bar.get_x() + bar.get_width() / 2
    plt.plot([xval-0.125, -1], [bar.get_height(), bar.get_height()], linestyle='--', color='#9bc1bc', alpha=0.4)
    if bar.get_height() in scaled_data:
        plt.text(xval, bar.get_height(), f"{bar.get_height():.6f}e6", ha='center', va='bottom')
    else:
        plt.text(xval, bar.get_height(), f"{bar.get_height():.2f}", ha='center', va='bottom')

for bar in bar2:
    xval = bar.get_x() + bar.get_width() / 2
    plt.plot([xval-0.125, -1], [bar.get_height(), bar.get_height()], linestyle='--', color='#9bc1bc', alpha=0.4)
    if bar.get_height() in scaled_data:
        plt.text(xval, bar.get_height(), f"{bar.get_height():.6f}e6", ha='center', va='bottom')
    else:
        plt.text(xval, bar.get_height(), f"{bar.get_height():.2f}", ha='center', va='bottom')

bar3 = plt.bar(X[-1] + 0.125, 5.529110, color = '#9bc1bc', width=0.5)
bar3_2 = plt.bar(X[-1] + 0.125, 0.480114, color = '#9bc1bc', width = 0.5, hatch='OO')

for bar in bar3:
    xval = bar.get_x() + bar.get_width() / 2
    plt.plot([xval-0.125, -1], [bar.get_height(), bar.get_height()], linestyle='--', color='#9bc1bc', alpha=0.4)
    if bar.get_height() in scaled_data:
        plt.text(xval, bar.get_height(), f"{bar.get_height():.6f}e6", ha='center', va='bottom')
    else:
        plt.text(xval, bar.get_height(), f"{bar.get_height():.2f}", ha='center', va='bottom')

for bar in bar3_2:
    xval = bar.get_x() + bar.get_width() / 2
    plt.plot([xval-0.125, -1], [bar.get_height(), bar.get_height()], linestyle='--', color='#9bc1bc', alpha=0.4)
    if bar.get_height() in scaled_data:
        plt.text(xval, bar.get_height(), f"{bar.get_height():.6f}e6", ha='center', va='bottom')
    else:
        plt.text(xval, bar.get_height(), f"{bar.get_height():.2f}", ha='center', va='bottom')
# Add labels and title
plt.xticks(X + 0.125, labels=labels)
plt.yticks(np.linspace(0, round(max(max(data[0]), max(data[1])))+1, 40))
plt.title('Statistics for POS and NER Tagging')
plt.xlim([-0.5, 4])
plt.show()

