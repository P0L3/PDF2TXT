import pandas as pd 
from os import listdir
from tqdm import tqdm

j = "ehs"

files = [f for f in listdir() if f.startswith(j)]
print(files)

for file in tqdm(files):

    df = pd.read_pickle(file)

    df.to_excel("./XL/{}.xlsx".format(file.split(".")[0]))