FROM python:3.8.0

WORKDIR /textprocessing

COPY ./requirements.txt ./
RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir PDF_TXT

CMD ["echo", "PDF_TXT container ready!"]
