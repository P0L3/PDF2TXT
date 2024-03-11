
import pandas as pd
from tqdm import tqdm
import numpy as np

df = pd.read_pickle("full_poss.pickle")

# print(df[["Nouns", "Verbs"]].head())

import re
import os


def construct_triples(sentence, verbs):
    # Create a pattern to match all verbs in the sentence
    try:
        verb_pattern = re.compile(r'\b(?:' + '|'.join(verbs) + r')\b')
    except:
        print("Bad evrb_pattern, skipping ...")
        return [(sentence, " ".join(verbs))]
    # Split the sentence by each verb occurrence
    segments = verb_pattern.split(sentence)
    # Remove empty segments
    # segments = [seg.strip() for seg in segments if seg.strip()]

    triples = []
    for i in range(len(segments) - 1):
        try:
            if segments[i].strip() == "" or segments[i+1].strip() == "":
                pass
            else:
                triples.append((sentence, segments[i].strip(), verbs[i], segments[i+1].strip()))
        except:
            pass

    return triples

triples_all = []
rows =  len(df)
print("Total number of sentences: ", rows)

numsent = []
numuverbs = []

i = 0
for index, row in tqdm(df.iterrows()):
    sentence = row["Sentence"]
    nouns = row["Nouns"]
    verbs = row["Verbs"]
    triples = construct_triples(sentence, verbs)
    # print(sentence)
    # for triple in triples:
    #     print(triple)
    # print(3*"------------")
    triples_all.extend(triples)

    # numsent.append(len(triples_all))
    # numuverbs.append(len(set(s[1] for s in triples_all)))

    # i += 1
    # if i > 100:
    #     break
    
# print(triples_all)
df = pd.DataFrame(triples_all, columns=['Sentence', 'Head', 'Relation', 'Tail'])
print(df)
df.to_csv("triples_full.csv")
df.to_pickle("triples_full.pickle")
# print(numsent, numuverbs)
# for triple in triples_all:
#     print(triple)

exit()
import matplotlib.pyplot as plt
# Assuming you have numsent and numuverbs lists

# Plotting numsent
plt.plot(range(len(numsent)), numsent, label='Number of Triples')

# Plotting numuverbs
plt.plot(range(len(numuverbs)), numuverbs, label='Number of Unique Verbs')

# Adding labels and legend
plt.xlabel('Sentence Index')
plt.ylabel('Count')
plt.title('Number of Triples and Unique Verbs per Sentence')
plt.legend()

# Display the plot
plt.show()
