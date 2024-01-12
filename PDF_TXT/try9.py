from bs4 import BeautifulSoup
import re
from functions import *

DIR = "./SAMPLE/GCB/"
# samples = listdir(DIR) 
sample = "Global Change Biology - 2023 - Sun - Machine learning for accelerating process‐based computation of land biogeochemical(1).pdf"

trouble_1 = []
trouble_2 = []
invalid = []

# print(10*"---")
# print(sample)
DIR = "./SAMPLE/GCB/"
html = pdf2html(target=DIR+sample)
soup = BeautifulSoup(html, 'html.parser')

elem = soup.find_all('div')[-1]
# print(last_elem)

while type(elem) != type(None):
        if re.search("^(?i)r\s*e\s*f\s*e\s*r\s*e\s*n\s*c\s*e\s*s\n+", elem.text):   
            # print(elem.text)
            break
        elem = elem.find_previous()

add_custom_tag_after_element(soup, elem, "reftag", "STOP CONTENT EXTRACTION HERE IN THE NAME OF GOD", {'style': 'font-family: TimesNewReference; font-size:69px'})
print(soup)