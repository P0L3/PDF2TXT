"""
Functions to use with Nature papers
"""

from bs4 import BeautifulSoup
import requests
import re
import logging

# Works on 80% -> not open access papers
def get_title(soup):
    """
    Extracts the title(s) from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.

    Returns:
    list: A list of titles extracted from the provided HTML.
    """
    # Find elements with font size 24 -> Tends to be title
    s24elem = soup.find_all(style=lambda value: value and 'font-size:24px' in value)

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s24elem]

    return text_content

def get_doi(soup):
    """
    Extracts the DOI(s) from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.

    Returns:
    list: A list containing DOI(s) extracted from the provided HTML.
    """
    # Find elements with font size 8px -> Tends to be title
    s8_wb2_elem = soup.find_all(style=lambda value: value and 'font-family: Whitney-Semibold2; font-size:8px' in value)

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
    authors = json["records"][0]["creators"]
    journal = json["records"][0]["publicationName"]
    date = json["records"][0]["publicationDate"]
    subjects = json["records"][0]["subjects"]
    abstract = json["records"][0]["abstract"]
    
    return authors, journal, date, subjects, abstract

def get_authors_and_affiliations(soup): # Doesn't work ehn there is multiple rows of authors
    """
    Extracts authors and their affiliations from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.

    Returns:
    tuple: A tuple containing author-affiliation pairs and affiliation information.
    """
    elements = soup.find_all('span', style=lambda value: value and ('font-family: Whitney-Semibold; font-size:12px' in value or 'font-family: Whitney-Semibold; font-size:6px' in value))

    authors_and_affiliations = []

    current_author = ""
    current_affiliation = ""

    for elem in elements:
        # Check if font-size is 12px (author names)
        if 'font-size:12px' in elem.get('style', ''):
            if current_author and current_affiliation:
                authors_and_affiliations.append((current_author.replace("and", "").strip(), current_affiliation.strip()))
                current_author = ""
                current_affiliation = ""
            current_author += elem.get_text(separator=' ', strip=True) + " "
        # Check if font-size is 6px (affiliations)
        elif 'font-size:6px' in elem.get('style', ''):
            current_affiliation += elem.get_text(separator=' ', strip=True) + " "

    # Append the last author and affiliation pair
    if current_author and current_affiliation:
        for i, letter in enumerate(current_affiliation):
            if not current_affiliation[i+1].isnumeric() and current_affiliation[i+1] != ",":
                current_affiliation = current_affiliation.split(" ")[0]
                break
        authors_and_affiliations.append((current_author.replace("and", "").strip(), current_affiliation.strip()))

    print(authors_and_affiliations)

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


    s8_wb_elem = soup.find_all('span', style=lambda value: value and ('font-family: Whitney-Book; font-size:8px' in value))
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s8_wb_elem]
    # print(text_content[:max(affil_list)])

    try:
        affiliation = [(i+1, text_content[i]) for i in range(max(affil_list))]
    except:
        warning_message = f"Unable to use max function. Skipping... -> Implies problems with affiliations ..."
        logging.warning(warning_message)
        affiliation = []
    return authors_and_affiliations, affiliation

def get_references(soup):
    """
    Extracts and cleans references from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.

    Returns:
    list: A list containing cleaned references extracted from the HTML content.
    """

    # Find elements with font size 7px -> Tends to be reference
    s7_mpr_elem = soup.find_all(style=lambda value: value and 'font-family: MinionPro-Regular; font-size:7px' in value)

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s7_mpr_elem]

    # Initial heuristic
    a = " ".join(text_content)
    ref = re.split(r"\d+\.(?!\d)", a)
    to_pop = []

    # Clean initial references
    for i, r in enumerate(ref):
        if len(r) < 40:
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

def get_content(soup):
    """
    Extracts content from HTML soup based on font size criteria.

    Args:
    - soup: BeautifulSoup object of the HTML content

    Returns:
    - content (str): Extracted text content from elements with font size 9px, minimizing extra spaces and hyphen removal.
    """

    # Find elements with font size 9px -> Tends to be content
    s9_mpr_elem = soup.find_all(style=lambda value: value and 'font-family: MinionPro-Regular; font-size:9px' in value)

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s9_mpr_elem]


    content = " ".join(text_content)
    content = re.sub(r"[ ]+", " ", content)
    content = re.sub(r"- ", "", content)
    
    return content


# For the open access
def get_title_2(soup):
    """
    Extracts the title(s) from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.

    Returns:
    list: A list of titles extracted from the provided HTML.
    """
    # Find elements with font size 24 -> Tends to be title
    s24elem = soup.find_all(style=lambda value: value and 'font-family: Harding-Bold; font-size:26px' in value)

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s24elem]

    return text_content

def get_doi_2(soup):
    "font-family: GraphikNaturel-Medium2; font-size:8px"

    """
    Extracts the DOI(s) from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.

    Returns:
    list: A list containing DOI(s) extracted from the provided HTML.
    """
    # Find elements with font size 8px -> Tends to be title
    s8_wb2_elem = soup.find_all(style=lambda value: value and 'font-family: GraphikNaturel-Medium2; font-size:8px' in value)

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s8_wb2_elem]

    return [text_content[0].split("doi.org")[1]]