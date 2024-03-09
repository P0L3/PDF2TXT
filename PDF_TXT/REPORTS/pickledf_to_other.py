import pandas as pd 
from os import listdir
from tqdm import tqdm

j = "unnamed"

files = [f for f in listdir() if f.startswith(j)]
print(files)
MAX_SHEET_LEN = 1000000


for file in tqdm(files):
    
    df = pd.read_pickle(file)

    if df.shape[0] > MAX_SHEET_LEN:
        for i in range(0, (df.shape[0]//MAX_SHEET_LEN)+1):
            if i+1 == df.shape[0]//MAX_SHEET_LEN + 1:
                df.iloc[i*MAX_SHEET_LEN:].to_excel("./XL/{}_{}.xlsx".format(file.split(".")[0], i))
            else:
                df.iloc[i*MAX_SHEET_LEN:(i+1)*MAX_SHEET_LEN].to_excel("./XL/{}_{}.xlsx".format(file.split(".")[0], i))
    else: 
        df.to_excel("./XL/{}.xlsx".format(file.split(".")[0]))
