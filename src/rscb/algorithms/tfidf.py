from __future__ import annotations
import nltk
import numpy
import sklearn
from nltk.corpus import stopwords
from scipy.sparse import csr_matrix, vstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List
from . import AbstractAlgorithm


class Tfidf(AbstractAlgorithm):
    articles_profiles: csr_matrix
    users_profiles: dict

    def __init__(self):
        nltk.download('stopwords')
    
    def get_recommendation(self, user_id: int) -> List[List[any, float]]:
        return self._get_similar_articles(user_id)

    def is_trained(self) -> bool:
        return (self.articles_profiles is not None) and (self.users_profiles is not None)

    def train(self) -> Tfidf:
        self._build_articles_profiles()
        self._build_users_profiles()

        return self
    
    def _build_articles_profiles(self):
        # Convert the corpus (collection of raw documents) to a matrix of TF-IDF features
        vectorizer = TfidfVectorizer(
            analyzer='word',
            stop_words=stopwords.words('indonesian') + stopwords.words('english'),
            ngram_range=(1, 2),
            max_features=10000  # limit to 10k features, or terms, from the most frequent term
        )

        self.articles_profiles = vectorizer.fit_transform(self.articles[1].values)

    def _build_users_profiles(self):
        self.users_profiles = {}

        for user_id in self.interactions.index.unique():
            # get interactions data for this user
            interaction = self.interactions.loc[user_id]
            interacted_articles_profiles = []

            for article_id in set(interaction['article_id']):
                article_index = self.articles[self.articles[0] == article_id].index.values[0]
                interacted_articles_profiles.append(self.articles_profiles[article_index])

            interacted_articles_profiles = vstack(interacted_articles_profiles)

            # change array shape to vertical
            interactions_weight = numpy.array(interaction['weight']).reshape(-1, 1)

            # axis 0 = sum in vertical axis
            interactions_weighted_avg = numpy.sum(interacted_articles_profiles.multiply(interactions_weight), axis=0)
            interactions_weighted_avg /= numpy.sum(interactions_weight)

            # normalize the weight.
            # FIXME: this part trigger the np.matrix deprecation warning
            profile = sklearn.preprocessing.normalize(interactions_weighted_avg)

            self.users_profiles[user_id] = profile

    def _get_similar_articles(self, user_id) -> List[List[any, float]]:
        # get the similarity between this user profile and our articles profiles
        cosine_similarities: numpy.ndarray = cosine_similarity(
            self.users_profiles[user_id],
            self.articles_profiles
        )

        # list of index of similar articles in descending order
        similar_indices = cosine_similarities.argsort().flatten()[::-1]

        # list of article id and it's similarity value
        similar_articles = [[int(self.articles[0][i]), float(cosine_similarities[0, i])] for i in similar_indices]

        return similar_articles
