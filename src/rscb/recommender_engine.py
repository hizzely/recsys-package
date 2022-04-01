from __future__ import annotations
from typing import List
from pandas import DataFrame
from .algorithms import AbstractAlgorithm
from .exceptions import AlgorithmUnsetError, UntrainedAlgorithmError


class RecommenderEngine:
    algorithm: AbstractAlgorithm
    articles: DataFrame
    interactions_train: DataFrame

    def __init__(self, articles: DataFrame = None, interactions_train: DataFrame = None):
        self.articles = articles
        self.interactions_train = interactions_train

    def set_articles(self, articles: DataFrame) -> RecommenderEngine:
        self.articles = articles
        return self

    def set_interactions(self, interactions_train: DataFrame) -> RecommenderEngine:
        self.interactions_train = interactions_train
        return self

    def set_algorithm(self, algorithm: AbstractAlgorithm) -> RecommenderEngine:
        self.algorithm = algorithm()
        print("Current algorithm:", type(self.algorithm).__name__)

        return self

    def train(self) -> RecommenderEngine:
        if self.algorithm is None:
            raise AlgorithmUnsetError

        self.algorithm \
            .set_interactions(self.interactions_train) \
            .set_articles(self.articles) \
            .train()

        return self

    def get_recommendation(self, user_id: int, top_n: int = 10, exclude: List[int] = None) -> List[List[any, float]]:
        if self.algorithm is None:
            raise AlgorithmUnsetError

        if self.algorithm.is_trained() is False:
            raise UntrainedAlgorithmError

        try:
            recommendations = self.algorithm.get_recommendation(user_id)
        except KeyError:
            print("User ID not found")
            return []

        if exclude is not None:
            recommendations = list(filter(lambda item: item[0] not in exclude, recommendations))

        return recommendations[:top_n]

