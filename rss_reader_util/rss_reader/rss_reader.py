# https://stackoverflow.com/questions/55936200/how-to-build-a-simple-rss-reader-in-python-3-7
# https://www.jcchouinard.com/read-rss-feed-with-python/

# how to add option without any argument (--json)
# https://intellipaat.com/community/4618/argparse-module-how-to-add-option-without-any-argument

# logging:
# https://khashtamov.com/ru/python-logging/

# https://www.crummy.com/software/BeautifulSoup/bs4/doc/#attrs

# format pubDate of rss feed:
# https://stackoverflow.com/questions/12270531/how-to-format-pubdate-with-python
# https://docs.python.org/3/library/datetime.html#strftime-strptime-behavior

# covert json string to a HTML table representation
# https://pypi.org/project/json2html/  - from json2html.jsonconv import json2html - important!

# convert html to pdf
# https://stackoverflow.com/questions/23359083/how-to-convert-webpage-into-pdf-by-using-python

# write file to a specific directory
# https://stackoverflow.com/questions/8024248/telling-python-to-save-a-txt-file-to-a-certain-directory-on-windows-and-mac


# parse RSS

# python -m pip install bs4  !!!
# python -m pip install requests  !!!
# python - m pip install lxml    !!!  чтобы нормально парсился xml
# python install pickledb

# python -m pip install --upgrade pip setuptools wheel

from bs4 import BeautifulSoup
import requests
import argparse
import json
import logging
import sys
from logging import StreamHandler, Formatter

from json2html import json2html
import rss_reader.version as ver # - для пакета import version as ver   ODO
import pickledb
import time
import feedparser
import os
from json2html.jsonconv import json2html  # вот здесь правильный импорт, помучилась сильно
from datetime import datetime
import pdfkit



logger = logging.getLogger(__name__)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))


def init_db():
    if not os.path.exists('rss.db'):
        with open('rss.db', 'w') as f:
            f.write('{}')

    rss_db = pickledb.load('rss.db', False)
    return rss_db


db = init_db()


def parse_rss_reader_args():
    """Creates the arguments parser, adds arguments."""

    parser = argparse.ArgumentParser(prog='rss_reader', description='This utility reads RSS feed & outputs to console')
    parser.add_argument('source', nargs='?', type=str, help='RSS URL')
    parser.add_argument('--version', action='store_true', help='print version info')
    parser.add_argument('--json', action='store_true', help='print result as JSON in stdout')
    parser.add_argument('--verbose', action='store_true', help='output verbose status messages in stdout')
    parser.add_argument('--limit', type=int, help='limit news topics if this parameter provided')
    parser.add_argument('--date', type=str, help='print out the news from the specified day')
    parser.add_argument('--to_html', type=str, help='convert news to html format')
    parser.add_argument('--to_pdf', type=str, help='convert news to pdf format')
    args = parser.parse_args()

    return args


def read_rss(rss_url):
    """
    Fetches the given url using requests;
    Parses the XML with BeautifulSoup;
    Creates a list of dictionaries with article data: title, image, link, date;
    Fetches feed title

    :param rss_url: RSS url for reading
    :return: feed_title - title of the rss feed, articles_dicts - list of dictionaries with article data
    """
    try:
        logger.debug("Starting rss reader...")
        url = requests.get(rss_url)
        logger.debug(f"Loading news from {rss_url}...")

        soup = BeautifulSoup(url.content, 'xml')
    except Exception as e:
        raise Exception('Error fetching the URL: ', rss_url)

    try:
        articles = soup.findAll('item')

        articles_dicts = [
            {
                'title': a.find('title').text,  # 'title': a.title.text, # alternative syntax
                'link': a.find('link').text,
                'image': a.find('media:content'),
                'date': a.find('pubDate').text
            }
            for a in articles
        ]

        feed_title = soup.find('channel').title.text
        return feed_title, articles_dicts
    except Exception as e:
        raise Exception('Could not parse the xml: %s' % rss_url)  # %s - placeholder для строки для еррора


def get_articles(articles_limit=float('inf')):

    #TODO errors: not integer.
    """
    Gets results of rss parsing

    :param articles_limit: if not specified, then user gets _all_ available feed;
    if larger than feed size then user gets _all_ available news.
    :return: articles_list - list of dictionaries with articles
    """

    args = parse_rss_reader_args()
    feed, articles = read_rss(args.source)
    logger.debug("Processing result...\n")
    if articles_limit >= 1:
        print(f'\nFeed: {feed}\n')
        articles_list = []
        for article in articles:
            if articles.index(article) < articles_limit:
                articles_dict = {
                    'Title': article["title"],
                    'Date': time.strftime('%a, %d %b %Y %X %z', feedparser.datetimes._parse_date(article["date"])),
                    'Link': article["link"]
                }
                if 'image' in article and article['image']:
                    articles_dict['Image'] = article["image"]["url"]

                print(articles_dict)                # DELETE ME TODO
                articles_list.append(articles_dict)

                date_in_db = time.strftime('%Y%m%d', feedparser.datetimes._parse_date(article["date"]))
                if not db.exists(date_in_db):
                    add_to_db(db, date_in_db, articles_dict)
                else:
                    update_db(db, date_in_db, articles_dict)
            else:
                break
    else:
        raise Exception("Sorry, no numbers below one")
    return articles_list


def print_articles(articles_list):
    """
    Prints requested articles in console
    :param articles_list: list of dictionaries with articles to be printed
    """
    for article in articles_list:
        print(
            f'Title: {article["Title"]}\n'
            f'Date: {article["Date"]}\n'
            f'Link: {article["Link"]}\n------------------------\n'
            )
        if 'Image' in article:
            print(f'Image: {article["Image"]}\n')


def add_to_db(database, date, article):
    """
    Adds article for the specific date to the local database

    :param database: local database where the articles for the specific dates are being stored
    :param date: a date in `%Y%m%d` format - actual publishing date
    :param article: dictionary with article data to be added
    """
    database.set(date, [article])
    database.dump()


def update_db(database, date, article):
    """
    Updates the list with articles for the specific date in the local database

    :param database: local database where the articles for the specific dates are being stored
    :param date: a date in `%Y%m%d` format - actual publishing date
    :param article: dictionary with article data
    """
    art_list_date = database.get(date)
    if article not in art_list_date:
        art_list_date.append(article)
    database.set(date, art_list_date)
    database.dump()


def print_from_db(database, date, articles_limit=float('inf')):
    """
    In case of using `--date` argument prints the news from the database for the specific date in console

    :param database: local database where the articles for the specific dates are being stored
    :param date: a date in `%Y%m%d` format - actual publishing date
    :param articles_limit: if not specified, then user gets _all_ available articles from database for the specific date;
    if larger than number of articles in database, then user gets _all_ available articles.
    :return specific_date_articles: the list of dictionaries with articles for the specific date
    """
    try:
        logger.debug(f"Printing the news from {date}...\n")
        specific_date_articles = database.get(date)
        limited_articles_list = []
        if articles_limit >= 1:
            for article in specific_date_articles:
                if specific_date_articles.index(article) < articles_limit:
                    limited_articles_list.append(article)
                else:
                    break
        else:
            logger.error("Sorry, no numbers below one")
        return limited_articles_list

    except Exception as e:
        raise Exception('Could not find the news for the requested date in the database.')


def create_json(articles_list):
    """
    In case of using `--json` argument the utility converts the news into JSON format

    :param articles_list: list of dictionaries with articles to be converted into JSON format
    :return articles_json: JSON string with articles
    """
    print(articles_list)   # DELETE ME TODO
    articles_json = json.dumps(articles_list, ensure_ascii=False, indent=2) # ensure_ascii делает кодировку нормальной
    print(type(articles_json))     # DELETE ME TODO
    return articles_json


def print_json(json_articles):
    """
    Prints the news in JSON format in stdout
    :param json_articles: JSON string with articles to be printed in stdout
    """
    logger.debug("Printing news in JSON format...\n")
    print(json_articles)


def convert_to_html(articles):
    """
    In case of using `--to_html` argument the utility converts the news into HTML format
    :param articles: JSON string with articles to be converted into HTML format
    :return html_output: HTML Table representation
    """
    json_articles = create_json(articles)
    logger.debug(f"Converting the news to HTML format...")
    html_output = json2html.convert(json=json_articles)
    return html_output


def convert_to_pdf(articles, path):
    """
    In case of using `--to_pdf` argument the utility converts the news into PDF format
    :param articles: HTML string with articles to be converted into PDF format and printed in stdout
    :param path: absolute path where news file will be saved
    """
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y__%H-%M-%S")
    file_name = f'{dt_string}.pdf'

    options = {
        'page-size': 'A4',
        'orientation': 'Landscape',
        'margin-top': '0.7in',
        'margin-right': '0.75in',
        'margin-bottom': '0.7in',
        'margin-left': '0.75in',
        'encoding': 'UTF-8',
    }

    logger.debug(f"Converting the news to PDF format...")
    html_articles = convert_to_html(articles)
    if os.path.exists(f'{path}'):
        pdfkit.from_string(f'{html_articles}', (os.path.join(f'{path}', f'{file_name}')), options=options)
        logger.debug(f"{dt_string}.pdf successfully created.")
    else:
        logger.error("Sorry, path doesn't exist.")


def write_to_file(content, path):  # сделать для всех форматов
    """
    Writes the news in a given format to a file TODO
    :param content: HTML Table representation of the news
    :param path: absolute path where news file will be saved
    """
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y__%H-%M-%S")
    file_name = f'{dt_string}.html'
    if os.path.exists(f'{path}'):
        with open(os.path.join(f'{path}', f'{file_name}'), "w") as f:
            f.write(f'{content}')
            logger.debug(f"{dt_string}.html successfully created.")
    else:
        logger.error("Sorry, path doesn't exist.")


def print_version():
    """
    In case of using `--version` argument prints version
    """
    print(ver.__version__)


def main():   ## NEW VERSION

    args = parse_rss_reader_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    #try:
    if args.source:
        if args.limit:
            articles = get_articles(articles_limit=args.limit)
        else:
            articles = get_articles(articles_limit=float('inf'))
        print_articles(articles)
    else:
        if args.date:
            if args.limit:
                articles = print_from_db(db, args.date, articles_limit=args.limit)
            else:
                articles = print_from_db(db, args.date, articles_limit=float('inf'))
            print_articles(articles)
        elif args.version:
            print_version()
        else:
            raise Exception("Enter some URL.")

    if args.json:
        json_articles = create_json(articles)
        print_json(json_articles)

    if args.to_html:
        html_news = convert_to_html(articles)
        write_to_file(html_news, args.to_html)

    if args.to_pdf:
        convert_to_pdf(articles, args.to_pdf)


# def main():   ## OLD VERSION
#
#     args = parse_rss_reader_args()
#     #try:
#     if args.source:
#         if args.verbose:
#             logger.setLevel(logging.DEBUG)
#         else:
#             logger.setLevel(logging.INFO)
#
#         if args.limit:
#             articles = get_articles(args.limit)
#         else:
#             articles = get_articles()
#         print_articles(articles)
#
#         if args.json:
#             json_articles = create_json(articles)
#             print_json(json_articles)
#
#         if args.to_html:
#             html_news = convert_to_html(articles)
#             write_to_file(html_news, args.to_html)
#
#         if args.to_pdf:
#             convert_to_pdf(articles, args.to_pdf)
#
#     else:
#         if args.date:
#             if args.limit:
#                 specific_date_articles = print_from_db(db, args.date, args.limit)
#             else:
#                 specific_date_articles = print_from_db(db, args.date)
#             print_articles(specific_date_articles)
#
#             if args.json:
#                 json_articles = create_json(specific_date_articles)
#                 print_json(json_articles)
#
#             if args.to_html:
#                 json_articles = create_json(specific_date_articles)
#                 converted_news = convert_to_html(json_articles)
#                 write_to_file(converted_news, args.to_html)
#
#             if args.to_pdf:
#                 convert_to_pdf(specific_date_articles, args.to_pdf)
#
#         elif args.version:
#             print_version()
#         else:
#             raise Exception("Enter some URL.")
#     # except Exception as e:
#     #     logger.error(e)
    #
    logger.debug("Exiting the program.")


if __name__ == "__main__":
    main()


# TODO ERROR] 'NoneType' object is not subscriptable- -  python rss_reader.py 'https://news.yahoo.com/rss/' --limit 35 --json --verbose
# 'image': None,
# <item>
# <title>Russia `alarmed' at no US visas to attend UN leaders meeting</title>
# <link>https://news.yahoo.com/russia-alarmed-no-us-visas-033903929.html</link>
# <pubDate>2022-09-03T03:39:03Z</pubDate>
# <source url="http://www.ap.org/">Associated Press</source>
# <guid isPermaLink="false">russia-alarmed-no-us-visas-033903929.html</guid>
# <media:credit role="publishing company"/>
# </item>

# test_url = 'https://news.yahoo.com/rss/'
# test_url = 'https://realpython.com/atom.xml' # Error     feed = soup.find('channel').title.text
# AttributeError: 'NoneType' object has no attribute 'title'

# test_url = 'https://practicaldatascience.co.uk/feed.xml'
# test_url = 'https://waylonwalker.com/rss.xml'
# test_url = 'https://www.jcchouinard.com/author/jean-christophe-chouinard/feed/'