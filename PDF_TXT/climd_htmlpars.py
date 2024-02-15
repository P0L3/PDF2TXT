"""
CLIMD html parsing
"""

from bs4 import BeautifulSoup
from parser_pdf import *
from functions import pdf2html, find_custom_element_by_regex, add_custom_tag_after_element, check_if_ium
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging

DIR = "./SAMPLE/CLIMD/"
logging.basicConfig(
    format='%(asctime)s %(message)s',
    filename="_".join(DIR.split("/")),
    filemode='w',
    ) # Adds time to warning output

doctype0_1 = {
    "get_title": ["font-family: LfhjmrMyriadPro-SemiboldSemiCn; font-size:16px"],
    "get_doi_regex": ["font-family: CrpyqwMyriadPro-SemiCn; font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: VdpqsdMyriadPro-Semibold; font-size:10px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: VdpqsdMyriadPro-Semibold; font-size:7px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: CmkfxpSTIX-Regular; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: LdkgqbMyriadPro-Bold; font-size:12px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: CmkfxpSTIX-Regular; font-size:8px",], # References text
    "get_content": ["font-family: (CmkfxpSTIX-Regular|XcrglhSTIXGeneral-Regular|YgbmsbSTIXGeneral-Regular|RtsnqcSTIXGeneral-Regular|TplwbkSTIXGeneral-Regular|TtvtmhSTIXMath-Regular); font-size:10px"], # Content regex
    "get_keywords": ["font-family: LfhjmrMyriadPro-SemiboldSemiCn; font-size:10px"], # Keywords title
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: CmkfxpSTIX-Regular; font-size:10px"], # Keywords styles
    "get_abstract": ["font-family: LdkgqbMyriadPro-Bold; font-size:10px"], # Abstract
}

doctype1_1 = {
    "get_title": ["font-family: MyriadPro-SemiboldSemiCn; font-size:16px"],
    "get_doi_regex": ["font-family: MyriadPro-SemiCn; font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: MyriadPro-Semibold; font-size:10px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: MyriadPro-Semibold; font-size:7px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: STIX-Regular; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: MyriadPro-Bold; font-size:12px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: STIX-Regular; font-size:8px", "font-family: MyriadPro-SemiCn; font-size:8px"], # References text
    "get_content": ["font-family: STIX-Regular; (font-size:10px|font-size:9px)"], # Content regex
    "get_keywords": ["font-family: MyriadPro-SemiboldSemiCn; font-size:10px"], # Keywords title
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-family: STIX-Regular; font-size:10px"], # Keywords styles
    "get_abstract": ["font-family: MyriadPro-Bold; font-size:10px"], # Abstract
}

doctype2_1 = {
    "get_title": ["font-family: AdvPTimesB; font-size:15px"],
    "get_doi_regex": ["font-family: AdvPTimes; font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:*\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvPTimesB; font-size:9px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: AdvPTimes; font-size:8px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: AdvPTimes; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvPTimesB; font-size:9px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvPTimes; font-size:8px"], # References text
    "get_content": ["font-family: AdvPTimes(|I); font-size:9px"], # Content regex
    "get_keywords": ["font-family: AdvPTimesB; font-size:9px"], # Keywords title
    "get_abstract": ["font-family: AdvPTimesB; font-size:9px"], # Abstract
}

doctype3_1 = {
    "get_title": ["font-family: AdvPSFGC; font-size:17px"],
    "get_doi_regex": ["font-family: AdvTimes; font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:*\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvTimes-b; font-size:10px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: AdvTimes; font-size:8px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: AdvTimes; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvPSFGC; font-size:10px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvTimes; font-size:8px"], # References text
    "get_content": ["font-family: (AdvTimes|AdvP4C4E74|AdvPSSPSMI|AdvP4C4E51|AdvP4C4E59|AdvPSSym|AdvTimes-i); font-size:10px"], # Content regex
    "get_keywords": ["font-family: AdvTimes-b; font-size:10px"], # Keywords title
    "get_abstract": ["font-family: AdvTimes-b; font-size:10px"], # Abstract
}

doctype4_1 = {
    "get_title": ["font-family: FranklinGothic-Heavy; font-size:18px"],
    "get_doi_regex": ["font-family: AdvTimes; font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:*\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: MathPackThree; font-size:10px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: MathPackThree; font-size:10px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: MathPackOne; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: FranklinGothic-Heavy; font-size:10px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: MathPackOne; font-size:8px", 
                                    "font-family: MacmillanMixed1; font-size:8px", 
                                    "font-family: MathPackFour; font-size:8px"], # References text
    "get_content": ["font-family: (MathPackOne|MacmillanMixed1|MathPackFour); font-size:10px"], # Content regex
    "get_keywords": ["font-family: MathPackThree; font-size:10px"], # Keywords title
    "get_abstract": ["font-family: MathPackThree; font-size:10px"], # Abstract
}

doctype5_1 = {
    "get_title": ["font-family: AdvPSTIM10-B; font-size:15px"],
    "get_doi_regex": ["font-family: AdvPSTIM10-R; font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:*\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: AdvPSTIM10-B; font-size:9px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: AdvPSTIM10-R; font-size:8px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: AdvPSTIM10-R; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: AdvPSTIM10-B; font-size:9px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: AdvPSTIM10-R; font-size:8px", ], # References text
    "get_content": ["font-family: AdvPSTIM10-R; font-size:9px", ], # Content regex
    "get_keywords": ["font-family: AdvPSTIM10-B; font-size:9px"], # Keywords title
    "get_abstract": ["font-family: AdvPSTIM10-B; font-size:9px"], # Abstract
}

doctype6_1 = {
    "get_title": ["font-family: MathPackThree; font-size:17px"],
    "get_doi_regex": ["font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:*\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-family: MathPackThree; font-size:10px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-family: MathPackThree; font-size:6px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-family: MathPackOne; font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-family: MathPackThree; font-size:10px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-family: MathPackOne; font-size:8px", "font-family: MathPackTwo; font-size:8px"], # References text
    "get_content": ["font-family: MathPack(One|Two); (font-size:10px|font-size:9px)"], # Content regex
    "get_keywords": ["font-family: MathPackThree; font-size:10px"], # Keywords title
    "get_abstract": ["font-family: MathPackThree; font-size:10px"], # Abstract
}

doctypedef_1 = {
    "get_title": ["font-size:16px"],
    "get_doi_regex": ["font-size:8px"],
    "get_doi_regex_r": ["[Dd][Oo][Ii]:\s*([\d.\/\w-]+)"],
    "get_authors_and_affiliations_au": ["font-size:10px"],  # Author name text
    "get_authors_and_affiliations_nu": ["font-size:7px"],  # Affiliation number
    "get_authors_and_affiliations_af": ["font-size:8px"],  # Affiliation text
    "get_references_nonumber_title": ["font-size:12px"], # Reference title
    "get_references_nonumber_title_r": ["^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n"], # Reference custom regex
    "get_references_nonumber_ref": ["font-size:8px",], # References text
    "get_content": ["(font-size:10px|font-size:9px)"], # Content regex
    "get_keywords": ["font-size:10px"], # Keywords title
    "get_keywords_r": ["^(?i)k\s*e\s*y\s*w\s*o\s*r\s*d\s*s\n*"], # Keywords regex
    "get_keywords_styles": ["font-size:10px"], # Keywords styles
    "get_abstract": ["font-size:10px"], # Abstract
}



# List of style samples to try for processing
styles = [doctype0_1, doctype1_1, doctype2_1, doctype3_1, doctype4_1, doctype5_1, doctype6_1, doctypedef_1]

data_list = []
Faults = 0
Faulty_samples = []
Styleless_samples = []

skip_samples = ["Issue Information"]
# year_skip = [n for n in range(1990, 2002)] # Skip years that are probably scanned (high effort - low reward)
# for y in year_skip:
#     skip_samples.append(f" {y} -")



# samples = [a.replace(".html", ".pdf") for a in listdir(DIR.replace("SAMPLE", "TEST"))]
samples = listdir(DIR) 
# print(samples[2])
# exit()
# samples = ["s00382-018-4083-9.pdf"]
for sample in tqdm(samples[85:]):
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
                keywords = get_keywords(soup, style["get_keywords"], style["get_keywords_r"][0], style["get_keywords_styles"], obj="span")
            else:
                keywords = get_keywords(soup, style["get_keywords"], style["get_keywords_r"][0], obj="span")
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
df = pd.DataFrame(data_list)
df.to_pickle("./PARS_OUT/test_climd.pickle")
print(Faults)