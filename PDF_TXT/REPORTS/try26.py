import pandas as pd
from matplotlib import pyplot as plt


file = "unnamed.pickle"
df_ner = pd.read_pickle(file)
print(df_ner.info())
# # Assuming df is your DataFrame
# # Grouping by 'Tag' and counting occurrences of 'Entity'
# grouped = df_ner.groupby('Tag')['Entity'].count().reset_index()

# # Sorting by the count of occurrences
# sorted_grouped = grouped.sort_values(by='Entity', ascending=False)

# print(sorted_grouped)

grouped = df_ner.groupby(['Tag', 'Entity']).size().reset_index(name='Entity Count')

# Sorting by the count of occurrences
sorted_grouped = grouped.sort_values(by=['Tag', 'Entity Count'], ascending=[True, False])

# print(sorted_grouped)
# TOP = 50
# for tag, data in sorted_grouped.groupby('Tag'):
#     plt.figure(figsize=(10, 6))
#     plt.barh(data['Entity'].head(TOP), data['Entity Count'].head(TOP))
#     plt.xlabel('Entity Count')
#     plt.ylabel('Entity')
#     plt.title(f'Top {TOP} Entities for Tag: {tag}')
#     plt.gca().invert_yaxis()  # Invert y-axis to have the highest count on top
#     plt.show()

def list_to_string(string_in_list):
    return " ".join(string_in_list)

df_ner["String_Title"] = df_ner['Title'].apply(list_to_string)

# Assuming df is your DataFrame
num_unique_titles = df_ner['String_Title'].nunique()
print("Number of unique titles:", num_unique_titles)


sentence_counts = df_ner['Sentence']
print(len(sentence_counts))


# Count the occurrences of each sentence
sentence_counts = df_ner['Sentence'].value_counts()

# Count the occurrences of each count (i.e., number of times a sentence appears)
sentence_occurrence_counts = sentence_counts.value_counts().sort_index()


df_occurance = pd.DataFrame({'Count': sentence_occurrence_counts})
df_occurance = df_occurance.reset_index()
df_occurance.columns = ['Occurrences', 'Frequency']
import seaborn as sns
ax = sns.barplot(data=df_occurance, x='Occurrences', y='Frequency')
ax.set_title('Distribution of Sentence Occurances')
ax.set_ylabel('Number of Unique Sentences')
ax.set_xlabel('Times Each Sentence Appears')
plt.xticks(rotation=90)
plt.gcf().subplots_adjust(bottom=0.6)
plt.show()

import math

# # # Plot the histogram
# # plt.figure(figsize=(16, 10))
# # plt.bar(sentence_occurrence_counts.index, [math.log10(count) for count in sentence_occurrence_counts.values], width=1.5)
# # plt.xlabel('Number of Occurrences')
# # plt.ylabel('Count of Sentences')
# # plt.title('Distribution of Sentence Occurrences')
# # plt.xticks(range(1, sentence_occurrence_counts.index.max() + 1))
# # plt.grid(axis='y', linestyle='--', alpha=0.7)
# # plt.show()
# import numpy as np
# # Define custom tick locations (every multiple of 3 starting from 4)
# tickloc = np.arange(start=4, stop=sentence_occurrence_counts.index.max(), step=3)

# # Plot the histogram
# # plt.figure(figsize=(16, 10))
# # plt.bar(sentence_occurrence_counts.index, [math.log10(count) for count in sentence_occurrence_counts.values], width=1.5)
# # plt.xlabel('Number of Entities')
# # plt.ylabel('Log Count of Sentences')
# # plt.title('Distribution of Entity Frequency')
# # plt.xticks(tickloc) # Use custom tick location array defined above
# # plt.yticks([])      # Hide y-axis ticks to focus on distribution
# # plt.grid(False)     # Remove grid lines
# # plt.margins(x=0.02) # Tighten margins around bars

# # Plot the histogram
# # plt.figure(figsize=(8, 6))
# # plt.bar(sentence_occurrence_counts.index, [math.log10(count) for count in sentence_occurrence_counts.values], width=1.5)
# # plt.xlim(-1, sentence_occurrence_counts.index.max())   # Set x-axis limits to include both ends
# # plt.xlabel('Number of Entities')
# # plt.ylabel('Log Count of Sentences')
# # plt.title('Distribution of Entity Frequency')
# # plt.xticks(([0, sentence_occurrence_counts.index.max()]))    # Display only two xtick labels
# # plt.axvline(x=0, color='k', ls='dotted', lw=1)              # Add vertical dotted line at x=0
# # plt.text(x=-0.9, y=0.5*plt.gca().get_ylim()[1], s="$n$=0", va='center', ha='right')  # 
# plt.figure(figsize=(8, 6))
# plt.bar(sentence_occurrence_counts.index, [math.log10(count) for count in sentence_occurrence_counts.values], width=1.5)
# plt.xlabel('Number of Entities')
# plt.ylabel('Log Count of Sentences')
# plt.title('Distribution of Entity Frequency')
# plt.xscale('symlog')                       # Apply symlog scaling to x-axis
# plt.xticks(([0, sentence_occurrence_counts.index.max()]))    # Display only two xtick labels
# plt.axvline(x=0, color='k', ls='dotted', lw=1)              # Add vertical dotted line at x=0
# plt.text(x=-0.9, y=0.5*plt.gca().get_ylim()[1], s="$n$=0", va='center', ha='right')  # Lab
# plt.show()