"""
This script processes and visualizes Named Entity Recognition (NER) data from a pickled DataFrame. It performs the following tasks:

1. **Load Data**: Reads a pickled NER DataFrame (`file`).
2. **Entity-Tag Counts**: Groups the data by 'Entity' and 'Tag' to count occurrences, saving the result to a pickle file.
3. **Top Entity-Tag Combinations**: Visualizes the top N entity-tag combinations as a bar chart.
4. **Entity Counts**: Counts occurrences of each entity and saves the result.
5. **Top Entities**: Visualizes the top N entities as a bar chart.

Dependencies: `pandas` and `matplotlib`.

Make sure the file path is correct, and the script will generate and save output pickle files.
"""


import pandas as pd
from matplotlib import pyplot as plt
from random import shuffle

colors = ["#09bdfc", "#90ee90", "#ffd700", "#daa520"]
file = "10ksample_ner.pickle"
df_ner = pd.read_pickle(file)

print(df_ner.keys())

entity_tag_counts = df_ner.groupby(['Entity', 'Tag']).size().reset_index(name='Count')
print(entity_tag_counts)
entity_tag_counts.to_pickle("{}_entity_tag_counts.pickle".format(file.split("_")[0]))

top_n = 20

# Get the top N entity-tag combinations and their counts
shuffle(colors)
top_entity_tag_combinations = entity_tag_counts.nlargest(top_n, 'Count')
top_entity_tag_combinations['Entity-Tag'] = top_entity_tag_combinations['Entity'] + ' - ' + top_entity_tag_combinations['Tag']
print(top_entity_tag_combinations.keys())
# Plot the bar chart
# plt.figure(figsize=(12, 8))
top_entity_tag_combinations.plot(kind='bar', x='Entity-Tag', y='Count', color=colors[1])
plt.title('Top {} Entity-Tag Combinations'.format(top_n))
plt.xlabel('Entity-Tag')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.tight_layout()
plt.show()

entity_counts = df_ner['Entity'].value_counts()
entity_counts.to_pickle("{}_entity_counts.pickle".format(file.split("_")[0]))
print(entity_counts)

# Number of top entities to display

top_n = 20

# Get the top N entities and their counts
shuffle(colors)
top_entities = entity_counts.head(top_n)

# Plot the bar chart
plt.figure(figsize=(10, 6))
top_entities.plot(kind='bar', color=colors[2])
plt.title('Top {} Entities'.format(top_n))
plt.xlabel('Entity')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.tight_layout()
plt.show()

