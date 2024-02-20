"""
EcoApp HTML pars
"""
from bs4 import BeautifulSoup
import re
from os import listdir, mkdir
import pandas as pd
from tqdm import tqdm
import logging
from parser_html import *
import requests
from functions import *



DIR = "./SAMPLE/ECOAPP/"

data_list = []
folders = listdir(DIR)
faults = []
skip_samples = []

samples = listdir(DIR)
for sample in tqdm(samples):
    print("\n")
    print(sample)
    # Read from html file
    with open(DIR + sample, "r") as f:
        html = f.read()

    # Load as soup object
    soup = BeautifulSoup(html, 'html.parser')
    # print(soup)
    
    # Get Title
    title = soup.find("h1", {'class': "citation__title"}).get_text().strip()
    print("\n", title)

    # Skip samples
    if any(skip in title for skip in skip_samples):
        continue

    # Get Abstract
    try:
        abstract = " ".join(
            [abs.get_text() for abs in soup.find("section", {"class": "article-section__abstract"}).find_all(
                "div"
                )
            ])  
    except AttributeError:
        abstract = "no_abstract"
        faults.append(f"EXC :: no_abstract: {title}")
    # print("\n", abstract)

    # Get Content, References and Tables
    paper_div = soup.find("article") # Whole content with authors etc
    article_div = paper_div.find("article") # Ppaer textual content, Abstract etc
    # print(article_div)

    content_list = []
    try:
        for con in article_div.find_all("p"):
            content_list.append(con)

        content = " ".join([divcon.get_text() for divcon in content_list]) # Content
        
    except AttributeError:
        content = "no_content"
        faults.append(f"EXC :: no_content: {title}")
    # print(content)

    # tables = [tab for tab in article_div.find_all("div", {"class": "article-table-content"})] # Tables
    # print(tables)

    references = "no_references"
    # print(references)
    
    # Get Authors and Affiliations
    authors_div = paper_div.find("div", {"class": "citation"}).find_all("div", {"class": "author-info accordion-tabbed__content"})
    # print(authors_div)

    # For output
    authors_and_affiliations = []
    authors = []
    affiliations = []

    # For midsteps
    authors_affil_dict = {}
    affils_list = []

    # Authors
    for a in authors_div:
        author = a.find("p", {"class": "author-name"}).get_text()
        affils = [affil.get_text() for affil in a.find_all("p") if affil.get_text() != author]
        # print(author)
        affils_list.extend(affils) # Get all affiliations per author
        authors_affil_dict[author] = affils 
        authors.append(author) # Add to authors
    
    
    affils_list = list(set(affils_list)) # Clean duplicates

    # Affiliations
    for i, af in enumerate(affils_list):
        affiliations.append((i+1, af))

    # Authors and affiliations
    for aaf in authors_affil_dict:
        numbers = []

        for aff in authors_affil_dict[aaf]:
            numbers.append(str(affils_list.index(aff) + 1))

        affiliation_numbers = ", ".join(numbers)
        authors_and_affiliations.append((aaf, affiliation_numbers))


    # print(authors_and_affiliations, authors, affiliations)

    # Get Keywords
    keywords = []
    keywords_meta = soup.find_all("meta", {"name": "citation_keywords"})
    # print(keywords_div)
    
    try: 
        for k in keywords_meta:
            keywords.append(k["content"])
    except AttributeError:
        keywords = "no_keywords"
        faults.append(f"EXC :: no_keywords: {title}")
    
    # Get DOI
    doi = soup.find("meta", {"property": "og:url"})["content"].split("/doi")[1]
    # print(doi)

    # Get Date
    date = soup.find("span", {"class": "epub-date"}).get_text()
    # print(date)
    
    # Structure
    paper_data = {
            "Title": title,
            "Authors_and_Affiliations": authors_and_affiliations,
            "Affiliations": affiliations,
            "DOI": doi,
            "Authors": authors,
            "Journal": doi,
            "Date": date,
            "Subjects": "no_subjects",
            "Abstract": abstract,
            "References": references,
            "Content": content,
            "Keywords": keywords,
        }
    
    data_list.append(paper_data)
print(faults)

df = pd.DataFrame(data_list)
df.to_pickle(f"./PARS_OUT/test_ecoapp.pickle")