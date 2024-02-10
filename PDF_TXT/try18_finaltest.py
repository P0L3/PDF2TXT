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

print(fi_cleaner(text))



# https://stackoverflow.com/questions/28339622/is-there-a-corpus-of-english-words-in-nltk
# https://stackoverflow.com/questions/14156473/how-can-i-use-a-dictionary-to-do-multiple-search-and-replace-operations
# https://www.digitalocean.com/community/tutorials/python-add-to-dictionary
# https://www.compart.com/en/unicode/U+FB02
# https://unicode.org/reports/tr15/
# https://docs.python.org/3.8/library/unicodedata.html#unicodedata.unidata_version
# https://superuser.com/questions/669130/double-latin-letters-in-unicode-ligatures
