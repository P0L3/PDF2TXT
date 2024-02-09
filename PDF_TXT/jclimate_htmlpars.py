"""
GCB html parsing
"""

from bs4 import BeautifulSoup
from parser_pdf import get_abstract, get_title, get_content, get_doi_regex, get_from_doi2bibapi, get_affiliations, get_references_nonumber, get_keywords, char_number2words_pages
from functions import pdf2html, find_custom_element_by_regex, add_custom_tag_after_element, check_if_ium
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

DIR = "./SAMPLE/JCLIMATE/"

doctype0_1 = {
    "get_title": ["font-family: Times-Bold; font-size:12px"],
    "get_doi_regex": ["font-family: Times-Roman; font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_affiliations": ["font-family: Times-Italic; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: Times-Roman; font-size:8px", 
                                      "font-family: Symbol; font-size:8px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: Times-Roman; font-size:8px", 
                                    "font-family: Times-Bold; font-size:8px", 
                                    "font-family: Times-Italic; font-size:8px",
                                    "font-family: Symbol; font-size:8px"], # References
    "get_content": ["font-family: Times-(Roman|Italic); font-size:10px"], # Content
    "get_keywords": ["font-family: Times-Italic; font-size:8px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: Times-Italic; font-size:8px"], # Keywords styles
    "get_abstract": ["font-family: Times-Roman; font-size:8px", "font-family: Symbol; font-size:8px"], # Abstract
}

doctype1_1 = {
    "get_title": ["font-family: AdvPSTIM10-B; font-size:11px"],
    "get_doi_regex": ["font-family: AdvPSTIM10-R; font-size:7px"], # Styles of doi text
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_affiliations": ["font-family: AdvPSTIM10-I; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvPSTIM10-R; font-size:7px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvPSTIM10-R; font-size:7px", "font-family: AdvPSTIM10-I; font-size:7px"], # References
    "get_content": ["font-family: (AdvPSTIM10-R|AdvPSTIM10-I|AdvP4C4E46); font-size:9px"], # Content regex
    "get_keywords": ["font-family: Times-Italic; font-size:8px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: Times-Italic; font-size:8px"], # Keywords styles
    "get_abstract": ["font-family: AdvPSTIM10-R; font-size:7px"], # Abstract
}

doctype2_1 = {
    "get_title": ["font-family: AdvPSTIM10-B; font-size:10px"],
    "get_doi_regex": ["font-family: AdvOTbb216540; font-size:7px", 
                      "font-family: AdvPSTIM10-R; font-size:7px"], # Styles of doi text
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_affiliations": ["font-family: AdvOT2b0f33d7.I; font-size:7px", 
                         "font-family: AdvPSTIM10-I; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvOTbb216540; font-size:7px", 
                                      "font-family: AdvPSTIM10-R; font-size:7px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvOTbb216540; font-size:7px", "font-family: AdvOT2b0f33d7.I; font-size:7px", 
                                    "font-family: AdvPSTIM10-R; font-size:7px", "font-family: AdvPSTIM10-I; font-size:7px"], # References
    "get_content": ["font-family: (AdvOTbb216540|AdvPSTIM10-R); font-size:8px"], # Content regex
    "get_keywords": ["font-family: AdvOTbb216540; font-size:7px",
                     "font-family: AdvPSTIM10-R; font-size:7px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: AdvOTbb216540; font-size:7px",
                            "font-family: AdvPSTIM10-R; font-size:7px"], # Keywords styles
    "get_abstract": ["font-family: AdvOTbb216540; font-size:7px",
                     "font-family: AdvPSTIM10-R; font-size:7px"], # Abstract
}

doctype3_1 = {
    "get_title": ["font-family: TimesTen-Bold; font-size:11px"],
    "get_doi_regex": ["font-family: AdvPSTIM10-R; font-size:7px",
                      "font-family: TimesTen-Roman; font-size:7px"], # Styles of doi text
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_affiliations": ["font-family: TimesTen-Italic; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: TimesTen-Roman; font-size:7px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: TimesTen-Roman; font-size:7px", "font-family: TimesTen-Italic; font-size:7px"], # References
    "get_content": ["font-family: TimesTen-Roman; font-size:9px"], # Content regex
    "get_keywords": ["font-family: Times-Italic; font-size:8px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: Times-Italic; font-size:8px"], # Keywords styles
    "get_abstract": ["font-family: TimesTen-Roman; font-size:7px"], # Abstract
}

doctype4_1 = {
    "get_title": ["font-family: Times-Bold; font-size:12px"],
    "get_doi_regex": ["font-family: Times-Roman; font-size:7px"], # Styles of doi text
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_affiliations": ["font-family: Times-Italic; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: Times-Roman; font-size:8px", 
                                      "font-family: Symbol; font-size:8px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: Times-Roman; font-size:8px", 
                                    "font-family: Times-Italic; font-size:8px",
                                    "font-family: Symbol; font-size:8px"], # References
    "get_content": ["font-family: Times-(Roman|Italic); font-size:10px"], # Content regex
    "get_keywords": ["font-family: Times-Italic; font-size:8px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: Times-Italic; font-size:8px"], # Keywords styles
    "get_abstract": ["font-family: Times-Roman; font-size:8px",
                     "font-family: Symbol; font-size:8px"], # Abstract
}

doctypedef_1 = {
    "get_title": ["font-size:17px"],
    "get_doi_regex": ["font-size:8px"],
    "get_authors_and_affiliations_au": ["font-size:8px"],  # Author
    "get_authors_and_affiliations_nu": ["font-size:8px"],   # Number
    "get_affiliations": ["font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-size:10px"], # Reference title
    "get_references_nonumber_ref": ["font-size:6px", "font-size:5px" ], # References
    "get_content": ["font-size:9px"], # Content
    "get_keywords": ["font-size:8px"], # Keywords
    "get_abstract": ["font-size:9px"]
}

# List of style samples to try for processing
styles = [doctype0_1, doctype1_1, doctype2_1, doctype3_1, doctype4_1, doctypedef_1]

data_list = []
Faults = 0
Faulty_samples = []
Styleless_samples = []

skip_samples = ["masthead"]

# samples = [a.replace(".html", ".pdf") for a in listdir(DIR.replace("SAMPLE", "TEST"))]
samples = listdir(DIR) 
# print(samples[2])
# exit()
# samples = ["Global Change Biology - 2001 - Hendrey - A free‐air enrichment system for exposing tall forest vegetation to elevated(2).pdf"]
for sample in tqdm(samples):
    s = 0
    print(20*"-")
    print(sample)
    
    should_skip = any(True for skip in skip_samples if skip in sample)
    if should_skip:
        print(f"Skipping {sample.split()[0]} pdf: {sample}")
        continue
    
    # Parse to html
    html = pdf2html(target=DIR+sample, all_texts=False)
    if not html:
        Faults += 1
        warning_message = f"HTML isn't parsed correctly -> Implies invalid pdf structure!"
        logging.warning(warning_message)
        Faulty_samples.append(sample)
        continue
    
    # Wy to deal with pdf scans heuristicaly
    if len(html) < 15000:
        warning_message = f"HTML is less then 15000 characters long -> Implies a scanned PDF document!"
        logging.warning(warning_message)
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
        # authors_and_affiliations, affiliations = get_authors_and_affiliations(soup, style["get_authors_and_affiliations_au"], style["get_authors_and_affiliations_nu"], style["get_authors_and_affiliations_af"])
        # authors_and_affiliations, affiliations = [], []
        # print(affiliations)
        authors_and_affiliations = ["no_authafil"]
        affiliations = get_affiliations(soup, style["get_affiliations"])
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
            if doi[0].endswith("."): # Hot fix if doi ends with . 
                doi[0] = doi[0][:-1]
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

        print("Content length: ", len(content))
        char_number2words_pages(len(content), re.findall(r"font-size:(\d+)", style["get_content"][0])[0])
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
df.to_pickle("test_jclimate.pickle")
print(Faults)