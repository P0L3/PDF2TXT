"""
Nature html parsing
"""
from bs4 import BeautifulSoup
from nature_parser import get_title, get_doi, get_from_springerapi, get_authors_and_affiliations, get_references, get_content
from functions import pdf2html
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

DIR = "./SAMPLE/NCLIMATE/"

# Initialize an empty DataFrame
# columns = [
#     "Title", "Authors_and_Affiliations", "Affiliations", "DOI",
#     "Authors", "Journal", "Date", "Subjects", "Abstract", "References", "Content"
# ]
# df = pd.DataFrame(columns=columns)
# Initialize an empty list to store dictionaries
data_list = []
Faults = 0
samples = listdir(DIR)
for sample in tqdm(samples):
    print(sample)
    # Parse to html
    html = pdf2html(target=DIR+sample)

    if not html:
        Faults += 1
        continue

    # Create soup object
    soup = BeautifulSoup(html, 'html.parser')

    # Extract data
    title = get_title(soup)
    print(title)
    if len(title) == 0:
        warning_message = f"Title isn't extracted correctly. -> Implies different paper structure!"
        logging.warning(warning_message)
        Faults += 1
        continue

    doi = get_doi(soup)
    print(doi)
    if len(doi) == 0:
        warning_message = f"DOI isn't extracted correctly. -> Implies different paper structure! Skipping paper!"
        logging.warning(warning_message)
        Faults += 1
        continue
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
    data_list.append(paper_data)

# Create the DataFrame from the list of dictionaries
df = pd.DataFrame(data_list)

df.to_pickle("test.pickle")
print(Faults)
