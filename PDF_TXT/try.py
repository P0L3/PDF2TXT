"""
SpringerNatrue tryout
"""
import re
import pandas as pd 

df = pd.read_pickle("test_gcb.pickle")
# for i, r in enumerate(df["References"][0]):
#     print(i, "   ", r)
    

# for column in df.keys():
#     print(df["{}".format(column)][0])
    # print(df["".format(column)][0])
# lengths = df["Content"].apply(lambda x: len(str(x)))
# print(lengths)
print(df.keys())
for title in df.Title:
    print(title)
print(30*"-")
for author in df.Authors_and_Affiliations:
    print(author)
print(30*"-")
for aff in df.Affiliations:
    print(aff)
print(30*"-")
for keywords in df.Keywords:
    print(keywords)
print(30*"-")
for content in df.Content:
    print(content)
for ref in df.References:
    print(len(ref))
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