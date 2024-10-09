"""Script to see statistics regarding nouns and pos"""

import pandas as pd
from matplotlib import pyplot as plt
from random import shuffle
import numpy as np

file = "10ksample_pos.pickle"
df_pos = pd.read_pickle(file)
N = 20

# colors = ['#E69F00', '#56B4E9', '#009E73', '#F0E442', '#0072B2', '#D55E00', '#CC79A7']
colors = ["#09bdfc", "#90ee90", "#ffd700", "#daa520"]

# Explode the 'Nouns' column to have one row per noun
exploded_df = df_pos.explode('Nouns')
exploded_df['Nouns'] = exploded_df['Nouns'].apply(lambda x: x.lower() if isinstance(x, str) else x)
# print(exploded_df.keys())
# print(exploded_df.Nouns)
exploded_df = exploded_df[exploded_df['Nouns'].str.len()>2]
# print(exploded_df.keys())
# print(exploded_df.Nouns)

# Calculate the overall count of each noun
overall_noun_counts = exploded_df['Nouns'].value_counts()

# Create a DataFrame from the counts
overall_noun_counts_df = pd.DataFrame({
    'Noun': overall_noun_counts.index,
    'Count': overall_noun_counts.values
})

# Sort the DataFrame by count in descending order
overall_noun_counts_df = overall_noun_counts_df.sort_values(by='Count', ascending=False)

# Display the DataFrame
overall_noun_counts_df.to_pickle("{}_overall_noun_counts.pickle".format(file.split("_")[0]))
print(overall_noun_counts_df)

#### PLOT HERE
# Plot the top N nouns by count
top_n = N  # Change this value to plot a different number of top nouns
plt.figure(figsize=(10, 12))
plt.barh(overall_noun_counts_df['Noun'][:top_n], overall_noun_counts_df['Count'][:top_n], color=colors[0])
# plt.xticks(rotation=45, ha='right')
plt.gca().invert_yaxis()  # invert y-axis
plt.xlabel('Count')
plt.ylabel('Noun')
plt.title(f'Top {top_n} nouns phrases by count')
plt.show()

# Add a column for the number of words in each noun
overall_noun_counts_df['NumWords'] = overall_noun_counts_df['Noun'].apply(lambda x: len(x.split()))

# Group by the number of words and sum the counts for each group
grouped_noun_counts = overall_noun_counts_df.groupby('NumWords')['Count'].sum().reset_index()

# Sort the DataFrame by the number of words
grouped_noun_counts = grouped_noun_counts.sort_values(by='NumWords')

# Display the grouped DataFrame
grouped_noun_counts.to_pickle("{}_grouped_noun_counts.pickle".format(file.split("_")[0]))
print(grouped_noun_counts)

#### PLOT HERE
# Plot the noun counts by the number of words
plt.figure(figsize=(10, 6))
plt.bar(grouped_noun_counts['NumWords'], grouped_noun_counts['Count'], color=colors[3])
plt.xlabel('Number of Words in Noun')
plt.ylabel('Total Count')
plt.title('Noun Counts Grouped by Number of Words')
plt.show()

# Add a column for the number of words in each noun
overall_noun_counts_df['NumWords'] = overall_noun_counts_df['Noun'].apply(lambda x: len(x.split()))

# Sort the DataFrame by the number of words and count in descending order
overall_noun_counts_df = overall_noun_counts_df.sort_values(by=['NumWords', 'Count'], ascending=[True, False])

# Display the DataFrame
overall_noun_counts_df.to_pickle("{}_grouped_overall_noun_counts.pickle".format(file.split("_")[0]))
print(overall_noun_counts_df)

#### PLOT HERE

top_n_per_wordcount = N
unique_word_counts = overall_noun_counts_df['NumWords'].unique()

for word_count in unique_word_counts:
    if word_count > 12:
        continue
    top_n_words = overall_noun_counts_df[overall_noun_counts_df['NumWords'] == word_count][:top_n_per_wordcount]
    shuffle(colors)
    plt.figure(figsize=(10, 12))
    plt.barh(top_n_words['Noun'], top_n_words['Count'], color=colors[1])
    plt.title(f'Top {top_n_per_wordcount} noun phrases with ({word_count} words)')
    plt.gca().invert_yaxis()  # invert y-axis
    plt.xlabel('Count')
    plt.ylabel('Noun')
    # plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()

    # print(f"Top {top_n_per_wordcount} noun phrases with ({word_count} words):")
    # for index, row in top_n_words.iterrows():
    #     print(f"{row['Noun']}\t{row['Count']:,}")
    # print()



#### Complex plot
# top_n = 10  # Number of top nouns
# bottom_n = 10  # Number of bottom nouns
# middle_n = 10  # Number of middle nouns
# mean_n = 10

# # Calculate mean count
# mean_count = overall_noun_counts_df['Count'].mean()
# median_count = overall_noun_counts_df['Count'].median()

# # Select top, bottom, and middle nouns
# top_nouns = overall_noun_counts_df['Noun'][:top_n]
# bottom_nouns = overall_noun_counts_df['Noun'][-bottom_n:]
# #middle_nouns = overall_noun_counts_df['Noun'][len(overall_noun_counts_df) // 2 - middle_n // 2:len(overall_noun_counts_df) // 2 + middle_n // 2]
# # middle_nouns = overall_noun_counts_df.iloc[(overall_noun_counts_df['Count'] - mean_count).abs().argsort()[:middle_n]]['Noun']
# middle_nouns = overall_noun_counts_df.iloc[(overall_noun_counts_df['Count'] - median_count).abs().argsort()[:middle_n]]['Noun']
# mean_nouns = overall_noun_counts_df.iloc[(overall_noun_counts_df['Count'] - mean_count).abs().argsort()[:mean_n]]['Noun']
# # Colors
# top_color = '#0072B2'  # Color for top segment
# middle_color = '#009E73'  # Color for middle segment
# mean_color = '#F0E442'
# bottom_color = '#D55E00'  # Color for bottom segment

# colors = [top_color] * top_n + [middle_color] * middle_n + [mean_color] * mean_n + [bottom_color] * bottom_n

# # Concatenate the selected nouns
# selected_nouns = pd.concat([top_nouns, middle_nouns, mean_nouns, bottom_nouns])

# plt.figure(figsize=(8, 10))
# plt.barh(selected_nouns, overall_noun_counts_df['Count'][selected_nouns.index], color=colors)
# plt.gca().invert_yaxis()  # invert y-axis
# plt.xscale('log')  # apply logarithmic scale to x-axis
# plt.xlabel('Count')
# plt.ylabel('Noun')
# plt.title(f'Selected Nouns by Count')
# plt.show()

