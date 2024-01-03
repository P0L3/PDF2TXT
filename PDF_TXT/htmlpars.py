"""
Nature html parsing
"""

from bs4 import BeautifulSoup

target = "./TEST/NCLIMATE/s41558-020-00938-y_Heat_Tolerance_In_Ectotherms_Scales_Predictably_With_Body_Size_.html"

with open(target, 'r') as inf:
    html = inf.read()

# print(html)
soup = BeautifulSoup(html, 'html.parser')

s24elem = soup.find_all(style=lambda value: value and 'font-size:24px' in value)
print(s24elem)