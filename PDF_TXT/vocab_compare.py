""" Script to check vocabulary overlaps """
import re

from supervenn import supervenn
import matplotlib.pyplot as plt

from os import listdir

from itertools import combinations
from operator import itemgetter

def regex_cnt(string, pattern):
    return len(re.findall(pattern, string))

def load_vocab_txt(dir):

    # Load from file
    with open(dir, 'r') as fvocab:
        vocab = fvocab.readlines()

    # Possible special tokens - update if needed
    special = ["##", "Ġ"]

    # Check which special token it is on half the data
    check = " ".join(vocab[:len(vocab)//2])

    for s in special:
        if regex_cnt(check, s) > 1000:
            special_token = s
            break
    print(special_token)

    # Replace with "##" special token
    if special_token != "##":
        for i in range(0, len(vocab)):
            vocab[i] = vocab[i].replace(special_token, "##")
            vocab[i] = vocab[i].replace("\n", "")  
    else:
        for i in range(0, len(vocab)):
            vocab[i] = vocab[i].replace("\n", "")  

    # Clean special tokens [CLS]...
    vocab = [v for v in vocab if type(re.match(r"[\<\[][\w\\\/]+[\>\]]", v)) == type(None)]

    # Return the set
    return set(vocab)

def sub_lists(my_list):
    subs = []  # Create an empty list 'subs' to store the sublists

    # Iterate through the range of numbers from 0 to the length of 'my_list' + 1
    for i in range(0, len(my_list) + 1):
        # Use the 'combinations' function to generate all combinations of 'my_list' of length 'i'
        temp = [list(x) for x in combinations(my_list, i)]

        # Check if 'temp' contains any elements; if so, extend the 'subs' list with the generated sublists
        if len(temp) > 0:
            subs.extend(temp)

    return subs  # Return the list of generated sublists


DIR = "./RESULTS/VOCABS/"

files = listdir(DIR)
# vocabs = [f for f in files if f.endswith(".txt")]
vocabs = ["CliReBERT.txt", "SciBERT.txt", "BioBERT.txt", "BERT.txt"]
list_of_vocabs = []
for v in vocabs:
    list_of_vocabs.append(load_vocab_txt(DIR+v))

labels = [l.replace(".txt", "") for l in vocabs]
# exit()
# vocab1 = load_vocab_txt(DIR1)
# vocab2 = load_vocab_txt(DIR2)


index_combinations = sub_lists(range(0, len(list_of_vocabs)))
print(index_combinations)

for comb in index_combinations:
    if len(comb) > 1:
        labels_temp = itemgetter(*comb)(labels)
        vocab_list_temp = itemgetter(*comb)(list_of_vocabs)

        if len(comb) > 2 and len(comb) <= 4:
            supervenn(vocab_list_temp, labels_temp, widths_minmax_ratio=0.1)
        elif len(comb) > 4: 
            supervenn(vocab_list_temp, labels_temp, widths_minmax_ratio=0.1, rotate_col_annotations=True, col_annotations_area_height=1.2)
        else:
            supervenn(vocab_list_temp, labels_temp)

        filename = "_".join(labels_temp)
        # plt.title("Supervenn: {}".format(labels_temp))
        plt.tight_layout()
        figure = plt.gcf() # get current figure
        figure.set_size_inches(16, 9)
        plt.savefig(f"./REPORTS/IMAGES/VENN/{filename}", dpi=500)
        plt.clf()

# print(vocab1.intersection(vocab2))
# exit()
# supervenn(list_of_vocabs[1:5], labels[1:5], min_width_for_annotation=1000, chunks_ordering='occurrence')
# plt.show()

