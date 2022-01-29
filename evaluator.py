import random
import typing

from pandas import DataFrame
from recommender import RecommenderEngine
from typing import Set


# interactions, interaction train and test should be indexed with user_id
def evaluate(interactions, interaction_train, interaction_test, engine: RecommenderEngine):
    users_results = {}

    # for each user id in test set
    for user_id in interaction_test.index.unique().values:
        # get top-N recommendation for this user
        # but exclude article ids that belong to train set
        exclude_list = set(interaction_train.loc[user_id]['article_id'])
        recommendation_result = engine.recommend(user_id, exclude_list)

        top_5_hits = 0

        # get article ids from test set
        article_ids_test = set(interaction_test.loc[user_id]['article_id'])

        # for each interacted article ids for this user in test set
        for article_id in article_ids_test:
            # get random sample of not interacted articles
            all_interacted_items = set(interactions.loc[user_id]['article_id'])
            not_interacted_items = set(interactions['article_id']) - all_interacted_items
            article_samples: Set = set(random.sample(not_interacted_items, 5))

            # combine the samples with current article_id
            find_articles = article_samples.union(set([article_id]))

            # only include specific articles in the recommendation result
            filtered_recommendation_result = recommendation_result.query('article_id in @find_articles')['article_id'].values

            # check top-n hits for items in filtered recommendation
            TOP_N = 5
            index = next((i for i, c in enumerate(filtered_recommendation_result) if c == article_id), -1)
            top_5_hits += int(index in range(TOP_N))  # convert true/false to numeric


        recall_5 = top_5_hits / float(len(article_ids_test))

        users_results[user_id] = {
            "top_5_hits": top_5_hits,
            "article_id_count": float(len(article_ids_test)),
            "recall_5": recall_5
        }

    hello = "hello"