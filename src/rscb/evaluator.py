import random
from pandas import DataFrame
from recommender_engine import RecommenderEngine


# interactions, interaction train and test should be indexed with user_id
def recall(interactions: DataFrame, interaction_train: DataFrame, interaction_test: DataFrame,
           trained_engine: RecommenderEngine) -> DataFrame:
    """Perform evaluation using Recall metric"""
    result = []

    # for each user id in test set
    for user_id in interaction_test.index.unique().values:
        # get top-N recommendation for this user
        # but exclude article ids that belong to train set
        exclude_list = set(interaction_train.loc[user_id]['article_id'])
        recommendation_result = trained_engine.recommend(user_id, top_n=10, exclude_article_ids=exclude_list)

        top_5_hits = 0
        top_10_hits = 0

        # get article ids from test set
        article_ids_test = set(interaction_test.loc[user_id]['article_id'])

        # get random sample of not interacted articles
        all_interacted_items = set(interactions.loc[user_id]['article_id'])
        not_interacted_items = set(interactions['article_id']) - all_interacted_items
        article_samples: set = set(random.sample(not_interacted_items, 5))  # 5 random articles

        # combine the samples with articles from test set
        find_articles = article_samples.union(article_ids_test)

        # for each interacted article ids for this user in test set
        for article_id in article_ids_test:
            # only include specific articles in the recommendation result
            filtered_recommendation_result = recommendation_result \
                .query('article_id in @find_articles')['article_id'] \
                .values

            # check top-n hits for items in filtered recommendation
            index = next((i for i, c in enumerate(filtered_recommendation_result) if c == article_id), -1)
            top_5_hits += int(index in range(5))  # convert true/false to numeric
            top_10_hits += int(index in range(10))  # convert true/false to numeric

        recall_5 = top_5_hits / len(article_ids_test)
        recall_10 = top_10_hits / len(article_ids_test)

        result.append({
            "user_id": user_id,
            "article_count": len(article_ids_test),
            "top_5_hits": top_5_hits,
            "recall_5": recall_5,
            "top_10_hits": top_10_hits,
            "recall_10": recall_10,
        })

    return DataFrame(result).set_index('user_id', True)


def hit_rate_loocv(articles: DataFrame, interaction_train: DataFrame) -> DataFrame:
    """Perform evaluation using Hit rate with Leave-One-Out-Cross-Validation metric"""

    result = []

    for user_id in interaction_train.index.unique():
        # get interacted articles from this user
        user_articles = interaction_train.loc[user_id]

        # then keep one random article...
        keep_article_id = random.choice(user_articles['article_id'].values)

        # ...and exclude that from the set
        user_articles = user_articles[user_articles['article_id'] != keep_article_id]

        # feed that to the engine and get the recommendation list
        recommendation_list: DataFrame = RecommenderEngine().load(articles, user_articles).train().recommend(user_id)

        keep_index = recommendation_list.index[recommendation_list['article_id'] == keep_article_id].values[0]

        result.append({
            'user_id': user_id,
            'keep_article_id': keep_article_id,
            'keep_index': keep_index,
            'is_top_10': keep_index in range(10)
        })

    return DataFrame(result).set_index('user_id', True)
