"""
GCB html parsing
"""

from bs4 import BeautifulSoup
from parser_pdf import get_title, get_content, get_doi_regex, get_from_doi2bibapi, get_authors_and_affiliations, get_references_nonumber, get_keywords
from functions import pdf2html
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

DIR = "./SAMPLE/GCB/"

doctype0_1 = {
    "get_title": ["font-family: AdvPalB; font-size:17px"],
    "get_doi_regex": ["font-family: AdvPalR; font-size:8px"],
    "get_doi_regex_r": ["doi:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvPalR; font-size:8px"],  # Author
    "get_authors_and_affiliations_nu": ["None"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: AdvPalI; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvPalB; font-size:9px"], # Reference title
    "get_references_nonumber_ref": ["font-family: AdvPalR; font-size:7px", "font-family: AdvPalI; font-size:7px", "font-family: AdvPalB; font-size:7px"], # References
    "get_content": ["font-family: AdvPalR; font-size:9px", "font-family: AdvPalB; font-size:9px"], # Content
    "get_keywords": ["font-family: AdvPalI; font-size:8px"], # Keywords
}

doctype1_1 = {
    "get_title": ["font-family: CharisSIL; font-size:13px"],
    "get_doi_regex": ["font-family: CharisSIL; font-size:7px"],
    "get_doi_regex_r": [""],
    "get_authors_and_affiliations_au": ["font-family: CharisSIL; font-size:10px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: CharisSIL; font-size:7px"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: CharisSIL-Italic; font-size:6px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: CharisSIL-Bold; font-size:7px"], # Reference title
    "get_references_nonumber_ref": ["font-family: CharisSIL; font-size:6px",  ], # References
    "get_content": ["font-family: CharisSIL; font-size:7px"], # Content
    "get_keywords": ["font-family: CharisSIL-Italic; font-size:6px"]
}

doctype2_1 = {
    "get_title": ["font-family: AdvOT596495f2; font-size:13px"],
    "get_doi_regex": ["font-family: AdvOT596495f2; font-size:6px", "font-family: AdvOT596495f2; font-size:7px"],
    "get_authors_and_affiliations_au": ["font-family: AdvOT596495f2; font-size:10px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: AdvOT596495f2; font-size:7px"],   # Number
    "get_authors_and_affiliations_af": ["font-family: AdvOT7fb33346.I; font-size:6px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvOT1efcda3b.B; font-size:7px"], # Reference title
    "get_references_nonumber_ref": ["font-family: AdvOT596495f2; font-size:6px",  ], # References
    "get_content": ["font-family: AdvOT596495f2; font-size:7px"], # Content
    "get_keywords": ["font-family: AdvOT7fb33346.I; font-size:6px"]
}

doctype3_1 = {
    "get_title": ["font-family: AdvOT863180fb; font-size:13px"],
    "get_doi_regex": ["font-family: AdvOT863180fb; font-size:6px"],
    "get_authors_and_affiliations_au": ["font-family: AdvOT863180fb; font-size:10px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: AdvOT863180fb; font-size:7px"],   # Number
    "get_authors_and_affiliations_af": ["font-family: AdvOTb92eb7df.I; font-size:6px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvOTb83ee1dd.B; font-size:7px"], # Reference title
    "get_references_nonumber_ref": ["font-family: AdvOT863180fb; font-size:6px",  ], # References
    "get_content": ["font-family: AdvOT863180fb; font-size:7px"], # Content
    "get_keywords": ["font-family: AdvOTb92eb7df.I; font-size:6px"], # Keywords
}

doctype4_1 = {
    "get_title": ["font-family: AdvGulliver; font-size:13px"],
    "get_doi_regex": ["font-family: AdvGulliver; font-size:6px"],
    "get_doi_regex_r": ["doi:([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvGulliver; font-size:10px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: AdvGulliver; font-size:7px", "font-family: AdvMacms; font-size:9px"],   # Number
    "get_authors_and_affiliations_af": ["font-family: AdvOTb92eb7df.I; font-size:6px", "font-family: AdvGulliver-I; font-size:6px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvGulliver-B; font-size:7px"], # Reference title
    "get_references_nonumber_ref": ["font-family: AdvGulliver; font-size:6px"], # References
    "get_content": ["font-family: AdvGulliver; font-size:7px"], # Content
    "get_keywords": ["font-family: AdvGulliver-I; font-size:6px"], # Keywords
}

doctype5_1 = {
    "get_title": ["font-family: AdvTimes; font-size:16px"],
    "get_doi_regex": ["font-family: AdvTimes; font-size:7px"],
    "get_doi_regex_r": ["doi:([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvTimes; font-size:12px"],  # Author
    "get_authors_and_affiliations_nu": ["font-family: AdvMacms; font-size:12px"],   # Number
    "get_authors_and_affiliations_af": ["font-family: AdvTimes; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvTimes-b; font-size:9px"], # Reference title
    "get_references_nonumber_ref": ["font-family: AdvTimes; font-size:7px"], # References
    "get_content": ["font-family: AdvTimes; font-size:9px"], # Content
    "get_keywords": ["font-family: AdvMc_Times-i; font-size:7px"], # Keywords
}

doctypedef_1 = {
    "get_title": ["font-size:13px"],
    "get_doi_regex": ["font-size:6px"],
    "get_authors_and_affiliations_au": ["font-size:10px"],  # Author
    "get_authors_and_affiliations_nu": ["font-size:7px"],   # Number
    "get_authors_and_affiliations_af": ["font-size:6px"],  # Affiliation text
    "get_references_nonumber_title": ["font-size:7px"], # Reference title
    "get_references_nonumber_ref": ["font-size:6px",  ], # References
    "get_content": ["font-size:7px"], # Content
    "get_keywords": ["font-size:6px", "font-size:7px"], # Keywords
}

# List of style samples to try for processing
styles = [doctype0_1, doctype1_1, doctype2_1, doctype3_1, doctype4_1, doctype5_1, doctypedef_1]

data_list = []
Faults = 0
Faulty_samples = []
Styleless_samples = []

skip_samples = []

# samples = [a.replace(".html", ".pdf") for a in listdir(DIR.replace("SAMPLE", "TEST"))]
# samples = listdir(DIR) 
samples = ["Global Change Biology - 2003 - Ares - Detection of process‐related changes in plant patterns at extended spatial scales.pdf"]
for sample in tqdm(samples):
    s = 0
    print(20*"-")
    print(sample)
    
    should_skip = any(sample.startswith(skip) for skip in skip_samples)
    if should_skip:
        print(f"Skipping {sample.split()[0]} pdf: {sample}")
        continue
    
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

        if len(title[0]) > 185:
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
        keywords = get_keywords(soup, style["get_keywords"])
        authors_and_affiliations, affiliations = get_authors_and_affiliations(soup, style["get_authors_and_affiliations_au"], style["get_authors_and_affiliations_nu"], style["get_authors_and_affiliations_af"])
        authors_and_affiliations, affiliations = [], []
        # print(affiliations)
        authors, journal, date, subjects, abstract = get_from_doi2bibapi(doi[0]) # Sa meta/v2 je bilo moguće dohvatiti i disciplines
        # print(authors)
        # print(journal)
        # print(date)
        # print(subjects)
        # print(abstract[:100])
        references = get_references_nonumber(soup, style["get_references_nonumber_title"], style["get_references_nonumber_ref"])
        # print(references[:5])
        content = get_content(soup, style["get_content"])
        print("Content length: ", len(content))
        
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
            "Content": "None",
            "Keywords": "None",
        }
        Styleless_samples.append(sample)

# Create the DataFrame from the list of dictionaries
print(Styleless_samples)
print(Faulty_samples)
# print(paper_data)
df = pd.DataFrame(data_list)
df.to_pickle("test_gcb.pickle")
print(Faults)