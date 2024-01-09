"""
Functions to use with Nature papers
"""

from bs4 import BeautifulSoup
import requests
import re
import logging
import subprocess

# Works on 80% -> not open access papers
def get_title(soup, styles):
    """
    Extracts the title(s) from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.
    style (str list): List of strings containing specific style that corresponds to titles.

    Returns:
    list: A list of titles extracted from the provided HTML.
    """
    # Find elements with font size 24 -> Tends to be title
    s24elem = soup.find_all(style=lambda value: value and any(style in value for style in styles))
    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s24elem]

    return ["".join(text_content)] # Replacement if Titles happen to be in multiple styles

def get_doi(soup, styles):
    """
    Extracts the DOI(s) from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.
    style (str list): List of strings containing specific style that corresponds to DOIs.

    Returns:
    list: A list containing DOI(s) extracted from the provided HTML.
    """

    # Find elements with font size 8px -> Tends to be title
    s8_wb2_elem = soup.find_all(style=lambda value: value and any(style in value for style in styles))

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s8_wb2_elem]

    return [text_content[0].split("doi.org")[1]]

def get_from_springerapi(doi):
    """
    Fetches information from Springer API based on DOI.

    Parameters:
    doi (str): The Digital Object Identifier.

    Returns:
    tuple: A tuple containing author information, journal name, publication date, and subjects.
    """
    api_url = "http://api.springernature.com/metadata/json/doi{}?api_key=559b3c54b224f61ceb4ba285528a1461".format(doi)

    response = requests.get(api_url)

    json = response.json()

    # print(json["records"][0].keys())
    # title = json["records"][0]["title"]
    if not json["records"]:
        warning_message = f"Unable to fetch any information from given doi: '{doi}' -> Implies problems with API or DOI ..."
        logging.warning(warning_message)
        authors, journal, date, subjects, abstract = ["no_info"]
    else:
        authors = json["records"][0]["creators"]
        journal = json["records"][0]["publicationName"]
        date = json["records"][0]["publicationDate"]
        subjects = json["records"][0]["subjects"]
        abstract = json["records"][0]["abstract"]
    
    return authors, journal, date, subjects, abstract

def get_authors_and_affiliations(soup, styles_au, styles_nu, styles_af, letter_flag = False): # Doesn't work when there is multiple rows of authors
    """
    Extracts authors and their affiliations from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.
    style (String List): List of strings containing specific style that corresponds to authors, affiliations.

    Returns:
    tuple: A tuple containing author-affiliation pairs and affiliation information.
    """
    elements = soup.find_all(style=lambda value: value and (any(style in value for style in styles_au) or any(style in value for style in styles_nu)))
    authors_and_affiliations = []

    current_author = ""
    current_affiliation = ""

    for elem in elements:
        # Check if font-size is 12px (author names)
        if 'font-size:{}'.format(re.findall(r"font-size:(\d+px)", styles_au[0])[0]) in elem.get('style', ''):
            if current_author and current_affiliation:
                if len(current_author) < 40:
                    authors_and_affiliations.append((current_author.replace("and", "").replace("&", "").strip(), current_affiliation.strip()))
                current_author = ""
                current_affiliation = ""
            current_author += elem.get_text(separator=' ', strip=True) + " "
        # Check if font-size is 6px (affiliations)
        elif 'font-size:{}'.format(re.findall(r"font-size:(\d+px)", styles_nu[0])[0]) in elem.get('style', ''):
            current_affiliation += elem.get_text(separator=' ', strip=True) + " "
    # Append the last author and affiliation pair
    if current_author and current_affiliation:
        for i, letter in enumerate(current_affiliation):
            if not current_affiliation[i+1].isnumeric() and current_affiliation[i+1] != ",":
                current_affiliation = current_affiliation.split(" ")[0]
                break
        if len(current_author) < 40:    
            authors_and_affiliations.append((current_author.replace("and", "").replace("&", "").strip(), current_affiliation.strip()))

    # print(authors_and_affiliations)

    # To get the number of affiliations
    # affil_list = [int(num) for _, affil in authors_and_affiliations for num in affil.split(",")] # OLD
    affil_list = []
    for _, affil in authors_and_affiliations:
        for num in affil.split(","):
            try:
                affil_list.append(int(num))
            except ValueError:
                warning_message = f"Unable to convert '{num}' to an integer. Skipping... -> Implies problems with affiliations ..."
                logging.warning(warning_message)
                pass  # Skip and continue if conversion fails

    # For affiliation names
    s8_wb_elem = soup.find_all(style=lambda value: value and any(style in value for style in styles_af))
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s8_wb_elem]
    # print(text_content[:max(affil_list)])

    try:
        affiliation = [(i+1, text_content[i]) for i in range(max(affil_list))]
    except:
        warning_message = f"Unable to use max function. Skipping... -> Implies problems with affiliations ..."
        logging.warning(warning_message)
        affiliation = []
    return authors_and_affiliations, affiliation

def get_references(soup, styles):
    """
    Extracts and cleans references from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.
    style (String List): List of strings containing specific style that corresponds to references.
    
    Returns:
    list: A list containing cleaned references extracted from the HTML content.
    """

    # Find elements with font size 7px -> Tends to be reference
    s7_mpr_elem =  soup.find_all(style=lambda value: value and any(style in value for style in styles))

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s7_mpr_elem]

    # Initial heuristic
    a = " ".join(text_content)
    # print(a)
    ref = re.split(r"(?<!\d)\d{1,3}\.(?!\d)", a)
    to_pop = []

    # Clean initial references
    for i, r in enumerate(ref):
        if len(r) < 15:
            to_pop.append(i)
        elif len(r) > 300:
            ref[i] = " ".join(re.split(r"(\(\d{3,}\)\.)", ref[i])[:2])
            if len(ref[i]) > 300:
                to_pop.append(i)

    # Remove unwanted indexes
    to_pop.reverse()  # Reversing the list to delete indices from the end to avoid index errors
    for i in to_pop:
        del ref[i]

    return ref

def get_content(soup, styles):
    """
    Extracts content from HTML soup based on font size criteria.

    Args:
    soup: BeautifulSoup object of the HTML content
    style (String Pattern): Regex pattern containing specific style that corresponds to content.    

    Returns:
    content (str): Extracted text content from elements with font size 9px, minimizing extra spaces and hyphen removal.
    """

    # Find elements with font size 9px -> Tends to be content
    pattern = re.compile(r'{}'.format(styles[0]))

    s9_mpr_elem = soup.find_all(style=lambda value: value and pattern.search(value))

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s9_mpr_elem]


    content = " ".join(text_content)
    content = re.sub(r"[ ]+", " ", content)
    content = re.sub(r"- ", "", content)
    
    return content

# Added for ehs

def get_doi_regex(soup, styles, regex="doi.org(\/[\d.\/\w-]+)"):
    """
    Extracts DOI from text using a specified regex pattern.

    Args:
        soup (BeautifulSoup): Parsed HTML content.
        style (str): Style attribute value used to identify specific elements.
        regex (str, optional): Regular expression pattern to match DOIs.
            Defaults to "doi.org(\/[\d.\/\w-]+)".

    Returns:
        re.Match or None: A regex match object containing the found DOI,
            or None if no DOI is found in the text content.
    """
    
    # Find elements with font size 8px -> Tends to be title
    s8_wb2_elem =  soup.find_all(style=lambda value: value and any(style in value for style in styles))

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s8_wb2_elem]
    # print(text_content)
    # Find doi with regex
    doi = re.search(regex, " ".join(text_content))
    
    return [doi.group(1) if doi else "no_doi"]
    
def get_from_doi2bibapi(doi):
    """
    Retrieves information from a DOI using doi2bib API.

    Args:
        doi (str): DOI (Digital Object Identifier) for the publication.

    Returns:
        tuple: A tuple containing information extracted from the DOI.
            The tuple contains:
            - authors (str): Authors of the publication.
            - journal (str): Journal where the publication was published.
            - date (str): Year of publication.
            - subjects (str): Subjects or categories related to the publication.
            - abstract (str): Abstract of the publication.
    """
    
    # Remove first slash if present
    if doi[0] == "/":
        doi = doi[1:]
        
    # Use CLI via subprocess
    res = subprocess.run(['doi2bib', doi], capture_output=True)
    byte = res.stdout.strip(b"\n")

    # Clen text from newlines and trailing whitespaces
    text = re.sub("[ \n]+", " ", byte.decode("utf-8"))
    text = re.sub(" ,", ",", text)

    # Define a regular expression pattern to extract key-value pairs
    pattern = r'(\w+)\s*=\s*{([^{}]+)}'

    # Find all matches of key-value pairs
    matches = re.findall(pattern, text)

    # Create a dictionary from matches
    result = {key: value for key, value in matches}
    try:
        authors = result["author"]
        journal = result["journal"]
        date = result["year"]
    except:
        warning_message = "Information not fetched, implies problem with DOI or API -> Defaulting to empty values ..."
        logging.warning(warning_message)
        authors = "no_authors"
        journal = "no_journal"
        date = "no_date"
    
    subjects = "no_subjects"
    abstract = "no_abstract"

    return authors, journal, date, subjects, abstract

# Added for enerpol

def get_authors_and_affiliations_by_author(soup, styles_au, styles_nu, styles_af): # Doesn't work when there is multiple rows of authors
    """
    Extracts authors and their affiliations from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.
    style (String List): List of strings containing specific style that corresponds to authors, affiliations.

    Returns:
    tuple: A tuple containing author-affiliation pairs and affiliation information.
    """
    # Authors
    elements = soup.find_all(style=lambda value: value and any(style in value for style in styles_au))
    
    authors = []
    for elem in elements:
        temp = elem.get_text(separator=' ', strip=True).replace(",", "").strip()
        if temp:
            authors.append(temp)
    
    text = soup.get_text(separator= ' ', strip=True)

    # Affiliations search between authors
    affiliations_num = []
    for i in range(len(authors)-1):

        regex = "{}\s+(.*?)\s+{}".format(authors[i].replace(".", "\."), authors[i+1].replace(".", "\."))

        temp = re.findall(regex, text)
        # print(len(temp))
        if len(temp) == 0:
            affiliations_num.append(["no_affiliation"])
        elif len(temp[0]) < 16:
            affiliations_num.append(temp)
        else:
            affiliations_num.append(["no_affiliation"])
    affiliations_num.append(["no_affiliation"])
    # print(authors)
    # print(affiliations_num)
    
    # Affiliation names
    affil_elements = soup.find_all(style=lambda value: value and any(style in value for style in styles_af))
    
    affiliations_text = [elem.get_text(separator=' ', strip=True) for elem in affil_elements]
    # print(affiliations_text)
    
    # Unique affiliation marks (a, b, 1, 2 ...)
    affiliations_list = []
    for affiliation in affiliations_num:
        for a in affiliation[0].split(","):
            if a != "no_affiliation":
                affiliations_list.append(a.strip())
                
    affiliations_list = sorted(af for af in set(affiliations_list) if af.isalpha())
    
    # Connect Affiliation mark with text
    affiliation = []
    for i, affil in enumerate(affiliations_list):
        affiliation.append((affil, affiliations_text[i]))
    
    # COnnect author with it's affiliations
    authors_and_affiliations = []
    for i, auth in enumerate(authors):
        authors_and_affiliations.append((auth, affiliations_num[i]))
        
    return authors_and_affiliations, affiliation


def get_references_nonumber(soup, ref_title_styles, ref_styles):
        
    # Find the span containing 'References' with the specific style attribute
    reference_span = soup.find(style=lambda value: value and any(style in value for style in ref_title_styles))
    # while reference_span.get_text()
    while not re.search("^References[\s]*\n", reference_span.text):
        # print(reference_span.text)
        reference_span = reference_span.find_next()
    # print(reference_span)
    ref = ""
    while not isinstance(reference_span.find_next(style=lambda value: value and any(style in value for style in ref_styles)), type(None)):
        reference_span = reference_span.find_next(style=lambda value: value and any(style in value for style in ref_styles))
        if re.search(r"^[A-Z]", reference_span.text):
            ref += "\n" + reference_span.text
        else:
            ref += reference_span.text
    
    # print(ref)
    
    ref = ref.split("\n\n")
    
    for i in range(len(ref)):
        ref[i] = ref[i].replace("\n", " ")
    
    return ref
