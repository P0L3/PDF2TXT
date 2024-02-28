"""
Functions to use with Nature papers
"""

from bs4 import BeautifulSoup
import requests
import re
import logging
import subprocess
from functions import *
from api_keys import *


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
    print(text_content)
    return [text_content[0].split("doi.org")[1]]

def get_from_springerapi(doi):
    """
    Fetches information from Springer API based on DOI.

    Parameters:
    doi (str): The Digital Object Identifier.

    Returns:
    tuple: A tuple containing author information, journal name, publication date, and subjects.
    """
    api_url = "http://api.springernature.com/metadata/json/doi{}?api_key={}".format(doi, api_key_springer)

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
    
    sizes = list(set(re.findall(r"font-size:\[*(\d+)\]*px", styles[0]))) # to get all sizes for extra fonts
    
    # Avoiding regex size situations -> Every regex size has to have at least 3 instances
    if len(sizes) == 1:
        if len(sizes[0]) > 2:
            sizes = [s for s in sizes[0]]
        
        
    extra_fonts = ["fb", "20"]

    extra = ["font-family: TimesNewReference; font-size:69px"]

    for s in sizes:
        for font in extra_fonts:
            extra.append(f"font-family: {font}; font-size:{s}px")
    # print(soup)
    s9_mpr_elem = soup.find_all(style=lambda value: value and (pattern.search(value) or value in extra))
    # print(s9_mpr_elem)
    # Extract text content from the found elements
    #text_content = [elem.get_text(separator=' ', strip=True) for elem in s9_mpr_elem]

    text_content = []
    for elem in s9_mpr_elem:
        text = elem.get_text(separator=' ', strip=True) #separator=' ', strip=True
        # print(text)
        text_content.append(text)
        
        if elem.text == "STOP CONTENT EXTRACTION HERE IN THE NAME OF GOD":
            print("Found references, stoping content extraction ...")
            break
    content = " ".join(text_content)
    content = re.sub(r"[ ]+", " ", content)
    content = re.sub(r"- ", "", content)

    content = content.split("STOP CONTENT EXTRACTION HERE IN THE NAME OF GOD")[0]
    
    # Clean ligations
    # print(type(content))
    print("Cleaning ...")
    content = fi_cleaner(content)
    print("Done ...")

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
    # print(" ".join(text_content))
    # Find doi with regex
    doi = re.search(regex, " ".join(text_content).replace("/ ", "/")) # hot fix for fractured DOI
    
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
    styles_au (List of Strings): List of strings specifying the style corresponding to authors.
    styles_nu (List of Strings): List of strings specifying the style corresponding to author numberings.
    styles_af (List of Strings): List of strings specifying the style corresponding to affiliations.

    Returns:
    tuple: A tuple containing author-affiliation pairs and affiliation information.

    This function aims to extract authors and their respective affiliations based on the provided
    styles for authors, author numberings, and affiliations within the parsed HTML represented by
    the BeautifulSoup object 'soup'.

    It searches for elements representing authors and their respective styles, retrieves their
    textual content, and gathers information about their affiliations based on the proximity
    of authors to affiliation markers.

    It returns a tuple containing two lists: 'authors_and_affiliations' contains tuples of authors
    and their corresponding affiliation information, while 'affiliation' contains tuples of unique
    affiliation markers and their respective affiliation text.
    """
    # Authors
    elements = soup.find_all(style=lambda value: value and any(style in value for style in styles_au))
    
    authors = []
    for elem in elements:
        temp = elem.get_text(separator=' ', strip=True).replace(",", "").strip()
        if temp:
            authors.append(temp)
    
    print(authors)
    text = soup.get_text(separator= ' ', strip=True)
    # print(text)
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
    # print(10*"-", affiliations_text)
    
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

def get_references_nonumber(soup, ref_title_styles, ref_styles, ref_title_regex="^References[\s]*\n"):
    """
    Extracts references without numbering from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.
    ref_title_styles (List of Strings): List of strings specifying the style attribute of the 'References' title.
    ref_styles (List of Strings): List of strings specifying the style attribute for reference items.

    Returns:
    List: A list containing extracted references without numbering.

    This function aims to extract references without numbering from the provided BeautifulSoup object 'soup'.
    It searches for the 'References' title span using the specified style attributes, then iterates through
    subsequent spans with reference styles to extract the text of references.

    The extracted references are cleaned by splitting on double newline characters and replacing single newlines
    within each reference with spaces before being returned as a list.
    """
    
    # Find the span containing 'References' with the specific style attribute
    reference_span = soup.find(style=lambda value: value and any(style in value for style in ref_title_styles))
    # while reference_span.get_text()
    if type(reference_span) != type(None):
        while not re.search(ref_title_regex, reference_span.text):
            # print(reference_span.text)
            reference_span = reference_span.find_next()
            if type(reference_span) == type(None):
                return "no_references"
    else:
        return "no_references"
    # print(reference_span)
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

def get_keywords(soup, keyword_title_styles, keyword_title_regex="^[Kk]eywords:[\s]*\n*", keyword_styles=[], obj = "div"): # Misses half keywords if they are in multiple lines, strugles with style changes
    """
    Extracts keywords from a BeautifulSoup object.

    Parameters:
    soup (BeautifulSoup): The BeautifulSoup object containing parsed HTML.
    keyword_title_styles (List of Strings): List of strings specifying the style attribute of the 'Keywords' title.
    keyword_title_regex (str, optional): Regular expression pattern to match the 'Keywords' title. Defaults to "^[Kk]eywords:[\s]*\n*".
    keyword_styles (List of Strings, optional): List of strings specifying the style attribute of keywords. Defaults to [].
    obj (str, optional): The type of HTML tag to search for keywords within. Defaults to "div".

    Returns:
    List or str: A list of extracted keywords or "no_keywords" if not found.

    This function aims to extract keywords from the provided BeautifulSoup object 'soup'. It searches for the 'Keywords'
    title span using the specified style attributes and retrieves the text following the title, assuming it begins
    with 'Keywords:' or 'keywords:'.

    If the 'Keywords' title is not found, it returns "no_keywords". Otherwise, it splits the extracted text by newline
    characters and returns a list of extracted keywords.

    The function also attempts to handle cases where keywords might be split across multiple lines or where there are
    style changes within the keyword section. If specific keyword styles are provided and no keywords are found initially,
    it will attempt to locate keywords using those styles within the specified HTML tag type.

    Example:
    >>> keywords = get_keywords(soup, ["font-weight: bold;"])
    """
    # Find the span containing 'Keywords:' with the specific style attribute
    keywords_span = soup.find(style=lambda value: value and any(style in value for style in keyword_title_styles))
    # print(keywords_span)
    keywords = ""
    if type(keywords_span) != type(None):
        while not re.search(keyword_title_regex, keywords_span.text):
            # print(keywords_span.text)
            keywords_span = keywords_span.find_next()
            # print(keywords_span.text)
            if type(None) == type(keywords_span):
                keywords = "no_keywords"
                break
    else:
        keywords = "no_keywords"
    # print(keywords_span)
    if not keywords == "no_keywords":
        keywords = keywords_span.text.split("\n")
        # print(keywords)
        # Fix if containing "Keywords"
        if re.search(keyword_title_regex, keywords[0]):
            keywords.extend(re.sub(keyword_title_regex, "",keywords[0]).split(","))
            keywords.pop(0)

    # print(keywords)
    # Fix for specific keyword styles if no keywords found
    if obj == "div":
        if "".join(keywords) == "" and len(keyword_styles) > 0:
            keywords = ""
            keywords_span = keywords_span.find_next(obj)
            # print(keywords_span)
            while keywords_span.span["style"] in keyword_styles:
                
                keywords += keywords_span.text
                keywords_span = keywords_span.find_next(obj)
    elif obj == "span":
        if "".join(keywords) == "" and len(keyword_styles) > 0:
            keywords = ""
            keywords_span = keywords_span.find_next(obj)
            # print(keywords_span)
            while keywords_span["style"] in keyword_styles:
                
                keywords += keywords_span.text
                keywords_span = keywords_span.find_next(obj)

    return keywords

# Added for gcb

def char_number2words_pages(charnum, fontsize = 12):
    """
    Converts a given character count to an estimated number of words and pages.

    Parameters:
    - charnum (int): The number of characters in the document.

    Returns:
    - bool: True if the estimated number of pages is greater than or equal to 10, False otherwise.

    The conversion is based on an assumed average of 6.5 characters per word and 5 characters per word, 
    as well as an assumed average of 256 words per page and 250 words per page.

    Example:
    >>> char_number2words_pages(1000)
    Words: 153.846 - 200.000	Pages: 0.599 - 0.800
    False
    """
    fontsize = int(fontsize)
    charnum = charnum/(12/(fontsize-1)) # Original estimation is made for font size 12 - Heuristic etimation

    if charnum:
        print("Words: {:.3f} - {:.3f}\tPages: {:.3f} - {:.3f}".format(charnum/6.5, charnum/5, (charnum/6.5)/256, (charnum/5)/250))

    return (charnum/5)/250 >= 10

def get_abstract(soup, abstract_title_styles): # Doesn't work when style interuptions are present, e.g. CO2 -> when subscripts are present 
    """
    Extracts the abstract text from a given HTML soup.

    Args:
        soup (BeautifulSoup): The HTML soup to search for the abstract text.
        abstract_title_styles (list): A list of style attributes to search for in the 'Abstract' span element.

    Returns:
        str: The abstract text found in the 'Abstract' span element, or "no_abstract" if no abstract text is found.
    """
    # Find the span containing 'Abstract' with the specific style attribute
    abstract_span = soup.find(style=lambda value: value and any(style in value for style in abstract_title_styles))

    abstract = ""
    if type(abstract_span) == type(None):
        warning_message = f"Unable to extract abstract -> Implies possibility of no Abstract at all ..."
        logging.warning(warning_message)
        return "no_abstract"

    while not re.search("^[Aa]bstract[\s]*\n*", abstract_span.text):
        # print(abstract_span.text)
    # print(abstract_span.text)
        abstract_span = abstract_span.find_next()
        if type(abstract_span) == type(None):
            abstract = "no_abstract"
            break
    # print(abstract_span)
    if not abstract == "no_abstract":
        abstract = abstract_span.find_next("span").text
    # print(abstract)

    return abstract

# Added for jclimate

def get_affiliations(soup, styles):
    """
    Extracts affiliations from a BeautifulSoup object based on specified styles.

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.
    - styles (list of str): A list of CSS styles used to identify relevant elements.

    Returns:
    - list of str: A list containing the text content of elements matching the specified styles.

    The function finds all HTML elements with styles matching any of the specified styles in the 'styles' list
    within the BeautifulSoup object ('soup'). It then extracts the text content of these elements and returns
    a list containing the affiliations.

    Example:
    >>> soup = BeautifulSoup(html_content, 'html.parser')
    >>> styles_to_search = ['style1', 'style2']
    >>> affiliations = get_affiliations(soup, styles_to_search)
    Number of affiliations: 3
    ['Affiliation 1', 'Affiliation 2', 'Affiliation 3']
    """
    s8_wb2_elem = soup.find_all(style=lambda value: value and any(style in value for style in styles))


    text_content = [elem.text for elem in s8_wb2_elem]
    # print("Number of affiliations: ", len(text_content))

    return text_content

# Added for jgra
