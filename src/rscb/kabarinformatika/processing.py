import math
import re
from pandas import DataFrame
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


def prepare_articles(articles: list[dict]) -> DataFrame:
    indonesian_stemmer = StemmerFactory().create_stemmer()
    corpus: list[list[any, str]] = []

    for article in articles:
        # Select "title" and "content" as feature
        feature = f"{article['title']} {article['content']}"
        # Case folding, make all characters lowercase
        feature = feature.lower()
        # Preserve alpha, "-", and whitespace
        feature = re.sub('[^-a-z ]+', '', feature)
        # Replace two or more whitespaces with one whitespace
        feature = re.sub('\s\s+', ' ', feature)
        # Stem Indonesian
        feature = indonesian_stemmer.stem(feature)
        # Add to the corpus
        corpus.append([article['id'], feature])

    return DataFrame(corpus)


def prepare_interactions(interactions: list[dict]) -> DataFrame:
    return DataFrame(interactions) \
        .groupby(['user_id', 'article_id'])['weight'].sum() \
        .apply(lambda x: math.log(1 + x, 2)) \
        .reset_index() \
        .set_index('user_id')
