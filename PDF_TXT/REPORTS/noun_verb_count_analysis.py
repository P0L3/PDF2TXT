import pandas as pd

file = "full_poss.pickle"
df_pos = pd.read_pickle(file)

## Nouns
# Explode the 'Nouns' column to have one row per noun
exploded_df = df_pos.explode('Nouns')

# Lower
exploded_df['Nouns'] = exploded_df['Nouns'].apply(lambda x: x.lower() if isinstance(x, str) else x)

# Calculate the overall count of each noun
overall_noun_counts = exploded_df['Nouns'].value_counts()

# Create a DataFrame from the counts
overall_noun_counts_df = pd.DataFrame({
    'Noun': overall_noun_counts.index,
    'Count': overall_noun_counts.values
})


## Verbs
# Explode the 'Nouns' column to have one row per noun
exploded_df_v = df_pos.explode('Verbs')

# Lower
exploded_df_v['Verbs'] = exploded_df_v['Verbs'].apply(lambda x: x.lower() if isinstance(x, str) else x)

# Calculate the overall count of each noun
overall_verb_counts = exploded_df_v['Verbs'].value_counts()

# Create a DataFrame from the counts
overall_verb_counts_df = pd.DataFrame({
    'Verb': overall_verb_counts.index,
    'Count': overall_verb_counts.values
})


## Nouns
# Sort the DataFrame by count in descending order
overall_noun_counts_df = overall_noun_counts_df.sort_values(by='Count', ascending=False)
df = overall_noun_counts_df

## Verbs
overall_verb_counts_df = overall_verb_counts_df.sort_values(by='Count', ascending=False)
df_v = overall_verb_counts_df

print("Nouns")
print(len(df))
print(df['Count'].sum())
print("Verbs")
print(len(df_v))
print(df_v['Count'].sum())