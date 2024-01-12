

from os import listdir
from functions import pdf2html
from bs4 import BeautifulSoup
import re
import logging
from tqdm import tqdm

DIR = "./SAMPLE/GCB/"
samples = listdir(DIR) 
trouble = []
for sample in tqdm(samples):
    
    print(10*"---")
    print(sample)

    html = pdf2html(target=DIR+sample)
    soup = BeautifulSoup(html, 'html.parser')
    counter = 0

    elem = soup.find("div")

    while type(elem) != type(None):
        if re.search("^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n*", elem.text):   
            print(elem.text)
            counter += 1
        elem = elem.find_next()

    if counter > 2:
        warning_message = f"Found multiple references titles"
        logging.warning(warning_message)
        trouble.append(sample)

    print(10*"---")

for t in trouble:
    print(t)

