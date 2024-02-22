"""
PNAS HTML pars
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



DIR = "./SAMPLE/PNAS/"

data_list = []
folders = listdir(DIR)
faults = []
skip_samples = ["In This Issue"]

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
    title = soup.find("h1", {'property': "name"}).get_text().strip()
    print("\n", title)

    # Skip samples
    if any(skip in title for skip in skip_samples):
        continue

    # Get Abstract
    try:
        abstract = " ".join(
            [abs.get_text() for abs in soup.find("section", {"id": "abstract"}).find_all(
                "div", {"role": "paragraph"}
                )
            ])  
    except AttributeError:
        abstract = "no_abstract"
        faults.append(f"EXC :: no_abstract: {title}")
    # print("\n", abstract)

    # Get Content, References and Tables
    paper_div = soup.find("article") # Whole content with authors etc
    # print(paper_div)

    content_list = []
    try:
        for con in paper_div.find_all("div", {"role": "paragraph"}):
            content_list.append(con)

        content = " ".join([divcon.get_text() for divcon in content_list]) # Content
        
    except AttributeError:
        content = "no_content"
        faults.append(f"EXC :: no_content: {title}")
    # print("\n", content)

    # tables = [tab for tab in paper_div.find_all("div", {"class": "article-table-content"})] # Tables
    # print(tables)

    # References
    try:
        references = []
        bib_div = paper_div.find("section", {"id": "bibliography"})

        for bib in bib_div.find_all("div", {"class": "citation-content"}):
            references.append(bib.get_text())
    except AttributeError:
        references = "no_references"
    # print("\n", references)
    
    # Get Authors and Affiliations
    authors_div = soup.find("section", {"class": "core-authors"}).find_all("div", {"property": "author"})
    # print(authors_div)

    # For output
    authors_and_affiliations = []
    authors = []
    affiliations = []

    # For midsteps
    authors_affil_dict = {}
    affils_list = []

    # Authors
    """
    # <div id="con1" property="author" typeof="Person" data-expandable="item">
    #   <div class="heading" aria-controls="con1_content" aria-expanded="false" tabindex="0" role="button">
    #       <h5>
    #           <span property="givenName">Oleg</span> 
    #           <span property="familyName">Lukin</span>
    #           <sup class="xref">
    #               <a href="#cor1" role="doc-noteref">1</a>
    #           </sup> 
    #           <a href="mailto:o.lukin@ukrorgsynth.com" property="email" aria-label="Email address">o.lukin@ukrorgsynth.com</a>
    #           <i class="icon-arrow-up" aria-hidden="true"></i>
    #       </h5>
    #   </div>
    #   <div class="content" style="display: none;" role="region" id="con1_content">
    #       <div class="affiliations">
    #           <div property="affiliation" typeof="Organization">
    #               <span property="name">Institute of Polymers, Department of Materials, HCI G527, and</span>
    #           </div>
    #           <div property="affiliation" typeof="Organization">
    #               <span property="name">National Taras Shevchenko University, Volodymyrska Street 64, Kiev 01033, Ukraine; and</span>
    #           </div>
    #       </div>
    #       <div class="core-author-link">
    #           <a href="/authored-by/Lukin/Oleg">View all articles by this author</a>
    #       </div>
    #   </div>
    # </div>
    """
    
    for a in authors_div:
        author = a.find("span", {"property": "givenName"}).get_text() + " " + a.find("span", {"property": "familyName"}).get_text()
        affils = [affil.get_text() for affil in a.find_all("div", {"property": "affiliation"}) if affil.get_text() != author]
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


    # print("\n", authors_and_affiliations, authors, affiliations)

    # Get Keywords
    """
    <meta name="keywords" content="dendrimers,single-crystal X-ray,sulfonimides,supramolecular chemistry">
    """

    try:
        keywords = soup.find("meta", {"name": "keywords"})["content"].split(",")
    except TypeError:
        faults.append(f"EXC :: no_keywords: {title}")
        keywords= "no_keywords"
    # print("\n", keywords)
    

    # Get DOI
    doi = soup.find("div", {"class": "doi"}).get_text().split("/doi.org")[1]
    # print("\n", doi)


    # Get Date
    date = soup.find("div", {"class": "core-date-published"}).get_text()
    # print("\n", date)
    # Structure
    paper_data = {
            "Title": title,
            "Authors_and_Affiliations": authors_and_affiliations,
            "Affiliations": affiliations,
            "DOI": doi,
            "Authors": authors,
            "Journal": [doi],
            "Date": date,
            "Subjects": "no_subjects",
            "Abstract": abstract,
            "References": references,
            "Content": content,
            "Keywords": keywords,
            "Style": "html",
        }

    data_list.append(paper_data)
    
# with open("faults.txt", "w") as file:
#     for f in faults:
#         file.write("\n"+f)
# print(faults)

df = pd.DataFrame(data_list)
df.to_pickle(f"./PARS_OUT/test_pnas.pickle")