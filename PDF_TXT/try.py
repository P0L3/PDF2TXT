"""
SpringerNatrue tryout
"""

import pandas as pd 

df = pd.read_pickle("test.pickle")

# print(df.info())
# lengths = df["Content"].apply(lambda x: len(str(x)))
# print(lengths)

for title in df.Title:
    print(title)