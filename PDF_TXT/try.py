"""
SpringerNatrue tryout
"""
import re
import pandas as pd 

df = pd.read_pickle("test.pickle")

print(df)
lengths = df["Content"].apply(lambda x: len(str(x)))
print(lengths)

# for title in df.Title:
#     print(title)

# string = "font-family: GraphikNaturel-Semibold; font-size:9px"
# print(re.findall(r"font-size:(\d+px)", string))