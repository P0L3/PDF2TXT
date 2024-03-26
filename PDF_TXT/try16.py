import re
import pandas as pd 
from parser_pdf import char_number2words_pages
import numpy as np

df = pd.read_pickle("PARS_OUT/test_climd.pickle")
# df2 = pd.read_pickle("PARS_OUT/test_jgra_2.pickle")

df.sort_values(by='Title', ascending=True, inplace=True)
# df2.sort_values(by='Title', ascending=True, inplace=True)

df.reset_index(drop=True, inplace=True)
# df2.reset_index(drop=True, inplace=True)

i = np.random.randint(0, len(df))

print(df["Title"][i])
print(df["DOI"][i])
print(20*"--")
print(df["Abstract"][i])
print(df["Content"][i])
print(20*"--")
print(df["Authors"][i])
print(df["References"][i])


# print(df2["Title"][i])
# print(df2["DOI"][i])
# print(20*"--")
# print(df2["Abstract"][i])
# print(df2["Content"][i])
# print(20*"--")
# print(df2["Authors"][i])
# print(df2["References"][i])