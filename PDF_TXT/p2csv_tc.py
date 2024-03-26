"""
Script to prepair the data for further preprocessing, created CSV version of the whole data and CSV of title-content pairs
"""

import pandas as pd 

DIR = "./RESULTS/ED4RE_2503/DEDUPLICATED/ED4RE_2603.pickle"

df = pd.read_pickle(DIR)
df.reset_index(inplace=True)
# df = df.head(10)

print("Converting to csv ...")
df.to_csv(DIR.replace("pickle", "csv"))

print("Title content pairs to csv ...")
df[["Title", "Content"]].to_csv(DIR.replace(".pickle", "_tc.csv"))

# print("Title content pairs to xml ...")
# df[["Title", "Content"]].to_xml(DIR.replace(".pickle", "_tc.xml"))

# print("Title content pairs to json ...")
# df[["Title", "Content"]].to_json(DIR.replace(".pickle", "_tc.json"))

