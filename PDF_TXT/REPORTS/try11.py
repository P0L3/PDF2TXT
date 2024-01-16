import pandas as pd
from matplotlib import pyplot as plt

df_ner = pd.read_pickle("ehs_ner.pickle")

print(df_ner.keys())

entity_tag_counts = df_ner.groupby(['Entity', 'Tag']).size().reset_index(name='Count')
print(entity_tag_counts)


top_n = 50

# Get the top N entity-tag combinations and their counts
top_entity_tag_combinations = entity_tag_counts.nlargest(top_n, 'Count')
top_entity_tag_combinations['Entity-Tag'] = top_entity_tag_combinations['Entity'] + ' - ' + top_entity_tag_combinations['Tag']
print(top_entity_tag_combinations.keys())
# Plot the bar chart
# plt.figure(figsize=(12, 8))
top_entity_tag_combinations.plot(kind='bar', x='Entity-Tag', y='Count', color='skyblue')
plt.title('Top {} Entity-Tag Combinations'.format(top_n))
plt.xlabel('Entity-Tag')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.tight_layout()
plt.show()

entity_counts = df_ner['Entity'].value_counts()
print(entity_counts)

# Number of top entities to display

top_n = 50

# Get the top N entities and their counts
top_entities = entity_counts.head(top_n)

# Plot the bar chart
plt.figure(figsize=(10, 6))
top_entities.plot(kind='bar', color='skyblue')
plt.title('Top {} Entities'.format(top_n))
plt.xlabel('Entity')
plt.ylabel('Count')
plt.xticks(rotation=45, ha='right')  # Rotate x-axis labels for better visibility
plt.tight_layout()
plt.show()

