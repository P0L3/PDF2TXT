"""
Check unicode data from text
"""

import unicodedata
import logging
from nltk.corpus import words
import nltk
nltk.download('words')
import re

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

def likely_word(tokenbefore, token, tokenafter):
    print(token)
    if token in words.words():
        return tokenbefore, token, tokenafter
    
    if tokenbefore+token+tokenafter in words.words():
        return "[SEP]", tokenbefore+token+tokenafter, "[SEP]"
    
    if token+tokenafter in words.words():
        return tokenbefore, token+tokenafter, "[SEP]"
    
    if tokenbefore+token in words.words():
        return "[SEP]", tokenbefore+token, tokenafter






tokens = text.split()
for i, word in enumerate(tokens):
    count = 0

    for j, c in enumerate(word):
        if c in ligatures_list and (j == 0 or j == len(word)-1):
            print(i, "\t", tokens[i-1], tokens[i], tokens[i+1])
            count += 1
            print(likely_word(tokens[i-1], re.sub(pattern, lambda m: ligatures_conv.get(m.group(0).upper()), tokens[i], flags=re.IGNORECASE), tokens[i+1]))
    
    if count > 1: # Check if some word containes multiple ligatures
        print(i, "\t", tokens[i-1], tokens[i], tokens[i+1])
        warning_message = f"Multiple ligatures in single word!"
        logging.warning(warning_message)





# https://stackoverflow.com/questions/28339622/is-there-a-corpus-of-english-words-in-nltk
# https://stackoverflow.com/questions/14156473/how-can-i-use-a-dictionary-to-do-multiple-search-and-replace-operations
# https://www.digitalocean.com/community/tutorials/python-add-to-dictionary
# https://www.compart.com/en/unicode/U+FB02
# https://unicode.org/reports/tr15/
# https://docs.python.org/3.8/library/unicodedata.html#unicodedata.unidata_version
# https://superuser.com/questions/669130/double-latin-letters-in-unicode-ligatures
