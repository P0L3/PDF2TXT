"""
Check unicode data from text
"""

import unicodedata
import logging
from nltk.corpus import words
import nltk
# nltk.download('words')
# nltk.download('wordnet')
import re
from tqdm import tqdm


# import these modules
from nltk.stem import WordNetLemmatizer
 
lemmatizer = WordNetLemmatizer()

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

    temp_token = token
    temp_tokenbefore = tokenbefore
    temp_tokenafter = tokenafter

    # Clean from punctuation and simmilar
    token = re.sub(r"[(),.!?;]+", "", token).lower()
    tokenbefore = re.sub(r"[(),.!?;]+", "", tokenbefore).lower()
    tokenafter = re.sub(r"[(),.!?;]+", "", tokenafter).lower()

    # Deal with concatenated words, such as "age-specific"
    tokenbefore = re.sub(r"\w+-", "", tokenbefore)


    if tokenbefore+token+tokenafter in words.words() or lemmatizer.lemmatize(tokenbefore+token+tokenafter) in words.words() or lemmatizer.lemmatize(tokenbefore+token+tokenafter, pos='v') in words.words():
        return "[SEP]", temp_tokenbefore+temp_token+temp_tokenafter, "[SEP]", 1
    
    elif token+tokenafter in words.words() or lemmatizer.lemmatize(token+tokenafter) in words.words() or lemmatizer.lemmatize(token+tokenafter, pos='v') in words.words():
        return temp_tokenbefore, temp_token+temp_tokenafter, "[SEP]", 1
    
    elif tokenbefore+token in words.words() or lemmatizer.lemmatize(tokenbefore+token) in words.words() or lemmatizer.lemmatize(tokenbefore+token, pos='v') in words.words():
        return "[SEP]", temp_tokenbefore+temp_token, temp_tokenafter, 1
    
    elif token in words.words() in words.words():
        return temp_tokenbefore, temp_token, temp_tokenafter, 1
    
    else:
        if len(temp_token) > 2:
            return temp_tokenbefore, temp_token, temp_tokenafter, 1
        else: 
            # print(temp_tokenbefore, temp_token, temp_tokenafter)
            return temp_tokenbefore, "[SEP]", temp_tokenafter, 0
    

tokens = text.split()
fi_counter = 0
fi_counter_solved = 0

for i, word in enumerate(tokens):
    count = 0

    for j, c in enumerate(word):
        if c in ligatures_list and (j == 0 or j == len(word)-1):
            # print(20*"-")
            # print(i, "\t", tokens[i-1], tokens[i], tokens[i+1], end="----")
            count += 1
            tokens[i-1], tokens[i], tokens[i+1], f = likely_word(tokens[i-1], re.sub(pattern, lambda m: ligatures_conv.get(m.group(0)), tokens[i]), tokens[i+1])
            fi_counter += 1
            fi_counter_solved += f
            # print(tokens[i-1], tokens[i], tokens[i+1])
    if count > 1: # Check if some word containes multiple ligatures
        print(i, "\t", tokens[i-1], tokens[i], tokens[i+1])
        warning_message = f"Multiple ligatures in single word!"
        logging.warning(warning_message)

print(" ".join(tokens))

print("Total fi problems: ", fi_counter)
print("Total fi solved  : ", fi_counter_solved)

print("Percentage solved: ", fi_counter_solved/fi_counter)



# https://stackoverflow.com/questions/28339622/is-there-a-corpus-of-english-words-in-nltk
# https://stackoverflow.com/questions/14156473/how-can-i-use-a-dictionary-to-do-multiple-search-and-replace-operations
# https://www.digitalocean.com/community/tutorials/python-add-to-dictionary
# https://www.compart.com/en/unicode/U+FB02
# https://unicode.org/reports/tr15/
# https://docs.python.org/3.8/library/unicodedata.html#unicodedata.unidata_version
# https://superuser.com/questions/669130/double-latin-letters-in-unicode-ligatures
