from __future__ import annotations
from abc import ABC, abstractmethod
from typing import List
from pandas import DataFrame


class AbstractAlgorithm(ABC):
    articles: DataFrame
    interactions: DataFrame

    @abstractmethod
    def get_recommendation(self, user_id: int) -> List[List[any, float]]:
        raise NotImplementedError

    @abstractmethod
    def is_trained(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def train(self) -> AbstractAlgorithm:
        raise NotImplementedError

    def set_articles(self, articles: DataFrame) -> AbstractAlgorithm:
        self.articles = articles
        return self

    def set_interactions(self, interactions: DataFrame) -> AbstractAlgorithm:
        self.interactions = interactions.set_index('user_id')
        return self
