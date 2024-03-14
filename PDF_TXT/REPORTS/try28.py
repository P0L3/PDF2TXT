import pandas as pd 

df = pd.read_pickle("full_overall_noun_counts.pickle")

print(df.Count.sum())