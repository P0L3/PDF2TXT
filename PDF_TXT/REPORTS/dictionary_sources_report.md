# Dictionary sources

##### [A Dictionary of Weather (3 ed.)](https://www.oxfordreference.com/display/10.1093/acref/9780191988356.001.0001/acref-9780191988356) - HTML
- Containes 2300+ entries
- Definitions are cut off behind paywall
- Should be scraped
- DONE - [dictionary_1.py](https://github.com/P0L3/PDFscience/blob/master/PDFscience/dictionary_1.py)

##### [Full Weather Gloassary](https://www.weather.gov/otx/Full_Weather_Glossary) - HTML
- Containes ~380 entries
- Can be copy pasted and processed
- DONE - [dictionary_2.py](https://github.com/P0L3/PDFscience/blob/master/PDFscience/dictionary_2.py)

##### [Glossary of Meteorology](https://glossary.ametsoc.org/wiki/Category:Terms) - HTML
- Containes ~10000 entries
- Has elaborate definitions
- Should be scraped with Selenium -> Protected with Cloudflare
- DONE - [dictionary_3.py](https://github.com/P0L3/PDFscience/blob/master/PDFscience/dictionary_3.py)

##### [Soil and Environmental Science Dictionary](https://www.routledge.com/Soil-and-Environmental-Science-Dictionary/Gregorich-Turchenek-Carter-Angers/p/book/9780367397241) - PDF
- Containes ~7000 entries in 380-page-long 
- Has elaborate definitions
- Should be extracted with pdfminer
- FAILED - Performed parameter search for layout algorithm using [param_search.py](https://github.com/P0L3/PDFscience/blob/master/PDFscience/param_search.py) -> No success

##### [El Niño Southern Oscillation in a Changing Climate](https://agupubs.onlinelibrary.wiley.com/doi/book/10.1002/9781119548164) - PDF
- Containes ~150 entries in 5-page-long glossary + much more in index!
- Should be extracted using pdfminer
- DONE - [dictionary_5.py](https://github.com/P0L3/PDFscience/blob/master/PDFscience/dictionary_5.py)
- NOTE - Index should be explored further

##### [Earth's Climate](https://www.macmillanlearning.com/college/us/product/Earths-Climate/p/1429255250) - PDF
- Containes ~300 entries
- Has good definitions
- Should be considered later (pdfminer)
- DONE - [dictionary_6.py](https://github.com/P0L3/PDFscience/blob/master/PDFscience/dictionary_6.py)
- NOTE - Index should be explored further

##### [Essentials of Meteorology](https://ggweather.com/met10/Glossary.pdf) - PDF
- Containes ~430 entries
- Has ok definitiond 
- Should be considered later (pdfminer)
