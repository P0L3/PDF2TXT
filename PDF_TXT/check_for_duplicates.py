"""
Script to detect duplicates in pandas dataframes
"""

import pandas as pd
from os import listdir, mkdir
from functions import pandas_dataframe_info
from tqdm import tqdm

DIR = "./RESULTS/ED4RE_2503/"

PER = 0.05
dfs = listdir(DIR)

try:
    mkdir(DIR+"DEDUPLICATED/")
except:
    print("Folder \"DEDUPLICATED\" already exists ...")

for df_name in tqdm(dfs):
    print(5*"----")
    print("Dataframe name: ", df_name)
    try:
        df = pd.read_pickle(DIR+df_name)
    except:
        print("Dataframe doesn't exist or is not a pickle file ...")
        continue
    
    # Content length
    df["Title"] = df["Title"].apply(lambda x: ' '.join(x))
    nrows = len(df)

   
    duplicate_rows = df[df.duplicated(subset=["Title", "Content"])]
    # print("Columns: ", ", ".join(df.keys().tolist()))
    try:
        df = df.drop_duplicates(subset=["Title", "Content"])
    except:
        print("Exception occured during deduplication ...")
        continue
    nrows_d = len(df)
    # Duplicates
    
    nrows_d_clean = len(duplicate_rows[duplicate_rows["Content"].str.len() > 10]["Title"])
    print("Number of rows:            ", nrows)
    print("Number of duplicates:      ", nrows-nrows_d)
    print("Real number of duplicates: ", nrows_d_clean)
    print(duplicate_rows[duplicate_rows["Content"].str.len() > 10]["Title"])
    
    if nrows_d_clean/nrows > PER:
        duplicate_rows[duplicate_rows["Content"].str.len() > 10][["Title", "Content"]].to_csv(DIR+df_name.split(".")[0]+"_duplicate.csv")
        print("Dataframe containes:       ", (nrows_d_clean/nrows)*100, "\% duplicates")

    print("General info: ", "\n", 5*"----")
    pandas_dataframe_info(df)
    print(5*"----")
    print(5*"----")
    print()
    df.to_pickle(DIR+"DEDUPLICATED/"+df_name)

