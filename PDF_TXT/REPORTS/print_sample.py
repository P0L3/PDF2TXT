import pandas as pd 
from os import listdir, chdir
from tqdm import tqdm
 
pd.options.display.max_columns = None
pd.options.display.max_rows = None

DIR = "/PDF_TXT/REPORTS/EXAMPLES/"
chdir("/PDF_TXT/RESULTS/ED4RE")
files = listdir()

pickles = [f for f in files if f.endswith(".pickle")]
print(pickles)
with open(DIR+"print_ed4re", "x") as f:
    for p in tqdm(pickles):
        df = pd.read_pickle(p)
        try:
            f.write("\n---------------------------------------------------\n")
            f.write(p)
            f.write(df.shape)
            f.write("\n")
            f.write(str(df.head(10)))
        except:
            pass
        
