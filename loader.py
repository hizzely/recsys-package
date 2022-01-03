from ingest import fetcher

def assign_ids(articles: list) -> list:
    id = 1
    result = []
    for article in articles:
        article.update({ 'id': id })
        result.append(article)
        id += 1
    return result


feeds = [
    'https://medium.com/feed/kabarinformatika/tagged/software-engineering',
    'https://medium.com/feed/kabarinformatika/tagged/startup',
    'https://medium.com/feed/kabarinformatika/tagged/Artificial%20Intelligence',
    'https://medium.com/feed/kabarinformatika/tagged/multimedia',
    'https://medium.com/feed/kabarinformatika/tagged/lessons%20learned'
]

articles = assign_ids(fetcher(feeds))

# for article in articles:
#     print('ID: ' + str(article['id']))
#     print('Title: ' + article['title'])
#     print('Author: ' + article['author'])
#     print('Categories: ' + " ".join(article['categories']))
#     print('Content: ' + article['content'])
#     print()
