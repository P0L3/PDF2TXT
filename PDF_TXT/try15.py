import re
import pandas as pd 
from parser_pdf import char_number2words_pages

df = pd.read_pickle("test_jgra.pickle")
df2 = pd.read_pickle("test2_jgra.pickle")

search = ['Enhanced relationship between the tropical Atlantic SST and the summertime western North Pacic subtropical high after the early 1980s']

for title1, content1, title2, content2 in zip(df["Title"], df["Content"], df2["Title"], df2["Content"]):
    if len(content1)/len(content2) > 1.5:
        print(title2)

    if title2 == search:
        print(title2)
        print(content2)