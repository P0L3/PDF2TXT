""" Script for concatenation of the dataframes """
import pandas as pd
import pickle
from os import listdir
from time import time

DIR = "./RESULTS/ED4RE_2503/DEDUPLICATED" # Change directory to where the pickled dataframes are

files = listdir(DIR)

# Loading
print(f"Merging {len(files)} files.")
dfs = []
for f in files:
    # with open(DIR+"/"+f, 'rb') as file:
    #     dfs.append(pickle.load(file))
    try:
        dfs.append(pd.read_pickle(DIR+"/"+f))
    except UnicodeDecodeError:
        with open(DIR+"/"+f, 'rb') as file:
            print(f"Exception occured for {f}.")
            dfs.append(pickle.load(file))
    except pickle.UnpicklingError:
        with open(DIR+"/"+f, 'rb') as file:
            print(f"Exception occured for {f}.")
            dfs.append(pickle.load(file))

# Merge
merged_df = pd.concat(dfs)

# Save
output_file = DIR+"/"+files[0].split("_")[0]+"_full_{}.pickle".format(time())

with open(output_file, 'wb') as f:
    pickle.dump(merged_df, f)

# Output
print(f"Merge complete! Located in \"{output_file}\"")


