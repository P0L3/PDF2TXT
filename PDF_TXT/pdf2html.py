"""
Nature pdf to html
"""
from io import StringIO, BytesIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams

output_string = StringIO()
target = "./SAMPLE/NPJCLIMATSCI/s41612-023-00487-z_Projection_Of_Temperature-Related_Mortality_Among_The_Elderly_Under_Advanced_Aging_And_Climate_Change_Scenario_.pdf"
# target = "pdf_with_svg_image-1.pdf"

with open(target, 'rb') as fin:
    extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='html', codec=None)

with open(target.replace("/SAMPLE/", "/TEST/").replace(".pdf", ".html"), 'w') as fout:
    fout.writelines(output_string.getvalue())