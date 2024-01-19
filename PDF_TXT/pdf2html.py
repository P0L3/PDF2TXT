"""
Nature pdf to html
"""
from io import StringIO, BytesIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()
target = "./SAMPLE/JGRA/JGR Atmospheres - 2014 - Hong - Enhanced relationship between the tropical Atlantic SST and the summertime western North.pdf"
# target = "pdf_with_svg_image-1.pdf"

with open(target, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='html', codec=None)

with open(target.replace("/SAMPLE/", "/TEST/").replace(".pdf", ".html"), 'w') as fout:
    fout.writelines(output_string.getvalue())