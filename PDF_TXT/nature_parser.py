"""
Functions to use with Nature papers
"""

from bs4 import BeautifulSoup
import requests

def get_title(soup):

    # Find elements with font size 24 -> Tends to be title
    s24elem = soup.find_all(style=lambda value: value and 'font-size:24px' in value)

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s24elem]

    return text_content

def get_doi(soup):
    
    # Find elements with font size 8px -> Tends to be title
    s8_wb2_elem = soup.find_all(style=lambda value: value and 'font-family: Whitney-Semibold2; font-size:8px' in value)

    # Extract text content from the found elements
    text_content = [elem.get_text(separator=' ', strip=True) for elem in s8_wb2_elem]

    return [text_content[0].split("doi.org")[1]]

def get_from_springerapi(doi):


    api_url = "http://api.springernature.com/metadata/json/doi{}?api_key=559b3c54b224f61ceb4ba285528a1461".format(doi)

    response = requests.get(api_url)

    json = response.json()

    # print(json["records"][0].keys())
    # title = json["records"][0]["title"]
    authors = json["records"][0]["creators"]
    journal = json["records"][0]["publicationName"]
    date = json["records"][0]["publicationDate"]
    subjects = json["records"][0]["subjects"]
    
    return authors, journal, date, subjects

# def get_authors()