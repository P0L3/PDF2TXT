"""
Tryout for general view of a pickle dataset
"""
import re
import pandas as pd 
from parser_pdf import char_number2words_pages

df = pd.read_pickle("test_ngeo.pickle")
# for i, r in enumerate(df["References"][0]):
#     print(i, "   ", r)
# df = df[df["Title"] == "The Control of Plant and Soil Hydraulics on the Interannual Variability of Plant Carbon Uptake Over the Central US"]
# print(df)
# for column in df.keys():
#     print(df["{}".format(column)][0])
    # print(df["".format(column)][0])
# lengths = df["Content"].apply(lambda x: len(str(x)))
# print(lengths)
print(df.keys())

print("Title:")
print(30*"-")
for title in df.Title:
    print(title)
print(30*"-")
print(30*"-")
print("DOI:")
print(30*"-")
for doi in df.DOI:
    print(doi)
print(30*"-")
print(30*"-")
print("Authors:")
print(30*"-")
for author in df.Authors:
    print(author)
print(30*"-")
print(30*"-")
print("Affiliations:")
print(30*"-")
for aff in df.Affiliations:
    print(len(aff))
print(30*"-")
print(30*"-")
# print("Keywords:")
# print(30*"-")
# for keywords in df.Keywords:
#     print(keywords)
print(30*"-")
print(30*"-")
print("Abstract:")
print(30*"-")
for abstract in df.Abstract:
    print(len(abstract))
print(30*"-")
print(30*"-")
print("Content:")
print(30*"-")
for content, title, doi in zip(df.Content, df.Title, df.DOI):
    print(len(content))
    if not char_number2words_pages(len(content), 8) or len(content) > 60000:
        print(title)
        print(doi)
        # print(content)
        # exit()
    # print(content)
    # exit()
print(30*"-")
print(30*"-")
print("References:")
print(30*"-")
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