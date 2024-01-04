from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import logging



def pdf2html(target="./SAMPLE/NCLIMATE/s41558-020-00938-y_Heat_Tolerance_In_Ectotherms_Scales_Predictably_With_Body_Size_.pdf"):

    try:
        output_string = StringIO()

        with open(target, 'rb') as fin:
            extract_text_to_fp(fin, output_string, laparams=LAParams(), output_type='html', codec=None)

        return output_string.getvalue()
    except:
        warning_message = f"Unable to read PDF. Skipping..."
        logging.warning(warning_message)
        return None