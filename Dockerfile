FROM python:3.9-alpine

RUN mkdir /sitemapper-app
COPY requirements.txt /sitemapper-app
COPY . /sitemapper-app

WORKDIR /sitemapper-app

RUN python3.9 setup.py sdist
RUN pip install -r requirements.txt
RUN mv dist/sitemapper-*.tar.gz dist/sitemapper.tar.gz
RUN pip install --upgrade dist/sitemapper.tar.gz

CMD ["python3.9", "-m", "sitemapper"]