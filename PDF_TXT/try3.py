from bs4 import BeautifulSoup
from nature_parser import get_title, get_doi, get_from_springerapi, get_authors_and_affiliations, get_references, get_content, get_title_2
from functions import pdf2html
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

sample = "./SAMPLE/NCLIMATE/s41558-022-01592-2_Why_Residual_Emissions_Matter_Right_Now_.pdf"

is_open_access = False
print(sample)
Faults = 0
# Parse to html
html = pdf2html(target=sample)

if not html:
    Faults += 1
    # continue

# Create soup object
soup = BeautifulSoup(html, 'html.parser')

# Extract data
title = get_title(soup)
if len(title) == 0:
    warning_message = f"Title isn't extracted correctly. -> Implies different paper structure!"
    logging.warning(warning_message)
    Faults += 1
    is_open_access = True
    # continue
if is_open_access:
    title = get_title_2(soup)

print(title)
doi = get_doi(soup)
print(doi)
if len(doi) == 0:
    warning_message = f"DOI isn't extracted correctly. -> Implies different paper structure! Skipping paper!"
    logging.warning(warning_message)
    Faults += 1
    # continue
authors_and_affiliations, affiliations = get_authors_and_affiliations(soup)
# print(affiliations)

authors, journal, date, subjects, abstract = get_from_springerapi(doi[0]) # Sa meta/v2 je bilo moguće dohvatiti i disciplines
# print(authors)
# print(journal)
# print(date)
# print(subjects)
# print(abstract[:100])
references = get_references(soup)
# print(references[:5])
content = get_content(soup)
# print(content[:100])

# Create a dictionary with the paper's data
paper_data = {
    "Title": title,
    "Authors_and_Affiliations": authors_and_affiliations,
    "Affiliations": affiliations,
    "DOI": doi,
    "Authors": authors,
    "Journal": journal,
    "Date": date,
    "Subjects": subjects,
    "Abstract": abstract,
    "References": references,
    "Content": content
}

# Append the dictionary to the list
# data_list.append(paper_data)