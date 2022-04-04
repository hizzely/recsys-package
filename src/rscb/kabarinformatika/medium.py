from typing import List
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup


def _extract_html_content(html: str) -> str:
    """Extract contents from HTML and return the cleaner version without HTML tags"""

    soup = BeautifulSoup(html, features="html.parser")
    elements = ["h1", "h2", "h3", "h4", "article", "section", "p", "span"]
    skipwords = ["Continue reading on", "on Medium"] # apparently case-sensitive
    content = ""

    for element in soup.find_all(elements):
        # Get the plain string without tags
        text = element.text

        # Don't append unrelated texts
        if any(word in text for word in skipwords):
            continue

        content += text + " "
    
    return content.strip()


def _map_article(id, article) -> dict:
    return {
        "id": int(id),
        "title": unidecode(article['title']),
        "author": unidecode(article['author']),
        "categories": article['categories'],
        "content": _extract_html_content(unidecode(article['content']))
    }


def get_articles(feeds: list) -> List[dict]:
    """Take a list of Medium RSS Feed urls and return the articles"""

    items = []
    parser_url = 'https://api.rss2json.com/v1/api.json'

    for feed in feeds:
        response = requests.get(parser_url, params={'rss_url': feed}).json()
        items += response['items']

    return [_map_article(idx + 1, item) for idx, item in enumerate(items)]
