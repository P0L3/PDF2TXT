"""
DOI to bib
"""

import subprocess
import re

DOI = "10.1002/jgrd.50863"
res = subprocess.run(['doi2bib', DOI], capture_output=True)
byte = res.stdout.strip(b"\n")

text = re.sub("[ \n]+", " ", byte.decode("utf-8"))
text = re.sub(" ,", ",", text)
# print(text)

# Define a regular expression pattern to extract key-value pairs
pattern = r'(\w+)\s*=\s*{([^{}]+)}'

# Find all matches of key-value pairs
matches = re.findall(pattern, text)

# Create a dictionary from matches
result = {key: value for key, value in matches}

