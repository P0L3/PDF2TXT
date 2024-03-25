"""
Script to detect duplicates in pandas dataframes
"""

import pandas as pd
from os import listdir

DIR = "./RESULTS/ED4RE_2503/"

dfs = listdir(DIR)

for df_name in dfs:
    print(5*"----")
    print("Dataframe name: ", df_name)
    try:
        df = pd.read_pickle(DIR+df_name)
    except:
        print("Dataframe doesn't exist or is not a pickle file ...")
        continue
    
    # Content length
    df["Content_length"] = df["Content"].str.len()
    df["Title"] = df["Title"].apply(lambda x: ' '.join(x))
    nrows = len(df)

   
    duplicate_rows = df[df.duplicated(subset=["Title", "Content_length", "Content"])]
    # print("Columns: ", ", ".join(df.keys().tolist()))
    try:
        df = df.drop_duplicates(subset=["Title", "Content_length"])
    except:
        continue
    nrows_d = len(df)
    # Duplicates
    
    nrows_d_clean = len(duplicate_rows[duplicate_rows["Content"].str.len() > 10]["Title"])
    print("Number of rows:            ", nrows)
    print("Number of duplicates:      ", nrows-nrows_d)
    print("Real number of duplicates: ", nrows_d_clean)
    print(duplicate_rows[duplicate_rows["Content"].str.len() > 10]["Title"])
    
    if nrows_d_clean/nrows > 0.1:
        duplicate_rows[duplicate_rows["Content"].str.len() > 10][["Title", "Content"]].to_csv(DIR+df_name.split(".")[0]+"_duplicate.csv")


