from pandas import DataFrame
from data.article_ingest import get_and_save_articles_as_json
from data.interaction_seeder import generate_and_save_interactions_as_json


articles = DataFrame(get_and_save_articles_as_json('articles.json'))

interactions = generate_and_save_interactions_as_json(articles['id'].to_list(), 20, 'interactions.json')