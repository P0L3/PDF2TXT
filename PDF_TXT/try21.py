"""Check if ligatures exist in pdf file"""

from os import listdir
from bs4 import BeautifulSoup
import re
import random
from functions import *
from tqdm import tqdm

# Load ligatures list
with open("ligatures_list.txt") as f:
    ligatures = f.read()
ligatures_list = ligatures.split()
print(ligatures_list)

# Load directory
DIR = "./SAMPLE/"
SUBDIR = listdir(DIR)

# Function to check if any string from the list is present in a text element
def check_strings_in_text(text, strings):
    for string in strings:
        # Using regular expression to find a match
        if re.search(string, text):
            # print(string)
            return True
    return False


# Iterate
for j in tqdm(SUBDIR[15:]):
    if j == "MDPI":
        continue
    files = listdir(DIR+j)
    print()
    print(30*"-")
    print(30*"-")
    print(j)
    print(30*"-")
    print(30*"-")

    files = random.sample(files, 20)
    for file in tqdm(files):

        if file.endswith("pdf"):
            html = pdf2html(target=DIR+j+"/"+file)

            if not html:
                continue
        
            soup =  BeautifulSoup(html, 'html.parser')

            print(30*"-")
            print(file)
            print(30*"-")
        else:
            continue 
        current_element = soup.find("span")

        # Remember already seen attributes
        already_seen = []

        # Loop to iterate through all elements
        while current_element is not None:
            # Process the current element (print or do other operations)
            if check_strings_in_text(current_element.text, ligatures_list):
                temp_0 = current_element.find_previous("span").attrs
                temp_1 = current_element.attrs
                try:
                    temp_2 = current_element.find_next("span").attrs
                except:
                    temp_2 = "NONEXT"

                if (temp_0, temp_1, temp_2) not in already_seen:
                    print()
                    print(temp_0)
                    # print()
                    print(temp_1)
                    # print()
                    print(temp_2)
                    # pass
                    already_seen.append((temp_0, temp_1, temp_2))

            # Move to the next element
            current_element = current_element.find_next("span")


# Output to test17.txt