"""
Science (ehs) html parsing
"""

from bs4 import BeautifulSoup
from parser import get_title, get_doi, get_from_springerapi, get_authors_and_affiliations, get_references, get_content, get_doi_regex
from functions import pdf2html
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

DIR = "./SAMPLE/EHS/"

doctype1 = [ 
    "font-size:18px", # get_title
    "font-family: BentonSansCond-Regular; font-size:8px", # get_doi_regex
    "font-family: Whitney-Semibold; font-size:12px", "font-family: Whitney-Semibold; font-size:6px", "font-family: Whitney-Book; font-size:8px", # get_authors_and_affiliations (author, affiliation, affiliation text)
    "font-family: MinionPro-Regular; font-size:7px", "font-family: MinionPro-RegularItalic; font-size:7px", # get_references
    "font-family: MinionPro-Regular\d*; font-size:9px" # get_content
]

doctype2 = [
    "font-family: Harding-Bold; font-size:26px", # get_title
    "font-family: GraphikNaturel-Medium2; font-size:8px", # get_doi
    "font-family: GraphikNaturel-Semibold; font-size:9px", "font-family: GraphikNaturel-Semibold; font-size:5px", "font-family: GraphikNaturel-Regular; font-size:7px", # get_authors_and_affiliations (author, affiliation, affiliation text)
    "font-family: GraphikNaturel-Regular; font-size:8px", "font-family: GraphikNaturel-RegularItalic; font-size:8px", # get_references (multiple styles (normal, italic))
    "font-family: HardingText-Regular; font-size:8px" # get_content
]

# List of style samples to try for processing
styles = [doctype1, doctype2]

data_list = []
Faults = 0
Faulty_samples = []
Styleless_samples = []

# samples = listdir(DIR)
samples = ["ehs.0072.pdf"]
for sample in tqdm(samples):
    s = 0
    print(20*"-")
    print(sample)

    # Parse to html
    html = pdf2html(target=DIR+sample)

    if not html:
        Faults += 1
        warning_message = f"HTML isn't parsed correctly -> Implies invalid pdf structure!"
        logging.warning(warning_message)
        Faulty_samples.append(sample)
        continue

    # Create soup object
    soup = BeautifulSoup(html, 'html.parser')

    # Extract title data
    title = []
    while len(title) == 0:
        try:
            style = styles[s]
        except:
            warning_message = "Title isn't extracted correctly. No more styles to try ..."
            logging.warning(warning_message)
            title = ["no_title"]
            s = 0
            break
        # 0 - title
        # 1 - doi
        # 2, 3, 4 - auth and affil
        # 5, 6 - ref
        # 7 - content

        title = get_title(soup, style[0])
        print(title)
        if len(title) == 0:
            warning_message = "Title isn't extracted correctly. -> Implies different paper structure! -> Trying style number: {}".format(s+1)
            logging.warning(warning_message)
            Faults += 1
            s += 1
            
    # Extract doi data
    doi = []
    while len(doi) == 0:
        try:
            style = styles[s]
        except:
            warning_message = "DOI isn't extracted correctly. No more styles to try ..."
            logging.warning(warning_message)
            title = ["no_doi"]
            s = -1
            break

        doi = get_doi_regex(soup, style[1])
        print(doi)
        if len(doi) == 0:
            warning_message = "DOI isn't extracted correctly. -> Implies different paper structure! Skipping paper! Trying style number: {}".format(s+1)
            logging.warning(warning_message)
            Faults += 1
            s += 1
    
    if s >= 0 and s < len(styles):
        style = styles[s]
        authors_and_affiliations, affiliations = get_authors_and_affiliations(soup, style[2:5])
        # print(affiliations)
        authors, journal, date, subjects, abstract = get_from_springerapi(doi[0]) # Sa meta/v2 je bilo moguće dohvatiti i disciplines
        # print(authors)
        # print(journal)
        # print(date)
        # print(subjects)
        # print(abstract[:100])
        references = get_references(soup, style[5:7])
        # print(references[:5])
        content = get_content(soup, style[7])
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

    else:
        paper_data = {
            "Title": title,
            "Authors_and_Affiliations": "None",
            "Affiliations": "None",
            "DOI": doi,
            "Authors": "None",
            "Journal": "None",
            "Date": "None",
            "Subjects": "None",
            "Abstract": "None",
            "References": "None",
            "Content": "None"
        }
        Styleless_samples.append(sample)

# Create the DataFrame from the list of dictionaries
print(Styleless_samples)
print(Faulty_samples)
df = pd.DataFrame(data_list)
df.to_pickle("test.pickle")
print(Faults)