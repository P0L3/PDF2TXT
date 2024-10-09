"""Script to see statistics regarding verbs and pos"""

import pandas as pd
from matplotlib import pyplot as plt
from random import shuffle

file = "10ksample_pos.pickle"
df_pos = pd.read_pickle(file)

colors = ["#09bdfc", "#90ee90", "#ffd700", "#daa520"]
shuffle(colors)
N = 20

# Explode the 'Verbs' column to have one row per verb
exploded_df = df_pos.explode('Verbs')
exploded_df['Verbs'] = exploded_df['Verbs'].apply(lambda x: x.lower() if isinstance(x, str) else x)
# Calculate the overall count of each verb
overall_verb_counts = exploded_df['Verbs'].value_counts()

# Create a DataFrame from the counts
overall_verb_counts_df = pd.DataFrame({
    'Verb': overall_verb_counts.index,
    'Count': overall_verb_counts.values
})

# Sort the DataFrame by count in descending order
overall_verb_counts_df = overall_verb_counts_df.sort_values(by='Count', ascending=False)

# Display the DataFrame
overall_verb_counts_df.to_pickle("{}_overall_verb_counts.pickle".format(file.split("_")[0]))
print(overall_verb_counts_df)

#### PLOT HERE
# Plot the top N verbs by count
top_n = N  # Change this value to plot a different number of top verbs
plt.figure(figsize=(10, 6))
plt.bar(overall_verb_counts_df['Verb'][:top_n], overall_verb_counts_df['Count'][:top_n], color=colors[0])
plt.xticks(rotation=45, ha='right')
plt.xlabel('Verb')
plt.ylabel('Count')
plt.title(f'Top {top_n} Verbs by Count')
plt.show()


# Add a column for the number of words in each verb
overall_verb_counts_df['NumWords'] = overall_verb_counts_df['Verb'].apply(lambda x: len(x.split()))

# Group by the number of words and sum the counts for each group
grouped_verb_counts = overall_verb_counts_df.groupby('NumWords')['Count'].sum().reset_index()

# Sort the DataFrame by the number of words
grouped_verb_counts = grouped_verb_counts.sort_values(by='NumWords')

# Display the grouped DataFrame
grouped_verb_counts.to_pickle("{}_grouped_verb_counts.pickle".format(file.split("_")[0]))
print(grouped_verb_counts)

#### PLOT HERE
# Plot the verb counts by the number of words
plt.figure(figsize=(10, 6))
plt.bar(grouped_verb_counts['NumWords'], grouped_verb_counts['Count'], color=colors[2])
plt.xlabel('Number of Words in Verb')
plt.ylabel('Total Count')
plt.title('Verb Counts Grouped by Number of Words')
plt.show()



# Sort the DataFrame by the number of words and count in descending order
overall_verb_counts_df = overall_verb_counts_df.sort_values(by=['NumWords', 'Count'], ascending=[True, False])

# Display the DataFrame
overall_verb_counts_df.to_pickle("{}_grouped_overall_verb_counts.pickle".format(file.split("_")[0]))
print(overall_verb_counts_df)

#### PLOT HERE

top_n_per_wordcount = N
unique_word_counts = overall_verb_counts_df['NumWords'].unique()

for word_count in unique_word_counts:
    shuffle(colors)
    if word_count > 12:
        continue
    top_n_verbs = overall_verb_counts_df[overall_verb_counts_df['NumWords'] == word_count][:top_n_per_wordcount]
    
    # print(f"Top {top_n_per_wordcount} noun phrases with ({word_count} words):")
    # for index, row in top_n_verbs.iterrows():
    #     print(f"{row['Verb']} \t {row['Count']} ")
    # print()

    plt.figure(figsize=(10, 6))
    plt.bar(top_n_verbs['Verb'], top_n_verbs['Count'], color=colors[1])
    plt.title(f'Top {top_n_per_wordcount} Verbs ({word_count} words)')
    plt.xlabel('Verb')
    plt.ylabel('Count')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.show()