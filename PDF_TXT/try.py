"""
SpringerNatrue tryout
"""
import re
import pandas as pd 

df = pd.read_pickle("test_enerpol.pickle")
# for i, r in enumerate(df["References"][0]):
#     print(i, "   ", r)
    

# for column in df.keys():
#     print(df["{}".format(column)][0])
    # print(df["".format(column)][0])
# lengths = df["Content"].apply(lambda x: len(str(x)))
# print(lengths)

for title in df.Title:
    print(title)
print(30*"-")
for keywords in df.Keywords:
    print(keywords)
for content in df.Content:
    print(len(content))
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