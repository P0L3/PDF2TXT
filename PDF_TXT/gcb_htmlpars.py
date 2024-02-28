"""
GCB html parsing
"""

from bs4 import BeautifulSoup
from parser_pdf import get_abstract, get_title, get_content, get_doi_regex, get_from_doi2bibapi, get_authors_and_affiliations, get_references_nonumber, get_keywords, char_number2words_pages
from functions import pdf2html, find_custom_element_by_regex, add_custom_tag_after_element, check_if_ium
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
    return arg.split('ž')
def number(arg):
    return arg
parser = argparse.ArgumentParser()
parser.add_argument("--str-list", type=list_of_strings)
args = parser.parse_args()
samples = args.str_list
multi_flag = True # Flag to see if script is run on multiprocessing manner
##

DIR = "./FULL_DATA/GCB/"
##
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filename="_".join(DIR.split("/")),
    filemode='w',
    ) # Adds time to warning output

doctype0_1 = {
    "get_title": ["font-family: AdvPalB; font-size:17px", "font-family: AdvPalBI; font-size:17px", "font-family: AdvGreek_BI; font-size:17px"],
    "get_doi_regex": ["font-family: AdvPalR; font-size:8px"],
    "get_doi_regex_r": ["doi:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvPalR; font-size:8px"],  # Author
    "get_authors_and_affiliations_nu": ["None"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: AdvPalI; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvPalB; font-size:9px"], # Reference title
    "get_references_nonumber_ref": [
        "font-family: AdvPalR; font-size:7px", 
        "font-family: AdvPalI; font-size:7px", 
        "font-family: AdvPalB; font-size:7px",
        "font-family: AdvPalR; font-size:6px", 
        "font-family: AdvPalI; font-size:6px", 
        "font-family: AdvPalB; font-size:6px",
        "font-family: AdvPalR; font-size:5px", 
        "font-family: AdvPalI; font-size:5px", 
        "font-family: AdvPalB; font-size:5px",
        "font-family: AdvEls-ent4; font-size:7px"], # References
    "get_content": ["font-family: AdvPal[RIB]; font-size:9px"], # Content - Regex
    "get_keywords": ["font-family: AdvPalI; font-size:8px"], # Keywords
    "get_abstract": ["font-family: AdvPalB; font-size:9px"], # Abstract
}

doctype1_1 = {
    "get_title": ["font-family: AdvPalatino-b; font-size:17px"],
    "get_doi_regex": ["font-family: CharisSIL; font-size:7px"],
    # "get_doi_regex_r": [""],
    "get_authors_and_affiliations_au": ["font-family: AdvPalatino-r; font-size:8px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: AdvP6F01; font-size:8px"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: AdvPalatino-i; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvPalatino-b; font-size:9px"], # Reference title
    "get_references_nonumber_ref": ["font-family: AdvPalatino-r; font-size:7px", "font-family: AdvPalatino-b; font-size:7px", "font-family: AdvPalatino-i; font-size:7px"], # References
    "get_content": ["font-family: AdvPalatino-[ri]; font-size:8px"], # Content
    "get_keywords": ["font-family: AdvPalatino-i; font-size:8px"], # Keywords
    "get_abstract": ["font-family: AdvPalatino-b; font-size:9px"], # Abstract
}

doctype2_1 = {
    "get_title": ["font-family: AdvPSPAL-B; font-size:17px", "font-family: AdvPSPAL-BI; font-size:17px"],
    "get_doi_regex": ["font-family: AdvPSPAL-R; font-size:8px"],
    "get_doi_regex_r": ["doi:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvPSPAL-R; font-size:8px", 
                                        "font-family: Advpala-ita; font-size:8px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: 20; font-size:8px"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: Advpala-ita; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvPSPAL-B; font-size:10px"], # Reference title
    "get_references_nonumber_ref": ["font-family: AdvPSPAL-R; font-size:5px", "font-family: AdvPSPAL-ita; font-size:5px", "font-family: AdvPSPAL-B; font-size:5px"], # References
    "get_content": ["font-family: AdvPSPAL-(R|ita); font-size:9px"], # Content
    "get_keywords": ["font-family: Advpala-ita; font-size:8px"], # Keywords
    "get_abstract": ["font-family: AdvPSPAL-B; font-size:9px"], # Abstract
}

doctype3_1 = {
    "get_title": ["font-family: AdvTT6071803a.B; font-size:17px", "font-family: AdvPSPAL-BI; font-size:17px"],
    "get_doi_regex": ["font-family: AdvTTa9c1b374; font-size:6px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvTT6071803a.B; font-size:11px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: AdvTT6071803a.B; font-size:7px"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: AdvTTa9c1b374; font-size:6px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvTT6071803a.B; font-size:7px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvTTa9c1b374; font-size:7px", "font-family: AdvTTeb5f0e55.I; font-size:7px"], # References
    "get_content": ["font-family: (AdvTTa9c1b374|AdvTTeb5f0e55.I); font-size:7px"], # Content
    "get_keywords": ["font-family: AdvTT6071803a.B; font-size:6px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: AdvTTa9c1b374; font-size:7px"], # Keywords styles
    "get_abstract": ["font-family: AdvTT6071803a.B; font-size:9px"], # Abstract
}

doctype4_1 = {
    "get_title": ["font-family: Lato-Bold; font-size:17px"],
    "get_doi_regex": ["font-family: Lato-Regular; font-size:6px", "font-family: Lato-Regular; font-size:7px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: Lato-Bold; font-size:11px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: Lato-Bold; font-size:7px"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: Lato-Regular; font-size:6px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: Lato-Bold; font-size:7px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: Lato-Regular; font-size:7px", "font-family: Lato-Italic; font-size:7px"], # References
    "get_content": ["font-family: Lato-(Regular|Italic); font-size:7px"], # Content
    "get_keywords": ["font-family: Lato-Bold; font-size:6px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: Lato-Regular; font-size:7px"], # Keywords styles
    "get_abstract": ["font-family: Lato-Bold; font-size:9px"], # Abstract
}

doctype5_1 = {
    "get_title": ["font-family: Lato-Bold; font-size:18px"],
    "get_doi_regex": ["font-family: Lato-Regular; font-size:7px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: Lato-Bold; font-size:12px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: Lato-Bold; font-size:8px"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: Lato-Regular; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: Lato-Bold; font-size:8px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: Lato-Regular; font-size:7px", "font-family: Lato-Italic; font-size:7px"], # References
    "get_content": ["font-family: Lato-(Regular|Italic); font-size:8px"], # Content
    "get_keywords": ["font-family: Lato-Bold; font-size:7px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: Lato-Regular; font-size:8px"], # Keywords styles
    "get_abstract": ["font-family: Lato-Bold; font-size:10px", "font-family: Lato-Bold; font-size:9px"], # Abstract
}

doctype6_1 = {
    "get_title": ["font-family: Palatino-Bold; font-size:17px"],
    "get_doi_regex": ["font-family: Palatino-Roman; font-size:7px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: Palatino-Roman; font-size:8px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: Palatino-Roman; font-size:8px"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: Palatino-Italic; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: Palatino-Bold; font-size:9px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: Palatino-Roman; font-size:7px", "font-family: Palatino-Italic; font-size:7px"], # References
    "get_content": ["font-family: Palatino-(Roman|Italic); font-size:8px"], # Content
    "get_keywords": ["font-family: Palatino-Italic; font-size:8px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: Palatino-Roman; font-size:8px", 
                            "font-family: Palatino-Italic; font-size:8px"], # Keywords styles
    "get_abstract": ["font-family: Palatino-Bold; font-size:9px", "font-family: Palatino-Bold; font-size:9px"], # Abstract
}

doctypedef_1 = {
    "get_title": ["font-size:17px"],
    "get_doi_regex": ["font-size:8px"],
    "get_authors_and_affiliations_au": ["font-size:8px"],  # Author
    "get_authors_and_affiliations_nu": ["font-size:8px"],   # Number
    "get_authors_and_affiliations_af": ["font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-size:10px"], # Reference title
    "get_references_nonumber_ref": ["font-size:6px", "font-size:5px" ], # References
    "get_content": ["font-size:9px"], # Content
    "get_keywords": ["font-size:8px"], # Keywords
    "get_abstract": ["font-size:9px"]
}

# List of style samples to try for processing
styles = [doctype0_1, doctype1_1, doctype2_1, doctype3_1, doctype4_1, doctype5_1, doctype6_1, doctypedef_1]

data_list = []
Faults = 0
Faulty_samples = []
Styleless_samples = []

skip_samples = ["Corrigendum", "Author index"]

# Special layout settings for PDFs after 2016
year = [str(i) for i in range(2016, 2024)]

# samples = [a.replace(".html", ".pdf") for a in listdir(DIR.replace("SAMPLE", "TEST"))]
if not samples:
    samples = listdir(DIR) 
    multi_flag = False
# samples = ["Global Change Biology - 2001 - Hendrey - A free‐air enrichment system for exposing tall forest vegetation to elevated(2).pdf"]
for sample in samples:
    s = 0
    # print(20*"-")
    print(sample)
    
    should_skip = any(True for skip in skip_samples if skip in sample)
    if should_skip:
        print(f"Skipping {sample.split()[0]} pdf: {sample}")
        continue
    
    # Parse to html
    if any(True for i in year if i in sample):
        # print("Year over 2016.")
        html = pdf2html(target=DIR+sample, line_margin=0.7) # Hot fix for newer PDFs
    else:
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

    # Get data
    if s >= 0 and s < len(styles):
        style = styles[s]
        if "get_keywords_r" in style.keys():
            if "get_keywords_styles" in style.keys():
                keywords = get_keywords(soup, style["get_keywords"], style["get_keywords_r"][0], style["get_keywords_styles"])
            else:
                keywords = get_keywords(soup, style["get_keywords"], style["get_keywords_r"][0])
        else:
            keywords = get_keywords(soup, style["get_keywords"])
        authors_and_affiliations, affiliations = get_authors_and_affiliations(soup, style["get_authors_and_affiliations_au"], style["get_authors_and_affiliations_nu"], style["get_authors_and_affiliations_af"])
        # authors_and_affiliations, affiliations = [], []
        # print(affiliations)
        authors, journal, date, subjects, abstract = get_from_doi2bibapi(doi[0]) # Sa meta/v2 je bilo moguće dohvatiti i disciplines

        # Try available regex styles if unintentional doi was found prior
        if authors == "no_authors":
            warning_message = "DOI isn't extracted correctly. -> Implies wrong regex pattern, trying other options if available ..."
            logging.warning(warning_message)
            if "get_doi_regex_r" in style.keys():
                for regex in style["get_doi_regex_r"]:
                    doi = get_doi_regex(soup, style["get_doi_regex"], regex)
                    if doi[0] != "no_doi":
                        print(doi)
                        break
            
            authors, journal, date, subjects, abstract = get_from_doi2bibapi(doi[0]) # Sa meta/v2 je bilo moguće dohvatiti i disciplines
        # print(authors)
        # print(journal)
        # print(date)
        # print(subjects)
        # print(abstract[:100])
        if "get_references_nonumber_title_r" in style.keys():
            references = get_references_nonumber(soup, style["get_references_nonumber_title"], style["get_references_nonumber_ref"], style["get_references_nonumber_title_r"][0])
        else:
            references = get_references_nonumber(soup, style["get_references_nonumber_title"], style["get_references_nonumber_ref"])
        # print(references[:5])
        if "get_abstract" in style.keys() and abstract == "no_abstract":
            abstract = get_abstract(soup, style["get_abstract"])

        # Add references tag to remove during content extraction
        elem = find_custom_element_by_regex(soup) 
        add_custom_tag_after_element(soup, elem, "reftag", "STOP CONTENT EXTRACTION HERE IN THE NAME OF GOD", {'style': 'font-family: TimesNewReference; font-size:69px'})
        
        content = get_content(soup, style["get_content"])

        # print("Content length: ", len(content))
        # char_number2words_pages(len(content))
        # print(abstract)

        
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
            "Keywords": keywords,
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
# print(paper_data)
##
t = round(time(), 1) # Timestamp when multiprocessing
n = randint(1, 10) # For fragments of dataframes
df = pd.DataFrame(data_list)
if multi_flag:
    df.to_pickle(f"./RESULTS/GCB/gcb_({t})_({n}).pickle")
else:
    df.to_pickle("./PARS_OUT/test_gcb.pickle")
print(Faults)
##