import re
from datetime import datetime

from newsgac.data_sources.models import Article
import newsgac.data_engineering.utils as DataUtils


def get_articles_from_file(file):
    duplicate_count = 0
    other_count = 0
    articles = []

    for line in file.read().splitlines():
        article = Article()

        line = line.rstrip()
        line = line.decode('utf8')
        # groups = re.search(r'^__label__(.{3}.+)DATE\=([\0-9]+) ((?s).*)$', line).groups()
        # groups = re.search(r'^__label__(.{3}.+)DATE\=([\0-9]+[^&]) ((?s).*)$', line).groups()
        reg_res = re.search(r'^__label__(.{3}.+)DATE\=(\d{1,}\/\d{1,}\/\d{2,}) ((?s).*)$', line)

        no_date = False
        if not reg_res:
            # no date
            reg_res = re.search(r'^__label__(.{3})((?s).*)', line)
            no_date = True

        if not reg_res:
            print (line)

        groups = reg_res.groups()
        article.label = groups[0].rstrip()

        if article.label not in DataUtils.genre_codes:
            article.label = 'OTH'
            other_count += 1

        if no_date:
            article.date = None
            article.raw_text = groups[1].rstrip()
        else:
            # TODO: correct the input mismatch documents - so far day and month are not used
            date_str = groups[1].rstrip()
            month = date_str.split("/")[0]
            day = date_str.split("/")[1]
            year = date_str.split("/")[2]

            if len(year) == 2:
                # fix for conversion 20xx where xx < 69 although the data is from 1900s
                year = "19" + year

            article.year = year
            date_str_corr = day + "/" + month + "/" + year
            article.date = datetime.strptime(date_str_corr, "%d/%m/%Y")
            article.raw_text = groups[2].rstrip()


            if article.raw_text not in map(lambda a: a.raw_text, articles):
                articles.append(article)
            else:
                duplicate_count += 1

    print( "Found ", other_count, " other genre in documents..")
    print("Found ", duplicate_count, " duplicate(s) in documents..")

    return articles


def process_data_source(data_source):
    data_source.articles = get_articles_from_file(data_source.file.file)
    data_source.save(cascade=True)
