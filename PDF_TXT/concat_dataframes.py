import pandas as pd
import pickle
from os import listdir

DIR = "./RESULTS/JCLIMATE"

files = listdir(DIR)

# Loading
print(f"Merging {len(files)} files.")
dfs = []
for f in files:
    # with open(DIR+"/"+f, 'rb') as file:
    #     dfs.append(pickle.load(file))
    dfs.append(pd.read_pickle(DIR+"/"+f))

# Merge
merged_df = pd.concat(dfs)

# Save
output_file = DIR+"/"+files[0].split("_")[0]+"_full.pickle"

with open(output_file, 'wb') as f:
    pickle.dump(merged_df, f)

# Output
print(f"Merge complete! Located in \"{output_file}\"")


