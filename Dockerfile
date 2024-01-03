FROM python:3.8.0

WORKDIR /textprocessing

# RUN pip3 install PyPDF2
RUN pip3 install pdfminer
RUN pip3 install beautifulsoup4
# RUN pip3 install pikepdf
# RUN pip3 install pymupdf

RUN mkdir PDF_TXT

CMD ["echo", "PDF_TXT container ready!"]
