import pandas as pd
from matplotlib import pyplot as plt

df_pos = pd.read_pickle("ehs_pos.pickle")

# Explode the 'Nouns' column to have one row per noun
exploded_df = df_pos.explode('Nouns')

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
print(overall_noun_counts_df)

#### PLOT HERE
# Plot the top N nouns by count
top_n = 20  # Change this value to plot a different number of top nouns
plt.figure(figsize=(10, 6))
plt.bar(overall_noun_counts_df['Noun'][:top_n], overall_noun_counts_df['Count'][:top_n])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Noun')
plt.ylabel('Count')
plt.title(f'Top {top_n} Nouns by Count')
plt.show()

# Add a column for the number of words in each noun
overall_noun_counts_df['NumWords'] = overall_noun_counts_df['Noun'].apply(lambda x: len(x.split()))

# Group by the number of words and sum the counts for each group
grouped_noun_counts = overall_noun_counts_df.groupby('NumWords')['Count'].sum().reset_index()

# Sort the DataFrame by the number of words
grouped_noun_counts = grouped_noun_counts.sort_values(by='NumWords')

# Display the grouped DataFrame
print(grouped_noun_counts)

#### PLOT HERE
# Plot the noun counts by the number of words
plt.figure(figsize=(10, 6))
plt.bar(grouped_noun_counts['NumWords'], grouped_noun_counts['Count'])
plt.xlabel('Number of Words in Noun')
plt.ylabel('Total Count')
plt.title('Noun Counts Grouped by Number of Words')
plt.show()

# Add a column for the number of words in each noun
overall_noun_counts_df['NumWords'] = overall_noun_counts_df['Noun'].apply(lambda x: len(x.split()))

# Sort the DataFrame by the number of words and count in descending order
overall_noun_counts_df = overall_noun_counts_df.sort_values(by=['NumWords', 'Count'], ascending=[True, False])

# Display the DataFrame
print(overall_noun_counts_df)

#### PLOT HERE
# # Plot the top 20 nouns per word count
# top_n_per_wordcount = 20
# unique_word_counts = overall_noun_counts_df['NumWords'].unique()

# plt.figure(figsize=(14, 8))
# print(unique_word_counts)
# for word_count in unique_word_counts:
#     if word_count > 9:
#         continue
#     top_n_words = overall_noun_counts_df[overall_noun_counts_df['NumWords'] == word_count][:top_n_per_wordcount]
#     plt.bar(top_n_words['Noun'], top_n_words['Count'], label=f'{word_count} words')

# plt.xticks(rotation=45, ha='right')
# plt.xlabel('Noun')
# plt.ylabel('Count')
# plt.title(f'Top {top_n_per_wordcount} Nouns per Word Count')
# plt.legend()
# plt.show()

# Plot the top 20 nouns per word count in separate plots
top_n_per_wordcount = 20
unique_word_counts = overall_noun_counts_df['NumWords'].unique()

for word_count in unique_word_counts:
    if word_count > 12:
        continue
    top_n_words = overall_noun_counts_df[overall_noun_counts_df['NumWords'] == word_count][:top_n_per_wordcount]
    
    plt.figure(figsize=(10, 6))
    plt.bar(top_n_words['Noun'], top_n_words['Count'])
    plt.title(f'Top {top_n_per_wordcount} Nouns ({word_count} words)')
    plt.xlabel('Noun')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()