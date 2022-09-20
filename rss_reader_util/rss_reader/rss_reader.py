from bs4 import BeautifulSoup
import requests
import argparse
import json
import logging
import sys
from logging import StreamHandler, Formatter
from json2html import json2html
import pickledb
import time
import feedparser
import os
from json2html.jsonconv import json2html  # вот здесь правильный импорт, помучилась сильно
from datetime import datetime
import pdfkit

try:
    import rss_reader.version as ver   # - to start as package `rss_reader`
except:
    import version as ver   # - to start as `python rss_reader\rss_reader.py`


logger = logging.getLogger(__name__)
handler = StreamHandler(stream=sys.stdout)
logger.addHandler(handler)
handler.setFormatter(Formatter(fmt='[%(asctime)s: %(levelname)s] %(message)s'))


def init_db():
    my_db = 'rss_reader/rss.db'
    try:
        if not os.path.exists('rss_reader/rss.db'):
            with open('rss_reader/rss.db', 'w') as f:
                f.write('{}')

        rss_db = pickledb.load(my_db, False)
    except Exception as e:
        raise Exception('Could not load database.')
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
    """
    Gets results of rss parsing
    :param articles_limit: if not specified, then user gets _all_ available feed;
    if larger than feed size then user gets _all_ available news.
    :return: articles_list - list of dictionaries with articles
    """

    args = parse_rss_reader_args()
    feed, articles = read_rss(args.source)
    logger.debug("Processing result...")
    logger.debug(f"Database is updated.\n")
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

                articles_list.append(articles_dict)

                date = time.strftime('%Y%m%d', feedparser.datetimes._parse_date(article["date"]))
                add_or_update_db(date_in_db=date, art_to_db=articles_dict)

            else:
                break
    else:
        raise Exception("Sorry, no numbers below one")

    return articles_list


def add_or_update_db(date_in_db, art_to_db):
    """
    Calls add_to_db or update_db
    :param date_in_db: date in '%Y%m%d' format;
    :param art_to_db: dictionary with article
    """

    if not db.exists(date_in_db):
        add_to_db(db, date_in_db, art_to_db)
    else:
        update_db(db, date_in_db, art_to_db)


def print_articles(articles_list):
    """
    Prints requested articles in console
    :param articles_list: list of dictionaries with articles to be printed
    """
    for article in articles_list:
        print(
            f'Title: {article["Title"]}\n'
            f'Date: {article["Date"]}\n'
            f'Link: {article["Link"]}'
            )
        if 'Image' in article:
            print(f'Image: {article["Image"]}\n------------------------\n'),


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
    articles_json = json.dumps(articles_list, ensure_ascii=False, indent=2)   # ensure_ascii делает кодировку нормальной

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


def create_file_name(extension):
    """
    Creates file name based on the current date and time
    :param extension: file extension
    :return file_name: file name
    """
    now = datetime.now()
    dt_string = now.strftime("%d-%m-%Y__%H-%M-%S")
    file_name = f'{dt_string}.{extension}'

    return file_name


def convert_to_pdf(articles, path):
    """
    In case of using `--to_pdf` argument the utility converts the news into PDF format
    :param articles: HTML string with articles to be converted into PDF format and printed in stdout
    :param path: absolute path where news file will be saved
    """
    file_name = create_file_name("pdf")
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
        logger.debug(f"{file_name} successfully created.")
    else:
        logger.error("Sorry, path doesn't exist.")


def write_to_file(content, path):
    """
    Writes the news in a given format to a file
    :param content: HTML Table representation of the news
    :param path: absolute path where news file will be saved
    """
    file_name = create_file_name("html")
    if os.path.exists(f'{path}'):
        with open(os.path.join(f'{path}', f'{file_name}'), "w") as f:
            f.write(f'{content}')
            logger.debug(f"{file_name} successfully created.")
    else:
        logger.error("Sorry, path doesn't exist.")


def print_version():
    """
    In case of using `--version` argument prints version
    """
    print(ver.__version__)


def main():

    args = parse_rss_reader_args()
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    else:
        logger.setLevel(logging.INFO)

    try:
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

    except Exception as e:
        logger.error(e)

    logger.debug("Exiting the program.")


if __name__ == "__main__":
    main()
