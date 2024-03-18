""" From Pandas dataframe to raw text for tokenizer training """

import pandas as pd 
from sklearn.model_selection import train_test_split
from os import mkdir

DF = "./RESULTS/ED4RE/full.pickle"
df = pd.read_pickle(DF)

texts = df["Content"]

DIR = "./RESULTS/SETS/"
NEW_DIR = DIR + DF.split("/")[-1].replace(".pickle", "")

TRAIN = 0.9955
TEST = 0.0025
VAL = 1 - TEST - TRAIN - 0.0001

train, test = train_test_split(texts, test_size=TEST+VAL, train_size=TRAIN, shuffle=True, random_state=3005)

test, val = train_test_split(test, train_size=0.55, shuffle=True, random_state=3005)

try:
    mkdir(NEW_DIR)
except FileExistsError:
    c = input("Folder already exists, do you with to continue? [y/n]: ")
    if c in 'yY':
        pass
    else:
        exit()

def write_to_text(data, name="unnamed"):
    with open(NEW_DIR + "/" + name + ".raw", "x") as file:
        for line in data:
            file.write(line)

write_to_text(train, name="train")
write_to_text(test, name="test")
write_to_text(val, name="val")