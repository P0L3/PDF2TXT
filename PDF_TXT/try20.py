"""Check if ligatures exist in html file"""

from os import listdir
from bs4 import BeautifulSoup
import re

# Load ligatures list
with open("ligatures_list.txt") as f:
    ligatures = f.read()
ligatures_list = ligatures.split()
print(ligatures_list)

# Load directory
DIR = "./TEST/"
SUBDIR = listdir(DIR)

# Function to check if any string from the list is present in a text element
def check_strings_in_text(text, strings):
    for string in strings:
        # Using regular expression to find a match
        if re.search(string, text):
            print(string)
            return True
    return False


# Iterate
for j in SUBDIR:
    files = listdir(DIR+j)
    print()
    print(30*"-")
    print(j)
    print(30*"-")
    for file in files:
        print(file)
        with open(DIR+j+"/"+file) as h:
            soup =  BeautifulSoup(h.read(), 'html.parser')
            
        current_element = soup.find("span")

        # Loop to iterate through all elements
        while current_element is not None:
            # Process the current element (print or do other operations)
            if check_strings_in_text(current_element.text, ligatures_list):
                print(current_element.find_previous("span"))
                print()
                print(current_element)
                print()
                print(current_element.find_next("span"))
                # pass
                exit()
            # Move to the next element
            current_element = current_element.find_next("span")


# Output to test16.txt