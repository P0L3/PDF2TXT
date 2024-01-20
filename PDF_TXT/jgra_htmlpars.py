"""
GCB html parsing
"""

from bs4 import BeautifulSoup
from parser_pdf import *
from functions import pdf2html, find_custom_element_by_regex, add_custom_tag_after_element, check_if_ium
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

DIR = "./SAMPLE/JGRA/"

doctype0_1 = {
    "get_title": ["font-family: MyriadPro-Semibold; font-size:15px"],
    "get_doi_regex": ["font-family: MyriadPro-Regular; font-size:7px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: MyriadPro-Bold; font-size:9px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: MyriadPro-Bold; font-size:6px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: MyriadPro-Regular; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: MyriadPro-Bold; font-size:11px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: MyriadPro-Regular; font-size:7px", "font-family: MyriadPro-It; font-size:7px"], # References text
    "get_content": ["font-family: MyriadPro-(Regular|It); font-size:9px"], # Content regex
    "get_keywords": ["font-family: Times-Italic; font-size:8px"], # Keywords
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: Times-Italic; font-size:8px"], # Keywords styles
    "get_abstract": ["font-family: MyriadPro-Bold; font-size:12px"], # Abstract
}

doctype1_1 = {
    "get_title": ["font-family: AdvTT99c4c969; font-size:15px"],
    "get_doi_regex": ["font-family: AdvTTe45e47d2; font-size:6px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvTTaf7f9f4f.B; font-size:9px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: AdvTTaf7f9f4f.B; font-size:5px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: AdvTTe45e47d2; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvTTaf7f9f4f.B; font-size:11px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvTTe45e47d2; font-size:6px", "font-family: AdvTT7329fd89.I; font-size:6px"], # References text
    "get_content": ["font-family: (AdvTTe45e47d2|AdvTT7329fd89.I); font-size:9px"], # Content regex 
    "get_keywords": ["font-family: AdvTTaf7f9f4f.B; font-size:6px"], # Keywords (Key points)
    "get_keywords_r": ["(?i)^Key Points:\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: AdvTTe45e47d2; font-size:6px", "font-family: 20; font-size:6px"], # Keywords styles
    "get_abstract": ["font-family: AdvTTaf7f9f4f.B; font-size:11px"], # Abstract
}

doctype2_1 = {
    "get_title": ["font-family: AdvTT2cba4af3.B; font-size:13px"],
    "get_doi_regex": ["font-family: AdvTT5843c571; font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvTT5843c571; font-size:10px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: AdvTT5843c571; font-size:7px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: AdvTT5843c571; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvTT2cba4af3.B; font-size:10px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvTT5843c571; font-size:7px", "font-family: AdvTTf90d833a.I; font-size:7px"], # References text
    "get_content": ["font-family: (AdvTT5843c571|AdvTTf90d833a.I); font-size:10px"], # Content regex 
    "get_keywords": ["font-family: AdvTTaf7f9f4f.B; font-size:6px"], # Keywords (Key points)
    "get_keywords_r": ["(?i)^Key Points:\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: AdvTTe45e47d2; font-size:6px", "font-family: 20; font-size:6px"], # Keywords styles
    "get_abstract": ["font-family: AdvTT5843c571; font-size:10px"], # Abstract
}

doctype3_1 = {
    "get_title": ["font-family: AdvTTb65e66bd; font-size:15px"],
    "get_doi_regex": ["font-family: AdvTT46dcae81; font-size:6px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvTT3b30f6db.B; font-size:9px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: AdvTT3b30f6db.B; font-size:5px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: AdvTT46dcae81; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvTT3b30f6db.B; font-size:11px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvTT65f8a23b.I; font-size:6px", "font-family: fb; font-size:6px", "font-family: AdvTT46dcae81; font-size:6px"], # References text
    "get_content": ["font-family: (AdvTT46dcae81|AdvTT65f8a23b.I); font-size:9px"], # Content regex 
    "get_keywords": ["font-family: AdvTT3b30f6db.B; font-size:6px"], # Keywords (Key points)
    "get_keywords_r": ["(?i)^Key Points:\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: AdvTT46dcae81; font-size:6px", "font-family: 20; font-size:6px"], # Keywords styles
    "get_abstract": ["font-family: AdvTT3b30f6db.B; font-size:11px"], # Abstract
}

doctype4_1 = {
    "get_title": ["font-family: STIXTwoText-Bold; font-size:15px"],
    "get_doi_regex": ["font-family: STIXTwoText; font-size:7px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: STIXTwoText-Bold; font-size:9px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: STIXTwoText-Bold; font-size:5px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: STIXTwoText; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: STIXTwoText-Bold; font-size:11px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: STIXTwoText; font-size:7px", "font-family: STIXTwoText-Italic; font-size:7px"], # References text
    "get_content": ["font-family: STIXTwoText; font-size:9px"], # Content regex 
    "get_keywords": ["font-family: STIXTwoText-Bold; font-size:7px"], # Keywords (Key points)
    "get_keywords_r": ["(?i)^Key Points:\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: STIXTwoText; font-size:7px"], # Keywords styles
    "get_abstract": ["font-family: STIXTwoText-Bold; font-size:12px"], # Abstract
}

doctype5_1 = {
    "get_title": ["font-family: AdvTTf331adb4.B; font-size:13px"],
    "get_doi_regex": ["font-family: AdvTT182ff89e; font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvTT182ff89e; font-size:10px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: AdvTT182ff89e; font-size:7px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: AdvTT182ff89e; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvTTf331adb4.B; font-size:10px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvTT182ff89e; font-size:7px", "font-family: AdvTT73b978ed.I; font-size:7px"], # References text
    "get_content": ["font-family: (AdvTT182ff89e|AdvTT73b978ed.I); font-size:9px"], # Content regex 
    "get_keywords": ["font-family: STIXTwoText-Bold; font-size:7px"], # Keywords (Key points)
    "get_keywords_r": ["(?i)^Key Points:\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: STIXTwoText; font-size:7px"], # Keywords styles
    "get_abstract": ["font-family: AdvTT182ff89e; font-size:10px"], # Abstract
}

doctype6_1 = {
    "get_title": ["font-family: STIX-Bold; font-size:15px"],
    "get_doi_regex": ["font-family: STIX-Regular; font-size:7px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: STIX-Bold; font-size:9px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: STIX-Bold; font-size:5px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: STIX-Regular; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: STIX-Bold; font-size:11px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: STIX-Regular; font-size:7px", "font-family: STIX-Italic; font-size:7px"], # References text
    "get_content": ["font-family: STIX-Regular; font-size:9px"], # Content regex 
    "get_keywords": ["font-family: STIX-Bold; font-size:7px"], # Keywords (Key points)
    "get_keywords_r": ["(?i)^Key Points:\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: STIX-Regular; font-size:7px"], # Keywords styles
    "get_abstract": ["font-family: STIX-Bold; font-size:12px"], # Abstract
}

doctype7_1 = {
    "get_title": ["font-family: AdvOTc022ae45.B; font-size:15px"],
    "get_doi_regex": ["font-family: AdvOT569473da; font-size:6px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvOTc022ae45.B; font-size:9px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: AdvOTc022ae45.B; font-size:5px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: AdvOT569473da; font-size:7px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvOTc022ae45.B; font-size:11px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvOT569473da; font-size:6px", "font-family: 20; font-size:6px", "font-family: AdvOTf2679e53.I; font-size:6px"], # References text
    "get_content": ["font-family: AdvOT569473da; font-size:9px"], # Content regex 
    "get_keywords": ["font-family: AdvOTc022ae45.B; font-size:6px"], # Keywords (Key points)
    "get_keywords_r": ["(?i)^Key Points:\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: AdvOT569473da; font-size:6px", "font-family: 20; font-size:6px"], # Keywords styles
    "get_abstract": ["font-family: AdvOTc022ae45.B; font-size:11px"], # Abstract
}

doctype8_1 = {
    "get_title": ["font-family: Dutch801BT-Bold; font-size:14px"],
    "get_doi_regex": ["font-family: Dutch801BT-Roman; font-size:9px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: Dutch801BT-Roman; font-size:11px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: Dutch801BT-Roman; font-size:6px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: Dutch801BT-Roman; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: Dutch801BT-Bold; font-size:11px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: Dutch801BT-Roman; font-size:8px", "font-family: Dutch801BT-Italic; font-size:8px", "font-family: Dutch801BT-Roman; font-size:5px"], # References text
    "get_content": ["font-family: Dutch801BT-(Roman|Italic); font-size:9px"], # Content regex 
    "get_keywords": ["font-family: AdvOTc022ae45.B; font-size:6px"], # Keywords (Key points)
    "get_keywords_r": ["(?i)^Key Points:\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: AdvOT569473da; font-size:6px", "font-family: 20; font-size:6px"], # Keywords styles
    "get_abstract": ["font-family: Dutch801BT-Roman; font-size:10px"], # Abstract
}

doctypedef_1 = {
    "get_title": ["font-size:13px", "font-size:15px", "font-size:14px"],
    "get_doi_regex": ["font-size:6px", "font-size:7px" "font-size:8px", "font-size:9px"],
    "get_authors_and_affiliations_au": ["font-family: Dutch801BT-Roman; font-size:11px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: Dutch801BT-Roman; font-size:6px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: Dutch801BT-Roman; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-size:10px", "font-size:11px", ], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-size:6px", "font-size:7px", "font-size:8px"], # References text
    "get_content": ["font-size:[789]px"], # Content
    "get_keywords": ["font-size:6px", "font-size:7px"], # Keywords (Key points)
    "get_keywords_r": ["(?i)^Key Points:\n*"], # Keywords regex
    "get_keywords_styles": ["font-size:6px", "font-size:7px"], # Keywords styles
    "get_abstract": ["font-size:10px", "font-size:11px"], # Abstract
}

# List of style samples to try for processing
styles = [doctype0_1, doctype1_1, doctype2_1, doctype3_1, doctype4_1, doctype5_1, doctype6_1, doctype7_1, doctype8_1, doctypedef_1]

data_list = []
Faults = 0
Faulty_samples = []
Styleless_samples = []

skip_samples = ["Issue Information"]
year_skip = [n for n in range(1990, 2002)] # Skip years that are probably scanned (high effort - low reward)
for y in year_skip:
    skip_samples.append(f" {y} -")



# samples = [a.replace(".html", ".pdf") for a in listdir(DIR.replace("SAMPLE", "TEST"))]
samples = listdir(DIR) 
# print(samples[2])
# exit()
# samples = ["JGR Atmospheres - 2013 - Masiello - Diurnal variation in Sahara desert sand emissivity during the dry season from IASI.pdf"]
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

        authors_and_affiliations, affiliations = get_authors_and_affiliations(soup, style["get_authors_and_affiliations_au"], style["get_authors_and_affiliations_nu"], style["get_authors_and_affiliations_af"])
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
df.to_pickle("test_jgra.pickle")
print(Faults)