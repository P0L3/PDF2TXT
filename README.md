# A repo for PDF processing of certain journals

## TODO
- Solve fi problem -> [ligatures](PDF_TXT/ligatures_list.txt)
- Parsers for journals: 30
- Test out diff for test3_jgra(_fi)
- Add missing parsers: ARX
- Test CLIMD, ECOAPP, NPJCLIAC, NPJCLISCI, GCB, 
- Solve Acknowledgement problem in [PNAS](/PDF_TXT/pnas_htmlpars.py) -> Check [Notes](/PDF_TXT/REPORTS/PNAS_test.md)
- Solve Missing text problems in [IJOC](/PDF_TXT/ijoc_htmlpars.py) -> Check [Notes](/PDF_TXT/REPORTS/IJOC_test.md)
- Check problems with JGRA

## Data structure

| Columns | Descriptions |
| ------- | ------------ |
|1. Title|*Paper title in a list*: `["Effects of pretraining corpora"]`|
|2. Authors_and_Affiliations|*List of author and affil number tuples*: `[("Andrija Poleksic", "1, 2"), (...)]`|
|3. Affiliations|*Affiliation text and number tuples*: `[(1, "FIDIT"), (...)]`|
|4. DOI|*Paper doi number in a list*: `["10.23919/mipro57284.2023.10159770"]`|
|5. Authors|*String containing all authors or detailed list*: `"Poleksic, Andrija and ..."` or `[{'ORCID': '123', 'creator': 'Poleksic, Andrija'}, {...}]`|
|6. Journal|*Name of the journal*: `"Nature Geoscience"`|
|7. Date|*Date of publishing*: `5-30-2034`|
|8. Subjects|*List of topics in the paper*: `["Earth Sciences", "..."`|
|9. Abstract|*Abstract text of the paper*: `"The amount of data ..."`|
|10. References|*List of references*: `["Matching the Blanks: Distributio ..."]`|
|11. Content|*Full text from paper*: `"Reading text to identify and ..."`|
|12. Keywords|*Keywords or keypoints from a paper, list, or string*: `["Internal variability", "..."]` or `"A significant interdecadal variation ..."`|
|13. Style|*Debug data*: `"1"`|


**Data template**:
``` python
# Original
paper_data = {
            "Title": title,
            "Authors_and_Affiliations": authors_and_affiliations,
            "Affiliations": affiliations,
            "DOI": doi,
            "Authors": authors,
            "Journal": journal,
            "Date": date,
            "Subjects": subjects,
            "Abstract": abstract,
            "References": references,
            "Content": content,
            "Keywords": keywords,
            "Style": style,
        }

# Default
paper_data = {
            "Title": "no_title",
            "Authors_and_Affiliations": "no_auth_and_affil",
            "Affiliations": "no_affil",
            "DOI": "no_doi",
            "Authors": "no_author",
            "Journal": "no_journal",
            "Date": "no_date",
            "Subjects": "no_subjects",
            "Abstract": "no_abstract",
            "References": "no_references",
            "Content": "no_content",
            "Keywords": "no_keywords",
            "Style": s,
        }
```




## Journals

- [**climd_htmlpars.py**](PDF_TXT/climd_htmlpars.py)    
    1. [Climate Dynamics](https://link.springer.com/journal/382)    
- [**ecoapp_htmlpars.py**](PDF_TXT/ecoapp_htmlpars.py)    
    2. [Ecological Applications](https://esajournals.onlinelibrary.wiley.com/journal/19395582) 
- [**ehs_htmlpars.py**](PDF_TXT/ehs_htmlpars.py)    
    3. [Ecosystem Health and Sustainability](https://spj.science.org/journal/ehs)
- [**enerpol_htmlpars.py**](PDF_TXT/enerpol_htmlpars.py)    
    4. [Energy Policy](https://www.sciencedirect.com/journal/energy-policy)
- [**gcb_htmlpars.py**](PDF_TXT/gcb_htmlpars.py)    
    5. [Global Change Biology](https://onlinelibrary.wiley.com/journal/13652486)
- [**ijoc_htmlpars.py**](PDF_TXT/ijoc_htmlpars.py)    
    6. [International Journal of Climatology](https://rmets.onlinelibrary.wiley.com/journal/10970088)
- [**jclimate_htmlpars.py**](PDF_TXT/jclimate_htmlpars.py)  
    7. [Journal of Climate](https://www.ametsoc.org/index.cfm/ams/publications/journals/journal-of-climate/)
- [**jgra_htmlpars.py**](PDF_TXT/jgra_htmlpars.py)  
    8. [Journal of Geophysical Research: Atmospheres](https://agupubs.onlinelibrary.wiley.com/journal/21698996?journalRedirectCheck=true)
- [**mdpi_htmlpars.py**](PDF_TXT/mdpi_htmlpars.py)  
    9. [MDPI Air](https://www.mdpi.com/journal/air)     
    10. [MDPI Atmosphere](https://www.mdpi.com/journal/atmosphere)  
    11. [MDPI Climate](https://www.mdpi.com/journal/climate)    
    12. [MDPI Earth](https://www.mdpi.com/journal/earth)    
    13. [MDPI Ecologies](https://www.mdpi.com/journal/ecologies)    
    14. [MDPI Energies](https://www.mdpi.com/journal/energies)  
    15. [MDPI Environments](https://www.mdpi.com/journal/environments)  
    16. [MDPI Forests](https://www.mdpi.com/journal/forests)    
    17. [MDPI Fuels](https://www.mdpi.com/journal/fuels)    
    18. [MDPI Hydrology](https://www.mdpi.com/journal/hydrology)    
    19. [MDPI Meteorology](https://www.mdpi.com/journal/meteorology)    
    20. [MDPI Oceans](https://www.mdpi.com/journal/oceans)  
    21. [MDPI Recycling](https://www.mdpi.com/journal/recycling)    
    22. [MDPI Sustainable Chemistry](https://www.mdpi.com/journal/suschem)  
    23. [MDPI Water](https://www.mdpi.com/journal/water)    
- [**nature_htmlpars.py**](PDF_TXT/nature_htmlpars.py)  
    24. [Nature Climate Change](https://www.nature.com/nclimate/)
- [**ngeo_htmlpars.py**](PDF_TXT/ngeo_htmlpars.py)  
    25. [Nature Geoscience](https://www.nature.com/ngeo/)
- [**npjcliac_htmlpars.py**](PDF_TXT/npjcliac_htmlpars.py):     
    26. [NPJ Climate Action](https://www.nature.com/npjclimataction/)
- [**npjclisci_htmlpars.py**](PDF_TXT/npjclisci_htmlpars.py):   
    27. [NPJ Climate and Atmospheric Science](https://www.nature.com/npjclimatsci/)     
    28. [NPJ Ocean Sustainability](https://www.nature.com/npjoceansustain/)
- [**pnas_htmlpars.py**](PDF_TXT/pnas_htmlpars.py)    
    29. [PNAS](https://www.pnas.org/)   
30. [Miscellaneous ArXiv](https://arxiv.org/)

## Test reports
- based on [try16.py](/PDF_TXT/try16.py) and outputs in [test25.txt](/PDF_TXT/test25.txt)

#### [PNAS report](/PDF_TXT/REPORTS/PNAS_test.md)
#### [IJOC report](/PDF_TXT/REPORTS/IJOC_test.md)
#### [JCLIMATE report](/PDF_TXT/REPORTS/JCLIMATE_test.md)
#### [CLIMD report](/PDF_TXT/REPORTS/CLIMD_test.md)
#### [JGRA report](/PDF_TXT/REPORTS/JGRA_test.md)

