"""
Nature pdf to html
"""
from io import StringIO, BytesIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()
# target = "./SAMPLE/JCLIMATE/clim-2010jcli3666.1(1).pdf"
target = "pdf_with_svg_image-1.pdf"

with open(target, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(all_texts=False), output_type='html', codec=None)

with open(target.replace("/SAMPLE/", "/TEST/").replace(".pdf", ".html"), 'w') as fout:
    fout.writelines(output_string.getvalue())