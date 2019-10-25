FROM python:2.7

RUN mkdir /newsgac
RUN mkdir /home/flask

RUN groupadd -g 999 flask && \
    useradd -r -u 999 -g flask flask

RUN chown flask:flask /newsgac
RUN chown flask:flask /home/flask

COPY requirements.txt /newsgac/requirements.txt
RUN pip install -r /newsgac/requirements.txt

RUN python -m spacy download nl_core_news_sm

COPY entrypoint.sh /newsgac
RUN chmod a+x /newsgac/entrypoint.sh

USER flask

COPY newsgac /newsgac/newsgac

RUN ["bash", "-c", "python <<< \"import nltk; nltk.download('punkt')\""]

WORKDIR /newsgac

COPY test /newsgac/test

ENTRYPOINT ["/newsgac/entrypoint.sh"]

CMD ["echo", "You should define a command in docker-compose.yml"]
