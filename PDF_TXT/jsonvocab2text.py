""" Script to transfer json style vocabs to pure txt """

import json

DIR = "./RESULTS/VOCABS/clivocab_climateroberta.json"

with open(DIR, 'r') as f:
    json = json.load(f)
try:
    vocab = json['model']['vocab'].keys()
except TypeError:
    vocab = json.keys()
print("Total vocab: ", len(vocab))

print("Saving to txt ...")

with open(DIR.replace("json", "txt"), 'x') as txtf:
    for token in vocab:
        txtf.write(token+"\n")

print("Done ...")
