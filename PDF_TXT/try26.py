import pandas as pd

df = pd.read_pickle("RESULTS/ED4RE_2603_tc_tokenized_remaining_350.pickle")

print(len(df["Sentences"][0]))