from os import listdir
from tqdm import tqdm
import pandas as pd

tests = [test for test in listdir() if test.endswith(".pickle") and test.startswith("test") and not "mdpi" in test]

counter = 0
for t in tqdm(tests):
    df_temp = pd.read_pickle(f"./{t}")
    
    for content, title in zip(df_temp["Content"], df_temp["Title"]):
        if "ﬂ" in content:
            print(t, 10*"-", title)
            print(content)
            counter += 1
            if counter > 19:
                break