import re
import pandas as pd 
from parser_pdf import char_number2words_pages
import numpy as np

df = pd.read_pickle("PARS_OUT/test_climd.pickle")

i = np.random.randint(0, len(df))

print(df["Title"][i])
print(20*"--")
print(df["Abstract"][i])
print(df["Content"][i])
print(20*"--")
print(df["Authors"][i])
print(df["References"][i])