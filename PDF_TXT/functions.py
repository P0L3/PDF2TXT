from io import StringIO
from pdfminer.high_level import extract_text_to_fp
from pdfminer.layout import LAParams
import logging
import re



def pdf2html(target="./SAMPLE/NCLIMATE/s41558-020-00938-y_Heat_Tolerance_In_Ectotherms_Scales_Predictably_With_Body_Size_.pdf", line_margin=0.5):

    try:
        output_string = StringIO()

        with open(target, 'rb') as fin:
            extract_text_to_fp(fin, output_string, laparams=LAParams(line_margin=line_margin), output_type='html', codec=None)

        return output_string.getvalue()
    except:
        warning_message = f"Unable to read PDF. Skipping..."
        logging.warning(warning_message)
        return None
    
def check_if_ium(soup):
    """
    Check if the provided BeautifulSoup 'soup' object indicates incomplete Unicode mappings (ium).

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.

    Returns:
    - bool: True if incomplete Unicode mappings are found, False otherwise.

    The function searches for a 'div' element in the provided 'soup' object and iterates through its
    next siblings until a text length of at least 50 characters is found or no more siblings are present.
    It then uses a regular expression to check if the text contains at least three consecutive instances
    of the pattern "(cid:\d+)" which might indicate incomplete Unicode mappings.
    """
    elem = soup.find("div")
    while len(elem.text) < 50 and not type(elem) == type(None):
        elem = elem.find_next()

    if type(elem) == type(None):
        raise Exception("NO div element found!")
    
    return bool(re.search("(\(cid:\d+\)){3,}", elem.text))

def add_custom_tag_after_element(soup, target_element, tag_name, tag_content, style_attributes):
    """
    Add a custom tag with specified content after a specific element in the BeautifulSoup 'soup' object.

    Parameters:
    - soup (BeautifulSoup): The BeautifulSoup object representing the HTML content.
    - target_element (Tag): The target element after which the new tag will be added.
    - tag_name (str): The name of the custom tag to be added.
    - tag_content (str): The content to be placed inside the custom tag.

    Returns:
    - BeautifulSoup: The modified BeautifulSoup object.
    """
    new_tag = soup.new_tag(tag_name)
    new_tag.string = tag_content
    new_tag.attrs.update(style_attributes)
    target_element.insert_after(new_tag)
    return soup

