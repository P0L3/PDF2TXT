import pandas as pd

df = pd.read_pickle("unnamed.pickle_entity_tag_counts.pickle")

print(df.info())

# Assuming your DataFrame is named df
top_entities_per_tag = df.groupby('Tag').apply(lambda x: x.nlargest(30, 'Count')).reset_index(drop=True)

# Display the result
print(top_entities_per_tag)


for index, row in top_entities_per_tag.iterrows():
    print(row['Entity'], '\t', row['Count'], '\t', row['Tag'])