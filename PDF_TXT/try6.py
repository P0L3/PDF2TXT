from pdfminer.high_level import extract_pages
from pdfminer.layout import LTTextContainer

def pdf_to_html(pdf_path, html_path):
    with open(html_path, 'w', encoding='utf-8') as html_file:
        for page_layout in extract_pages(pdf_path):
            for element in page_layout:
                if isinstance(element, LTTextContainer):
                    html_file.write('<span>{}</span>'.format(element.get_text()))
            html_file.write('<br>')

target = "./SAMPLE/GCB/Global Change Biology - 2001 - Defries - A new global 1‐km dataset of percentage tree cover derived from remote sensing.pdf"
target_html = "./TEST/GCB/Global Change Biology - 2001 - Defries - A new global 1‐km dataset of percentage tree cover derived from remote sensing.html"
pdf_to_html(target, target_html)