"""
Tryout for general view of a pickle dataset
"""
import re
import pandas as pd 
from parser_pdf import char_number2words_pages

df = pd.read_pickle("./RESULTS/MDPI/mdpi_full.pickle")
### General dataset info
length = 10000
print("Number of rows: ", len(df))
print("Columns: ", ", ".join(df.keys().tolist()))
zcn = (df['Content'].str.len() <= 0).sum() # Zero content number
lcn = (df['Content'].str.len() <= length).sum() # Length content number
print("Average content length:                ", round(df["Content"].str.len().mean(), 2))
print("Number of empty contents:              ", zcn, " / ", len(df), " => ", round(zcn/len(df), 4)*100, "%")
print("Number of <= {length} length contents: ", lcn, " / ", len(df), " => ", round(lcn/len(df), 4)*100, "%")

print(df.info())
print(df.head())

# for i, r in enumerate(df["References"][0]):
#     print(i, "   ", r)
# df = df[df["Title"] == "The Control of Plant and Soil Hydraulics on the Interannual Variability of Plant Carbon Uptake Over the Central US"]
# print(df)
# for column in df.keys():
#     print(df["{}".format(column)][0])
    # print(df["".format(column)][0])
# lengths = df["Content"].apply(lambda x: len(str(x)))
# print(lengths)


# print("Journal:")
# print(30*"-")
# for journal in df.Journal:
#     print(journal)
    
# print("Date:")
# print(30*"-")
# for date in df.Date:
#     print(date)
    
# print("Subjects:")
# print(30*"-")
# for sub in df.Subjects:
#     print(sub)

# print("Title:")
# print(30*"-")
# for title in df.Title:
#     print(title)
# print(30*"-")
# print(30*"-")
# print("DOI:")
# print(30*"-")
# for doi in df.DOI:
#     print(doi)
# print(30*"-")
# print(30*"-")
# print("Authors:")
# print(30*"-")
# for author, title, doi in zip(df.Authors, df.Title, df.DOI):
#     print(author)
#     if len(author) < 2:
#         print(title)
#         print(doi)
#         print(20*"-")

        

# print(30*"-")
# print(30*"-")
# print("Affiliations:")
# print(30*"-")
# for aff in df.Affiliations:
#     print(len(aff))
# print(30*"-")
# print(30*"-")
# print("Keywords:")
# print(30*"-")
# for keywords in df.Keywords:
#     print(keywords)
# print(30*"-")
# print(30*"-")
# print("Abstract:")
# print(30*"-")
# for abstract, title, doi in zip(df.Abstract, df.Title, df.DOI):
#     if len(abstract) < 1000:
#         print(title)
#         print(doi)
#     else:
#         print(len(abstract))
# print(30*"-")
# print(30*"-")
# print("Content:")
# print(30*"-")
# for content, title, doi in zip(df.Content, df.Title, df.DOI):
#     print(len(content))
    # if not char_number2words_pages(len(content), 4): #or len(content) > 60000:
    #     print(title)
    #     print(doi)
        # print(content)
        # exit()
    # print(content)
#     # exit()
# print(30*"-")
# print(30*"-")
# print("References:")
# print(30*"-")
# for ref in df.References:
#     print(ref)

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