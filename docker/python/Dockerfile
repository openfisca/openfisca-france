FROM python:2.7

RUN mkdir /usr/src/app
WORKDIR /usr/src/app

COPY ./setup.py ./

RUN pip install -e .
RUN pip install -e ".[test]"

COPY docker/python/start.sh /usr/local/bin/openfisca-start
RUN chmod +x /usr/local/bin/openfisca-start

CMD ["openfisca-start"]
