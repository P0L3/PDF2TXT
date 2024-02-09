# A repo for PDF processing of certain journals

## TODO
- Solve fi problem -> [ligatures](PDF_TXT/ligatures_list.txt)
    - Add styles to cover fi detection for all journals, solved: 
- Structure dataframe output -> Add empty values where missing
- Clean directory
- Parsers for journals: 1, 2, 6, 29, 30

## Data structure

## Fi problem
### JGRA
Solved: S1, S3, S7
TODO: S0, S2, S4, S5, S6, Sdef

- S1: 
  - get_references_nonumber_ref
  - get_keyword_styles
  - get_content
  - get_authors_and_affiliations_af
- S2:
  - get_keyword_styles
- S3:
  - get_keyword_styles
  - get_content
  - get_authors_and_affiliations_af
- S7:
  - get_content
  - get_authors_and_affiliations_af
  - get_references_nonumber_ref
  - get_keyword_styles
- S8:
  - get_keyword_styles

### NGEO
Solved:
TODO: S0, S1

### JCLIMATE
Solved: S1
TODO: S0, S2, S3, S4, Sdef

- S0:
  - get_references_nonumber_title
  - get_references_nonumber_ref
  - get_abstract
- S4: 
  - get_references_nonumber_title
  - get_references_nonumber_ref
  - get_abstract

### NPJCLIAC
Solved: S0
TODO: S2, S3

- S0:
  - get_references
  - get_content

### GCB
Solved: S0
TODO: S1 - S6, Sdef

### ENERPOL
Solved: S0, S2, S3, S5
TODO: S1, S4, Sdef

- S0:
  - get_content
  - get_authors_and_affiliations_au
  - get_references_nonumber_ref
- S2:
  - get_authors_and_affiliations_af
  - get_keywords
  - get_content
- S3:
  - get_content

### EHS
Solved:
TODO:



## Journals
1. [Climate Dynamics](https://link.springer.com/journal/382)
2. [Ecological Applications](https://esajournals.onlinelibrary.wiley.com/journal/19395582) 
- [**ehs_htmlpars.py**](PDF_TXT/ehs_htmlpars.py)    
    3. [Ecosystem Health and Sustainability](https://spj.science.org/journal/ehs)
- [**enerpol_htmlpars.py**](PDF_TXT/enerpol_htmlpars.py)    
    4. [Energy Policy](https://www.sciencedirect.com/journal/energy-policy)
- [**gcb_htmlpars.py**](PDF_TXT/gcb_htmlpars.py)    
    5. [Global Change Biology](https://onlinelibrary.wiley.com/journal/13652486)
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
29. [PNAS](https://www.pnas.org/)
30. [Miscellaneous ArXiv](https://arxiv.org/)

