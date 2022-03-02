from typing import List
import re
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup


def extract_html_content(html: str) -> str:
    """Extract contents from HTML and return the cleaner version without HTML tags"""

    content = ""
    soup = BeautifulSoup(html, features="html.parser")

    for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "article", "section", "pre", "span", "p", "em"]):
        for string in element.stripped_strings:
            # Remove any weird character placement caused by formatting.
            clean_string = string.replace(",", "").strip() + " "

            # Reduce excessive spaces to one space, mostly on code examples.
            # https://stackoverflow.com/questions/1546226/is-there-a-simple-way-to-remove-multiple-spaces-in-a-string
            clean_string = re.sub(' +', ' ', clean_string)

            content += clean_string

    return content.strip()


def map_article(article) -> dict:
    return {
        "title": unidecode(article['title']),
        "author": unidecode(article['author']),
        "categories": article['categories'],
        "content": extract_html_content(unidecode(article['content']))
    }


def assign_ids(articles: List[dict]) -> List[dict]:
    """Take a list of articles and return them with assigned sequential IDs"""

    id = 1
    result = []

    for article in articles:
        article.update({'id': id})
        result.append(article)
        id += 1

    return result


def get_articles(feeds: list) -> List[dict]:
    """Take a list of Medium RSS Feed urls and return the articles"""

    result = []
    parser_url = 'https://api.rss2json.com/v1/api.json'

    for feed in feeds:
        response = requests.get(parser_url, params={'rss_url': feed}).json()
        result += [map(map_article, response['items'])]

    return assign_ids(result)
