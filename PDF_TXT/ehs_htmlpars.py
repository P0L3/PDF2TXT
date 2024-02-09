"""
Science (ehs) html parsing
"""

from bs4 import BeautifulSoup
from parser_pdf import get_title, get_doi, get_from_springerapi, get_authors_and_affiliations, get_references, get_content, get_doi_regex, get_from_doi2bibapi
from functions import pdf2html
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

DIR = "./SAMPLE/EHS/"

doctype1_1 = {
    "get_title": ["font-size:18px"],
    "get_doi_regex": ["font-family: BentonSansCond-Regular; font-size:8px"],
    "get_authors_and_affiliations_au": ["font-family: BentonSansCond-Bold; font-size:12px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: BentonSansCond-Bold; font-size:7px"],   # Number
    "get_authors_and_affiliations_af": ["font-family: BentonSansCond-Regular; font-size:9px"],  # Affiliation text
    "get_references": [
        "font-family: MinionPro-Regular; font-size:9px",
        "font-family: MinionPro-It; font-size:9px"
    ],
    "get_content": ["font-size:10px"]
}

doctype2_1 = {
    "get_title": ["font-family: AdvPSMy-B; font-size:21px"],
    "get_doi_regex": ["font-family: AdvTT6489ba6c; font-size:7px"],
    "get_doi_regex_r": ["doi(\/[\d.\/\w-]+)\/suppinfo"],
    "get_authors_and_affiliations_au": ["font-family: AdvTT3abd98ce.B; font-size:9px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: AdvTT3abd98ce.B; font-size:6px"],   # Number
    "get_authors_and_affiliations_af": ["font-family: AdvTT6489ba6c; font-size:7px"],  # Affiliation text
    "get_references": [
        "font-family: AdvTT6489ba6c; font-size:8px",
        "font-family: AdvTT8b1d421d.I; font-size:8px",
    ],
    "get_content": ["font-family: (AdvTT6489ba6c|AdvTT8b1d421d.I); font-size:9px"]
}

doctype3_1 = {
    "get_title": ["font-size:21px"],
    "get_doi_regex": ["font-family: PalatinoLinotype-Roman; font-size:8px", "font-family: PalatinoLinotype-Roman; font-size:10px"],
    "get_doi_regex_r": ["doi(\/[\d.\/\w-]+)\/suppinfo"],
    "get_authors_and_affiliations_au": ["font-family: PalatinoLinotype-Bold; font-size:10px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: PalatinoLinotype-Bold; font-size:5px"],   # Number
    "get_authors_and_affiliations_af": ["font-family: PalatinoLinotype-Roman; font-size:7px"],  # Affiliation text
    "get_references": [
        "font-family: PalatinoLinotype-Roman; font-size:8px",
        "font-family: GraphikNaturel-RegularItalic; font-size:8px"
    ],
    "get_content": ["font-size:10px"]
}

doctypedef_1 = {
    "get_title" : ["font-family: Myriad-Bold; font-size:21px"],
    "get_doi_regex": ["font-family: Minion-Regular; font-size:9px"],
    "get_authors_and_affiliations_au": ["font-family: PalatinoLinotype-Bold; font-size:10px"]
}

# List of style samples to try for processing
styles = [doctype1_1, doctype2_1, doctype3_1, doctypedef_1]

data_list = []
Faults = 0
Faulty_samples = []
Styleless_samples = []

samples = listdir(DIR)
# samples = ["ehs2.1224.pdf"]
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
    title = [""]
    while len(title[0]) == 0:
        try:
            style = styles[s]
        except:
            warning_message = "Title isn't extracted correctly. No more styles to try ..."
            logging.warning(warning_message)
            title = ["no_title"]
            s = 0
            break

        title = get_title(soup, style["get_title"])
        print(title)
        if len(title[0]) == 0:
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

        doi = get_doi_regex(soup, style["get_doi_regex"])
        print(doi)
        if len(doi) == 0:
            warning_message = "DOI isn't extracted correctly. -> Implies different paper structure! Skipping paper! Trying style number: {}".format(s+1)
            logging.warning(warning_message)
            Faults += 1
            s += 1

    # Try available regex patterns for the style
    if doi[0] == "no_doi":
        warning_message = "DOI isn't extracted correctly. -> Implies wrong regex pattern, trying other options if available ..."
        logging.warning(warning_message)
        if "get_doi_regex_r" in style.keys():
            for regex in style["get_doi_regex_r"]:
                doi = get_doi_regex(soup, style["get_doi_regex"], regex)
                if doi[0] != "no_doi":
                    print(doi)
                    break

    # Get data
    if s >= 0 and s < len(styles):
        style = styles[s]
        authors_and_affiliations, affiliations = get_authors_and_affiliations(soup, style["get_authors_and_affiliations_au"], style["get_authors_and_affiliations_nu"], style["get_authors_and_affiliations_nu"])
        # print(affiliations)
        authors, journal, date, subjects, abstract = get_from_doi2bibapi(doi[0]) # Sa meta/v2 je bilo moguće dohvatiti i disciplines
        # print(authors)
        # print(journal)
        # print(date)
        # print(subjects)
        # print(abstract[:100])
        references = get_references(soup, style["get_references"])
        # print(references[:5])
        content = get_content(soup, style["get_content"])
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
# print(paper_data)
df = pd.DataFrame(data_list)
df.to_pickle("test_ehs.pickle")
print(Faults)