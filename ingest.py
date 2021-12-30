import re
import requests
from unidecode import unidecode
from bs4 import BeautifulSoup

def extract_content(html_content) -> str:
    content = ""
    soup = BeautifulSoup(html_content, features="html.parser")
    
    for element in soup.find_all(["h1", "h2", "h3", "h4", "h5", "h6", "article", "section", "pre", "span", "p", "em"]):
        for string in element.stripped_strings:
            # Remove any weird character placement caused by formatting.
            clean_string = string.replace(",", "").strip() + " "
            
            # Reduce excessive spaces to one space, mostly on code examples.
            # https://stackoverflow.com/questions/1546226/is-there-a-simple-way-to-remove-multiple-spaces-in-a-string
            clean_string = re.sub(' +', ' ', clean_string)
            
            content += clean_string
    
    return content.strip()

def transform(article) -> dict:
    return {
        "title": unidecode(article['title']),
        "author": unidecode(article['author']),
        "categories": article['categories'],
        "content": extract_content(unidecode(article['content']))
    }

def fetcher(feeds) -> list:
    result = []
    parser_url = 'https://api.rss2json.com/v1/api.json'
        
    for feed in feeds:
        response = requests.get(parser_url, params = {'rss_url': feed}).json()
        result += [transform(article) for article in response['items']]
        
    return result