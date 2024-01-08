doctype1 = [ 
    "font-size:24px", # get_title
    "font-family: Whitney-Semibold2; font-size:8px", # get_doi
    "font-family: Whitney-Semibold; font-size:12px", "font-family: Whitney-Semibold; font-size:6px", "font-family: Whitney-Book; font-size:8px", # get_authors_and_affiliations (author, affiliation, affiliation text)
    "font-family: MinionPro-Regular; font-size:7px", "font-family: MinionPro-RegularItalic; font-size:7px", # get_references
    "font-family: MinionPro-Regular\d*; font-size:9px" # get_content
]

doctype1_1 = {
    "get_title": ["font-size:24px"],
    "get_doi": ["font-family: Whitney-Semibold2; font-size:8px"],
    "get_authors_and_affiliations_au": ["font-family: Whitney-Semibold; font-size:12px"], # Author
    "get_authors_and_affiliations_nu": ["font-family: Whitney-Semibold; font-size:6px"],  # Number
    "get_authors_and_affiliations_af": ["font-family: Whitney-Book; font-size:8px"],      # Affiliation text
    "get_references": ["font-family: MinionPro-Regular; font-size:7px", "font-family: MinionPro-RegularItalic; font-size:7px"],
    "get_contet": ["font-family: MinionPro-Regular\d*; font-size:9px"]
}

print(doctype1_1["get_references"])