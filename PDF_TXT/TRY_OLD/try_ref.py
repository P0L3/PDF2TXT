"""
References titles check
"""

from os import listdir
from functions import pdf2html
from bs4 import BeautifulSoup
import re
import logging
from tqdm import tqdm
from functions import check_if_ium

DIR = "./SAMPLE/GCB/"
# samples = listdir(DIR) 
samples = ["Global Change Biology - 2015 - Wang - Carbon accumulation and sequestration of lakes in China during the Holocene(1).pdf", "Global Change Biology - 2011 - Garcia - Exploring consensus in 21st century projections of climatically suitable areas for(1).pdf", "Global Change Biology - 2008 - Houghton - The spatial distribution of forest biomass in the Brazilian Amazon a comparison(1).pdf", "Global Change Biology - 2023 - Sun - Machine learning for accelerating process‐based computation of land biogeochemical(1).pdf"
]
trouble_1 = []
trouble_2 = []
invalid = []
for sample in tqdm(samples):
    
    print(10*"---")
    print(sample)

    html = pdf2html(target=DIR+sample)
    soup = BeautifulSoup(html, 'html.parser')
    counter = 0

    if check_if_ium(soup):
        warning_message = f"File with invalid unicode mappings!"
        logging.warning(warning_message)
        invalid.append(sample)
        continue

    elem = soup.find("div")

    # last_elem = soup.find_all('div')[-1]
    # print(last_elem)
    while type(elem) != type(None):
        if re.search("^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n+", elem.text):   
            print(elem.text)
            counter += 1
        elem = elem.find_next()

    if counter > 2:
        warning_message = f"Found multiple references titles"
        logging.warning(warning_message)
        trouble_1.append(sample)
    elif counter < 2:
        warning_message = f"Found inssuficient number of titles"
        logging.warning(warning_message)
        trouble_2.append(sample)

    print(10*"---")

print("PDFs with multiple references: ")
for t in trouble_1:
    print(t)

print("PDF with references not found: ")
for t in trouble_2:
    print(t)

print("PDF with invalid mappings: ")
for t in invalid:
    print(t)

