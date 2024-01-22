"""
MDPI html parsing
"""
from bs4 import BeautifulSoup
import re
from os import listdir
import pandas as pd
from tqdm import tqdm
import logging
from parser_html import *
import requests
from functions import *


DIR = "./SAMPLE/MDPIAIR/"

samples = listdir(DIR)
for sample in tqdm(samples):
    
    # Read from html file
    with open(DIR+sample, "r") as f:
        html = f.read()
    
    # Load as soup object
    soup = BeautifulSoup(html, 'html.parser')
    
    # Get title
    title = soup.find("h1", {'class': "title hypothesis_container"}).get_text()
    print(title)
    
    # Get Abstract
    abstract = " ".join(
        [abs.get_text() for abs in soup.find("section", {"class": "html-abstract"}).find_all(
            "div", {"class": "html-p"}
            )
        ])
    print(abstract)
    
    

    break

    # paper_data = {
    #         "Title": title,
    #         "Authors_and_Affiliations": authors_and_affiliations,
    #         "Affiliations": affiliations,
    #         "DOI": doi,
    #         "Authors": authors,
    #         "Journal": journal,
    #         "Date": date,
    #         "Subjects": subjects,
    #         "Abstract": abstract,
    #         "References": references,
    #         "Content": content,
    #         "Keywords": keywords,
    #     }
    
