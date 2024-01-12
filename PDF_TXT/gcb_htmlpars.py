"""
GCB html parsing
"""

from bs4 import BeautifulSoup
from parser_pdf import get_abstract, get_title, get_content, get_doi_regex, get_from_doi2bibapi, get_authors_and_affiliations, get_references_nonumber, get_keywords, char_number2words_pages
from functions import pdf2html
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

DIR = "./SAMPLE/GCB/"

doctype0_1 = {
    "get_title": ["font-family: AdvPalB; font-size:17px", "font-family: AdvPalBI; font-size:17px", "font-family: AdvGreek_BI; font-size:17px"],
    "get_doi_regex": ["font-family: AdvPalR; font-size:8px"],
    "get_doi_regex_r": ["doi:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvPalR; font-size:8px"],  # Author
    "get_authors_and_affiliations_nu": ["None"],   # Number, Letter
    "get_authors_and_affiliations_af": ["font-family: AdvPalI; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvPalB; font-size:9px"], # Reference title
    "get_references_nonumber_ref": [
        "font-family: AdvPalR; font-size:7px", "font-family: AdvPalI; font-size:7px", "font-family: AdvPalB; font-size:7px",
        "font-family: AdvPalR; font-size:6px", "font-family: AdvPalI; font-size:6px", "font-family: AdvPalB; font-size:6px",
        "font-family: AdvPalR; font-size:5px", "font-family: AdvPalI; font-size:5px", "font-family: AdvPalB; font-size:5px"], # References
    "get_content": ["font-family: AdvPal[RI]; font-size:9px"], # Content - Regex
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
    "get_authors_and_affiliations_au": ["font-family: AdvPSPAL-R; font-size:8px"],  # Author
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
    "get_content": ["font-family: AdvTTa9c1b374; font-size:7px", "font-family: AdvTTeb5f0e55.I; font-size:7px"], # Content
    "get_keywords": ["font-family: AdvTT6071803a.B; font-size:6px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: AdvTTa9c1b374; font-size:7px"], # Keywords styles
    "get_abstract": ["font-family: AdvTT6071803a.B; font-size:9px"], # Abstract
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
styles = [doctype0_1, doctype1_1, doctype2_1, doctype3_1, doctypedef_1]

data_list = []
Faults = 0
Faulty_samples = []
Styleless_samples = []

skip_samples = []

# Special layout settings for PDFs after 2016
year = [str(i) for i in range(2016, 2024)]

# samples = [a.replace(".html", ".pdf") for a in listdir(DIR.replace("SAMPLE", "TEST"))]
# samples = listdir(DIR) 
samples = ["Global Change Biology - 2017 - Assis - Projected climate changes threaten ancient refugia of kelp forests in the North(1).pdf"]
for sample in tqdm(samples):
    s = 0
    print(20*"-")
    print(sample)
    
    should_skip = any(sample.startswith(skip) for skip in skip_samples)
    if should_skip:
        print(f"Skipping {sample.split()[0]} pdf: {sample}")
        continue
    
    # Parse to html
    if any(True for i in year if i in sample):
        print("Year over 2016.")
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
        if "get_keywords_r" in style.keys():
            if "get_keywords_styles" in style.keys():
                keywords = get_keywords(soup, style["get_keywords"], style["get_keywords_r"][0], style["get_keywords_styles"])
            else:
                keywords = get_keywords(soup, style["get_keywords"], style["get_keywords_r"][0])
        else:
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
        if "get_references_nonumber_title_r" in style.keys():
            references = get_references_nonumber(soup, style["get_references_nonumber_title"], style["get_references_nonumber_ref"], style["get_references_nonumber_title_r"][0])
        else:
            references = get_references_nonumber(soup, style["get_references_nonumber_title"], style["get_references_nonumber_ref"])
        # print(references[:5])
        if "get_abstract" in style.keys() and abstract == "no_abstract":
            abstract = get_abstract(soup, style["get_abstract"])
        content = get_content(soup, style["get_content"])
        content = content.split(references[0])[0]
        print("Content length: ", len(content))
        char_number2words_pages(len(content))
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