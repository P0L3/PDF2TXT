"""
Nature pdf to html
"""
from io import StringIO, BytesIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()
target = "./SAMPLE/GCB/Global Change Biology - 2004 - Mohan - Genetic variation in germination growth and survivorship of red maple in response.pdf"


with open(target, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(line_margin=0.7), output_type='html', codec=None)

with open(target.replace("/SAMPLE/", "/TEST/").replace(".pdf", ".html"), 'w') as fout:
    fout.writelines(output_string.getvalue())