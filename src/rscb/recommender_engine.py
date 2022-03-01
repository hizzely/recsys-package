import nltk
import numpy
import sklearn
from nltk.corpus import stopwords
from pandas import DataFrame
from scipy.sparse import csr_matrix, vstack
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class RecommenderEngine:
    articles: DataFrame
    articles_profiles: csr_matrix
    articles_features: numpy.ndarray
    interactions_train: DataFrame
    users_profiles: dict

    def __init__(self):
        nltk.download('stopwords')

    def load(self, articles: DataFrame, interactions_train: DataFrame):
        self.articles = articles
        self.interactions_train = interactions_train

        return self

    def train(self):
        self._build_articles_profiles()
        self._build_users_profiles()

        return self

    def recommend(self, user_id: int, top_n=10, exclude_article_ids=[]) -> DataFrame:
        similar_articles = self._get_similar_articles(user_id)

        similar_articles = similar_articles \
            .query('article_id not in @exclude_article_ids') \
            .reset_index(drop=True)

        return similar_articles[:top_n]

    def recommend_tokens(self, user_id: int, top_n=100) -> DataFrame:
        result = zip(self.articles_features, self.users_profiles[user_id].flatten().tolist())
        result = sorted(result, key=lambda x: -x[1])
        result = DataFrame(result[:top_n], columns=['token', 'relevance'])

        return result

    def _build_articles_profiles(self):
        # Build the corpus
        corpus = []

        for i in range(len(self.articles)):
            article = self.articles.loc[i]
            document = f"{article['title']} {article['content']} {article['author']} "
            document += ' '.join(article['categories'])
            corpus.append(document)

        # Convert the corpus (collection of raw documents) to a matrix of TF-IDF features
        vectorizer: TfidfVectorizer = TfidfVectorizer(
            analyzer='word',
            stop_words=stopwords.words('indonesian') + stopwords.words('english'),
            ngram_range=(1, 2),
            max_features=10000  # limit to 10k features, or terms, from the most frequent term
        )

        self.articles_profiles = vectorizer.fit_transform(corpus)
        self.articles_features = vectorizer.get_feature_names_out()

    def _build_users_profiles(self):
        self.users_profiles = {}

        for user_id in self.interactions_train.index.unique():
            # get interactions data for this user
            interaction = self.interactions_train.loc[user_id]
            interacted_articles_profiles = []

            for article_id in set(interaction['article_id']):
                article_index = self.articles[self.articles['id'] == article_id].index.values[0]
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

    def _get_similar_articles(self, user_id, top_n=100) -> DataFrame:
        # get the similarity between this user profile and our articles profiles
        cosine_similarities: numpy.ndarray = cosine_similarity(
            self.users_profiles[user_id],
            self.articles_profiles
        )

        # list of index of similar articles within top-n
        similar_indices = cosine_similarities.argsort().flatten()[-top_n:]

        # list of article id and it's similarity value
        similar_articles = [(self.articles['id'][i], cosine_similarities[0, i]) for i in similar_indices]

        # transform the list into dataframe then sort by
        # its similarity value in descending order
        similar_articles = DataFrame(similar_articles, columns=['article_id', 'strength']) \
            .sort_values(by=['strength'], ascending=False, ignore_index=True)

        return similar_articles
