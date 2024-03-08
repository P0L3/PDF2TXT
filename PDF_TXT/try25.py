"""Test parquet"""

import pandas as pd

df = pd.read_parquet("./OLD/wiki/test-00000-of-00001.parquet")

for text in df["text"].head():
    print(len(text))
    print(text)