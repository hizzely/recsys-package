from ingest import fetcher

feeds = [
    'https://medium.com/feed/kabarinformatika/tagged/software-engineering',
    'https://medium.com/feed/kabarinformatika/tagged/startup',
    'https://medium.com/feed/kabarinformatika/tagged/Artificial%20Intelligence',
    'https://medium.com/feed/kabarinformatika/tagged/multimedia',
    'https://medium.com/feed/kabarinformatika/tagged/lessons%20learned'
]

articles = fetcher(feeds)

# for article in articles:
#     print('Title: ' + article['title'])
#     print('Author: ' + article['author'])
#     print('Categories: ' + " ".join(article['categories']))
#     print('Content: ' + article['content'])
#     print()