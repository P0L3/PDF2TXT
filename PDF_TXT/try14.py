from parser_pdf import get_from_doi2bibapi, get_from_springerapi

doi = "10.1002/jgrd.50863"


print(get_from_doi2bibapi(doi))
print(20*"-")
print(get_from_springerapi(doi))
