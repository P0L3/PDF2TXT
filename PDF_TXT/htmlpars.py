"""
Nature html parsing
"""
from bs4 import BeautifulSoup
from nature_parser import get_title, get_doi, get_from_springerapi

target = "./TEST/NCLIMATE/s41558-020-00938-y_Heat_Tolerance_In_Ectotherms_Scales_Predictably_With_Body_Size_.html"

with open(target, 'r') as inf:
    html = inf.read()

soup = BeautifulSoup(html, 'html.parser')

title = get_title(soup)
print(title)


# # Find elements with font size 24 -> Tends to be title
# s12_ws_elem = soup.find_all(style=lambda value: value and 'font-family: Whitney-Semibold; font-size:12px' in value)
# print(s12_ws_elem)
# # Extract text content from the found elements
# text_content = [elem.get_text(separator=' ', strip=True) for elem in s12_ws_elem]
# text_content = [a.replace("and", "").strip() for a in text_content if len(a) > 2]
# print(text_content)

# elements = soup.find_all('span', style=lambda value: value and ('font-family: Whitney-Semibold; font-size:12px' in value or 'font-family: Whitney-Semibold; font-size:6px' in value))

# authors_and_affiliations = []

# current_author = ""
# current_affiliation = ""

# for elem in elements:
#     # Check if font-size is 12px (author names)
#     if 'font-size:12px' in elem.get('style', ''):
#         if current_author and current_affiliation:
#             authors_and_affiliations.append((current_author.strip(), current_affiliation.split(" ")[0].strip()))
#             current_author = ""
#             current_affiliation = ""
#         current_author += elem.get_text(separator=' ', strip=True) + " "
#     # Check if font-size is 6px (affiliations)
#     elif 'font-size:6px' in elem.get('style', ''):
#         current_affiliation += elem.get_text(separator=' ', strip=True) + " "

# # Append the last author and affiliation pair
# if current_author and current_affiliation:
#     authors_and_affiliations.append((current_author.strip(), current_affiliation.strip()))

# print(authors_and_affiliations)

doi = get_doi(soup)
print(doi)


authors, journal, date, subjects = get_from_springerapi(doi[0]) # Sa meta/v2 je bilo moguće dohvatiti i disciplines
print(authors)
print(journal)
print(date)
print(subjects)

## DALJE NASTAVITI S AFILIJACIOJOM
