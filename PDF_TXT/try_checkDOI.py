from parser_pdf import get_from_doi2bibapi, get_from_springerapi

doi = "/10.1038/sj.sc.3101301"


print(get_from_doi2bibapi(doi))
print(20*"-")
print(get_from_springerapi(doi))

