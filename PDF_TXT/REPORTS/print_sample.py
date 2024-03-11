import pandas as pd 
from os import listdir
from tqdm import tqdm
 
pd.options.display.max_columns = None
pd.options.display.max_rows = None

DIR = "./EXAMPLES/"

files = listdir()

pickles = [f for f in files if f.endswith(".pickle")]
print(pickles)
with open(DIR+"print", "x") as f:
    for p in tqdm(pickles):
        df = pd.read_pickle(p)
        try:
            f.write("\n---------------------------------------------------\n")
            f.write(p)
            f.write("\n")
            f.write(str(df.head(10)))
        except:
            pass
        
