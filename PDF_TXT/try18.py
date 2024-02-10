"""
Check unicode data from text
"""

import unicodedata
import logging

import re
from tqdm import tqdm
from functions import *

# import these modules

with open("./test11.txt") as f:
    text = f.read()


# Dictionary
ligatures_dict = []
ligatures_conv = {}
for c in range(0, 0x10FFFF + 1):
    d = unicodedata.normalize('NFKD', chr(c))
    if len(d) > 1 and d.isascii() and d.isalpha():
        # print("U+%04X (%s): %s\n" % (c, chr(c), d))
        ligatures_dict.append({
            "unicode": "U+%04X"%(c),
            "sign": "%s"%(chr(c)),
            "norm": "%s"%(d),
            "%s"%(chr(c)): "%s"%(d)
        })
        ligatures_conv["%s"%(chr(c))] = "%s"%(d)

# List for comparison
ligatures_list = [c["sign"] for c in ligatures_dict]

# Regex
pattern = '|'.join(sorted(re.escape(k) for k in ligatures_conv))
print(pattern)
with open('ligatures_data.py', 'w') as f:
    f.write(f"ligatures_dict = {ligatures_dict}\n")
    f.write(f"ligatures_conv = {ligatures_conv}\n")
    f.write(f"ligatures_list = {ligatures_list}\n")
    f.write(f"pattern = \"{pattern}\"\n")
    

tokens = text.split()
fi_counter_unsolved = []
fi_counter_solved = []


for i, word in enumerate(tokens):
    count = 0

    for j, c in enumerate(word):
        if c in ligatures_list:
            if (j == 0 or j == len(word)-1):
                temp = tokens[i]
                # print(20*"-")
                # print(i, "\t", tokens[i-1], tokens[i], tokens[i+1], end="----")
                count += 1
                tokens[i-1], tokens[i], tokens[i+1], f = likely_word(tokens[i-1], re.sub(pattern, lambda m: ligatures_conv.get(m.group(0)), tokens[i]), tokens[i+1])
                if f == 0:
                    fi_counter_unsolved.append((temp, tokens[i]))
                else:
                    fi_counter_solved.append((temp, tokens[i]))
            else:
                tokens[i] = re.sub(pattern, lambda m: ligatures_conv.get(m.group(0)), tokens[i])
                count += 1
            # print(tokens[i-1], tokens[i], tokens[i+1])
    if count > 1: # Check if some word containes multiple ligatures
        print(i, "\t", tokens[i-1], tokens[i], tokens[i+1])
        warning_message = f"Multiple ligatures in single word!"
        logging.warning(warning_message)

print(" ".join(tokens))

print("Total fi problems: ", len(fi_counter_solved) + len(fi_counter_unsolved))
print("Total fi solved  : ", len(fi_counter_solved))
print(fi_counter_solved)

print("Percentage solved: ", len(fi_counter_solved)/(len(fi_counter_solved) + len(fi_counter_unsolved)))
print(fi_counter_unsolved)



# https://stackoverflow.com/questions/28339622/is-there-a-corpus-of-english-words-in-nltk
# https://stackoverflow.com/questions/14156473/how-can-i-use-a-dictionary-to-do-multiple-search-and-replace-operations
# https://www.digitalocean.com/community/tutorials/python-add-to-dictionary
# https://www.compart.com/en/unicode/U+FB02
# https://unicode.org/reports/tr15/
# https://docs.python.org/3.8/library/unicodedata.html#unicodedata.unidata_version
# https://superuser.com/questions/669130/double-latin-letters-in-unicode-ligatures
