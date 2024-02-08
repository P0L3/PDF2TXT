"""Playing with pos results"""

import pandas as pd

df = pd.read_pickle("ehs_pos.pickle")

# print(df[["Sentence", "Nouns", "Verbs"]])

for sen, nou, ver in zip(df["Sentence"], df["Nouns"], df["Verbs"]):
    print(20*"-")
    print(sen)
    print(nou)
    print(ver)
    