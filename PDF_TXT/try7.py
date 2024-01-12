from pdfminer.high_level import extract_pages
from pdfminer.layout import LAParams

la_params = LAParams()

for page in extract_pages("./SAMPLE/GCB/Global Change Biology - 2017 - Assis - Projected climate changes threaten ancient refugia of kelp forests in the North(1).pdf", laparams=la_params, caching=False):
    print("*****OUTPUT:*****")
    for element in page:
        print(element)