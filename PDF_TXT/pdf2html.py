"""
Nature pdf to html
"""
from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()
target = "./SAMPLE/NCLIMATE/s41558-020-00955-x_Greater_Committed_Warming_After_Accounting_For_The_Pattern_Effect_.pdf"


with open(target, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='html', codec=None)

with open(target.replace("/SAMPLE/", "/TEST/").replace(".pdf", ".html"), 'w') as fout:
    fout.writelines(output_string.getvalue())