"""
SpringerNatrue tryout
"""
import re
import pandas as pd 

df = pd.read_pickle("test_nature.pickle")


print(df["Authors_and_Affiliations"])
# lengths = df["Content"].apply(lambda x: len(str(x)))
# print(lengths)

# for title in df.Title:
#     print(title)

# a = []
# for i in range(len(lengths)):
#     # print(lengths[i])
#     # print(df["Authors"][i])

#     if df["Authors"][i] == "no_authors":
#         a.append([lengths[i], df["Title"][i], df["DOI"][i]])

# for f in a:
#     print(f)

# string = "font-family: GraphikNaturel-Semibold; font-size:9px"
# print(re.findall(r"font-size:(\d+px)", string))