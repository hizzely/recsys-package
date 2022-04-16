import random
from pandas import DataFrame
from . import RecommenderEngine


# interactions, interaction train and test should be indexed with user_id
def recall(interactions: DataFrame,
           interaction_train: DataFrame,
           interaction_test: DataFrame,
           trained_engine: RecommenderEngine) -> DataFrame:
    """Perform evaluation using Recall metric"""
    interactions = interactions.set_index('user_id')
    interaction_train = interaction_train.set_index('user_id')
    interaction_test = interaction_test.set_index('user_id')
    result = []

    # for each user id in test set...
    # *also handle edge case where pandas will treat single row data as series instead of dataframe
    # https://stackoverflow.com/q/16782323
    for user_id in interaction_test.index.unique().values:
        # get top-N recommendation for this user
        # but exclude article ids that belong to train set
        exclude_list = list(set(interaction_train.loc[[user_id]]['article_id']))
        recommendation_result = trained_engine.get_recommendation(user_id, top_n=10, exclude=exclude_list)

        top_5_hits = 0
        top_10_hits = 0

        # get article ids from test set
        article_ids_test = set(interaction_test.loc[[user_id]]['article_id'])

        # get random sample of not interacted articles
        all_interacted_items = set(interactions.loc[[user_id]]['article_id'])
        not_interacted_items = set(interactions['article_id']) - all_interacted_items
        article_samples = set(random.sample(not_interacted_items, 5))  # 5 random articles

        # combine the samples with articles from test set
        find_articles = article_samples.union(article_ids_test)

        # for each interacted article ids for this user in test set
        for article_id in article_ids_test:
            # only include specific articles in the recommendation result
            recommendation_result = list(filter(lambda i: i[0] in find_articles, recommendation_result))

            # check top-n hits for items in filtered recommendation
            for idx, item in enumerate(recommendation_result):
                if int(item[0]) is article_id:
                    top_5_hits += int(idx in range(5))
                    top_10_hits += int(idx in range(10))

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


# def hit_rate_loocv(articles: DataFrame, interaction_train: DataFrame) -> DataFrame:
#     """Perform evaluation using Hit rate with Leave-One-Out-Cross-Validation metric"""
#
#     result = []
#
#     for user_id in interaction_train.index.unique():
#         # get interacted articles from this user
#         user_articles = interaction_train.loc[user_id]
#
#         # then keep one random article...
#         keep_article_id = random.choice(user_articles['article_id'].values)
#
#         # ...and exclude that from the set
#         user_articles = user_articles[user_articles['article_id'] != keep_article_id]
#
#         # feed that to the engine and get the recommendation list
#         recommendation_list = RecommenderEngine(articles, user_articles) \
#             .set_algorithm(Tfidf) \
#             .train() \
#             .get_recommendation(user_id, top_n=10)
#
#         keep_index = recommendation_list.index[recommendation_list['article_id'] == keep_article_id].values[0]
#
#         result.append({
#             'user_id': user_id,
#             'keep_article_id': keep_article_id,
#             'keep_index': keep_index,
#             'is_top_10': keep_index in range(10)
#         })
#
#     return DataFrame(result).set_index('user_id', True)
