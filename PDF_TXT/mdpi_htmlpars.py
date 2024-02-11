"""
MDPI html parsing
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



DIR = "./SAMPLE/MDPI/"

data_list = []
folders = listdir(DIR)
faults = []

skip_samples = ["A New Open Access Journal", 
                "Acknowledgment to Reviewers" ,
                "Acknowledgement to Reviewers", 
                "Earth—An Open Access Journal", 
                "Acknowledgment to the Reviewers",
                "Scientific Open Access Journal",
                "Book Review",
                "Sandra Brown (1944–2017): A Distinguished Tropical Ecologist"]
for folder in tqdm(folders):
    sub_DIR = DIR + folder + "/"

    samples = listdir(sub_DIR)
    for sample in tqdm(samples):
        print("\n")
        print(sample)
        # Read from html file
        with open(sub_DIR + sample, "r") as f:
            html = f.read()
        
        # Load as soup object
        soup = BeautifulSoup(html, 'html.parser')
        
        # Get Title
        title = soup.find("h1", {'class': "title hypothesis_container"}).get_text().strip()
        print(title)

        # Skip samples
        if any(skip in title for skip in skip_samples):
            continue

        # Get Abstract
        try:
            abstract = " ".join(
                [abs.get_text() for abs in soup.find("section", {"class": "html-abstract"}).find_all(
                    "div", {"class": "html-p"}
                    )
                ])  
        except AttributeError:
            abstract = "no_abstract"
            faults.append(f"EXC :: no_abstract: {title}")

        # print(abstract)
        
        # Get Content, References and Tables
        content_div = soup.find("div", {"class": "html-article-content"})

        content_list = []
        for con in content_div.find_all("div", {"class": "html-p"}):
            if con.find("div", {"class": "html-table-wrap"}):
                continue
            else:
                content_list.append(con)
        
        
        content = " ".join([divcon.get_text() for divcon in content_list]) # Content
        # print(content)

        tables = [tab for tab in content_div.find_all("div", {"class": "html-table_show"})] # Tables
        # print(tables)

        references = [ref.get_text() for ref in content_div.find(
            "div", {"class": "html-back"}
            ).find(
                "section", {"id": "html-references_list"}
                ).find_all(
                    "li"
                    )]
        # print(references)
        
        # Get Authors and Affiliations
        authors_div = content_div.find("div", {"class": "art-authors hypothesis_container"}).find_all("span", {"class": "inlineblock"})

        authors_and_affiliations = []
        authors = []
        for a in authors_div:
            try:
                au = a.find("span").get_text() # Contains Author names
            except AttributeError:
                au = a.find("div").get_text()
                faults.append(f"EXC :: no_author_span: {title}")
            nu = a.find("sup").get_text() # Contains affiliations

            authors.append(au)
            authors_and_affiliations.append((au, nu))
        # print(authors_and_affiliations)
        # print(authors)
            
        affiliations_div = content_div.find("div", {"class": "art-affiliations"}).find_all("div", {"class": "affiliation"})
        
        affiliations = []
        for af in affiliations_div:
            affil = af.get_text().strip().split("\n") # Separate number and affiliations text
            try: 
                affiliations.append((affil[0], affil[1]))
            except IndexError: # Fix when just 
                if len(affil) < 2:
                    affiliations.append(("1", affil[0]))
        # print(affiliations)
            

        # Get Keywords
        keywords_div = content_div.find("div", {"id": "html-keywords"})
        
        try: 
            keywords_text = keywords_div.get_text().split(":")

            if len(keywords_text) > 1:
                keywords = re.split(r"(,|;)", keywords_text[1]) # If "Keywords: "
            else:
                keywords = re.split(r"(,|;)", keywords_text)

            keywords = [k.strip() for k in keywords if len(k) > 1] # Clean newlines, commas, and semicolons
            # print(keywords)
        except AttributeError:
            keywords = "no_keywords"
            faults.append(f"EXC :: no_keywords: {title}")

        # Get DOI
        doi = content_div.find("div", {"class": "bib-identity"}).get_text()
        # print(doi)

        # Get Date
        date = content_div.find("div", {"class": "pubhistory"}).get_text()
        # print(date)
        
        # Structure
        paper_data = {
                "Title": title,
                "Authors_and_Affiliations": authors_and_affiliations,
                "Affiliations": affiliations,
                "DOI": doi,
                "Authors": authors,
                "Journal": doi.split()[0],
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
    df.to_pickle(f"./PARS_OUT/test_mdpi{folder}.pickle")