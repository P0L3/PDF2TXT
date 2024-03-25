"""
Nature html parsing
"""
from bs4 import BeautifulSoup
from parser_pdf import *
from functions import pdf2html
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

import argparse
from time import time
from random import randint

## Multprocessing add-on
def list_of_strings(arg):
    return arg.split('žž')
def number(arg):
    return arg
parser = argparse.ArgumentParser()
parser.add_argument("--str-list", type=list_of_strings)
args = parser.parse_args()
samples = args.str_list
multi_flag = True # Flag to see if script is run on multiprocessing manner
##

DIR = "./FULL_DATA/NPJCLIAC/"

##
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filename="_".join(DIR.split("/")),
    filemode='w',
    ) # Adds time to warning output

doctype1_1 = {
    "get_title": ["font-family: AdvOTa20b42a7; font-size:19px"],
    "get_doi_regex": ["font-family: AdvMyriad_R; font-size:8px"],
    "get_authors_and_affiliations_au": ["font-family: AdvTT6780a46b; font-size:8px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: AdvTT6780a46b; font-size:5px"],   # Number
    "get_authors_and_affiliations_af": ["font-family: AdvOT46dcae81; font-size:6px"],       # Affiliation text
    "get_references": [
        "font-family: AdvOT65f8a23b.I; font-size:6px",
        "font-family: AdvOT46dcae81; font-size:6px",
        "font-family: fb; font-size:6px"
    ],
    "get_content": ["(font-family: AdvOT46dcae81; font-size:8px|font-family: fb; font-size:8px)"] # Regex content
}

doctype2_1 = {
    "get_title": ["font-family: AdvTTe45e47d2; font-size:24px"],
    "get_doi_regex": ["font-family: AdvTTe45e47d2; font-size:7px"],
    "get_authors_and_affiliations_au": ["font-family: AdvTTb5929f4c; font-size:11px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: AdvTTb5929f4c; font-size:7px"],  # Number
    "get_authors_and_affiliations_af": ["font-family: AdvTTb5929f4c; font-size:7px"],  # Affiliation text
    "get_references": [
        "font-family: AdvTTb5929f4c; font-size:7px",
        "font-family: 20; font-size:7px"
    ],
    "get_content": ["(font-family: AdvTT86d47313; font-size:9px|font-family: 20; font-size:9px|font-family: fb; font-size:9px)"]
}

doctype3_1 = {
    "get_title": ["font-family: MyriadPro-Regular; font-size:24px"],
    "get_doi_regex": ["font-family: MyriadPro-Regular; font-size:8px"],
    "get_authors_and_affiliations_au": ["font-family: MyriadPro-Light; font-size:11px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: MyriadPro-Light; font-size:7px"],  # Number
    "get_authors_and_affiliations_af": ["font-family: MyriadPro-Light; font-size:7px"],  # Affiliation text
    "get_references": [
        "font-family: MyriadPro-Light; font-size:7px",
        "font-family: MTSY; font-size:7px"
    ],
    "get_content": ["font-family: WarnockPro-Regular; font-size:9px"]
}
# List of style samples to try for processing
styles = [doctype1_1, doctype2_1, doctype3_1]

data_list = []
Faults = 0
Faulty_samples = []
Styleless_samples = []

if not samples:
    samples = listdir(DIR) 
    multi_flag = False
# samples = ["s44168-023-00063-4_Corporate_Motivations_And_Co-Benefit_Valuation_In_Private_Climate_Finance_Investments_Through_Voluntary_Carbon_Markets_.pdf"]
# samples = listdir(DIR)
for sample in samples:
    s = 0
    # print(20*"-")
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

    if check_if_ium(soup):
        warning_message = f"HTML isn't parsed correctly due to incomplite unicode mappings."
        logging.warning(warning_message)
        Faulty_samples.append(sample)
        continue

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

        if len(title[0]) > 190:
            warning_message = "Title too long. -> Implies different paper structure! -> Trying style number: {}".format(s+1)
            logging.warning(warning_message)
            title[0] = ""
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
        # print(doi)
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
                    # print(doi)
                    break
    
    if s >= 0 and s < len(styles):
        style = styles[s]
        authors_and_affiliations, affiliations = get_authors_and_affiliations(soup, style["get_authors_and_affiliations_au"], style["get_authors_and_affiliations_nu"], style["get_authors_and_affiliations_af"])
        # print(affiliations)

        authors, journal, date, subjects, abstract = get_from_springerapi(doi[0]) # Sa meta/v2 je bilo moguće dohvatiti i disciplines
        if authors == "no_authors":
            warning_message = "DOI isn't extracted correctly. -> Implies wrong regex pattern, trying other options if available ..."
            logging.warning(warning_message)
            if "get_doi_regex_r" in style.keys():
                for regex in style["get_doi_regex_r"]:
                    doi = get_doi_regex(soup, style["get_doi_regex"], regex)
                    if doi[0] != "no_doi":
                        # print(doi)
                        break
            if doi[0].endswith("."): # Hot fix if doi ends with . 
                doi[0] = doi[0][:-1]
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
        # print(content)

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
            "Content": content,
            "Keywords": "no_keywords",
            "Style": s,
        }

        # Append the dictionary to the list
        data_list.append(paper_data)

    else:
        paper_data = {
            "Title": title,
            "Authors_and_Affiliations": "no_auth_and_affil",
            "Affiliations": "no_affil",
            "DOI": doi,
            "Authors": "no_authors",
            "Journal": "no_journal",
            "Date": "no_date",
            "Subjects": "no_subjects",
            "Abstract": "no_abstract",
            "References": "no_references",
            "Content": "no_content",
            "Keywords": "no_keywords",
            "Style": s,
        }
        Styleless_samples.append(sample)


# Create the DataFrame from the list of dictionaries
print(Styleless_samples)
print(Faulty_samples)

##
t = round(time(), 1) # Timestamp when multiprocessing
n = randint(1, 10) # For fragments of dataframes
df = pd.DataFrame(data_list)
if multi_flag:
    df.to_pickle(f"./RESULTS/NPJCLIAC/npjcliac_({t})_({n}).pickle")
else:
    df.to_pickle("./PARS_OUT/test_npjcliac.pickle")
print(Faults)
##