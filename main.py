import math
import pandas
from pandas import DataFrame
from sklearn.model_selection import train_test_split
from recommender import RecommenderEngine


def print_result(_articles, _interactions_train, _user_id, _rec_tokens, _rec_articles):
    # Tell user's interacted articles
    interacted_article_ids = _interactions_train.loc[_user_id]['article_id']
    interacted_articles = _articles.query('id in @interacted_article_ids')

    print("You've interacted with these articles in the past:")
    print(interacted_articles[['id', 'title']])
    print("")

    print("Those articles contain these keywords:")
    print(_rec_tokens)
    print("")

    # Give article recommendations
    recommendations_total = len(_rec_articles)

    if recommendations_total > 0:
        print("Therefore, you might be interested in these other similar articles:")
        for i in range(recommendations_total):
            recommendation: DataFrame = _rec_articles.loc[i]
            article = articles[articles['id'] == recommendation['article_id']].iloc[0]
            print(f"- {article['id']}: {article['title']} ({recommendation['strength']})")
    else:
        print("But we have no other similar content left :(")

# Load data
articles: DataFrame = pandas.read_json('./data/articles.json')
interactions: DataFrame = pandas.read_json('./data/interactions.json')

# Sum the weight for each article interactions.
# Smooth the distribution by applying natural logarithm in case the same event recorded multiple times.
# TODO: Once settled, consider moving this into the dataset preparation module
interactions = interactions \
    .groupby(['user_id', 'article_id'])['weight'].sum() \
    .apply(lambda x: math.log(1 + x, 2)) \
    .reset_index()

# Split the dataset into training and testing set using hold-out method.
interactions_train, interactions_test = train_test_split(
    interactions,
    stratify=interactions['user_id'],
    test_size=0.20,
    random_state=42
)

# We can then access it using: df.loc[user_id]
interactions = interactions.set_index('user_id')
interactions_train = interactions_train.set_index('user_id')
interactions_test = interactions_test.set_index('user_id')

# Initialize the recommender engine
engine = RecommenderEngine().load(articles, interactions_train).train()

while True:
    # TODO: What if the user has seen all articles? wouldn't that make the recommendation list empty?
    user_id = int(input('User ID: '))

    # Create recommendation
    rec_articles = engine.recommend(user_id)
    rec_tokens = engine.recommend_tokens(user_id)

    print_result(articles, interactions_train, user_id, rec_tokens, rec_articles)
