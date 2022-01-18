import pandas
import math
import nltk
import numpy
import time
from nltk.corpus import stopwords
from pandas import DataFrame
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize as skl_normalize
from scipy.sparse import csr_matrix
from scipy.sparse import vstack

APP_START = time.time()

nltk.download('stopwords')


#################################################
# DATASET PREPARATION
#################################################

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
interactions_train: DataFrame
interactions_test: DataFrame
interactions_train, interactions_test = train_test_split(
    interactions,
    stratify=interactions['user_id'],
    test_size=0.20,
    random_state=42
)

# Make 'user_id' as index label
# We can then access it using: df.loc[user_id]
interactions = interactions.set_index('user_id')
interactions_train = interactions_train.set_index('user_id')
interactions_test = interactions_test.set_index('user_id')


#################################################
# BUILD THE RECOMMENDER SYSTEM
#################################################

# Build the corpus
corpus = []
for i in range(len(articles)):
    article = articles.loc[i]
    document = f"{article['title']} {article['content']} {article['author']} "
    document += ' '.join(article['categories'])
    corpus.append(document)

# Convert the corpus (collection of raw documents) to a matrix of TF-IDF features
vectorizer: TfidfVectorizer = TfidfVectorizer(
    analyzer='word',
    stop_words=stopwords.words('indonesian') + stopwords.words('english'),
    ngram_range=(1, 2),
    max_features=10000  # limit to 5000 features, or terms, from the most frequent term
)

vectors: csr_matrix = vectorizer.fit_transform(corpus)

feature_names: numpy.ndarray = vectorizer.get_feature_names_out()

# Visualize articles relevance by tokens
# pdas = DataFrame(vectors.toarray(), index = articles['id'], columns = feature_names)


def build_users_profiles(tfidf_vectors: csr_matrix, articles: DataFrame, interactions_train: DataFrame):
    user_profiles = {}

    for user_id in interactions_train.index.unique():
        # get interactions data for this user
        user_interactions = interactions_train.loc[user_id]

        # get articles profiles (the vectors)
        article_vectors = []
        for article_id in set(user_interactions['article_id']):
            # get the profile from generated vectors
            article_index = articles[articles['id'] == article_id].index.values[0]
            # collect
            article_vectors.append(tfidf_vectors[article_index])
        article_vectors = vstack(article_vectors)

        # Vertical
        interactions_weight = numpy.array(user_interactions['weight']).reshape(-1, 1)

        # axis 0 = sum in vertical axis
        interactions_weighted_avg = numpy.sum(article_vectors.multiply(interactions_weight), axis=0) / numpy.sum(
            interactions_weight)

        # normalize the weight.
        # FIXME: this part trigger the np.matrix deprecation warning
        profile = skl_normalize(interactions_weighted_avg)

        user_profiles[user_id] = profile

    return user_profiles


#################################################
# USING THE SYSTEM
#################################################

user_profiles = build_users_profiles(vectors, articles, interactions_train)

APP_READY = time.time()


def get_user_relevance_tokens(user_id, total, user_profiles, feature_names):
    result = zip(feature_names, user_profiles[user_id].flatten().tolist())
    result = sorted(result, key=lambda x: -x[1])
    result = DataFrame(result[:total], columns=['token', 'relevance'])
    return result


def create_recommendation(
        article_ids,
        vectors,
        user_profiles,
        interactions_train: DataFrame,
        user_id,
        total: int,
        exclude_interacted_articles=True) -> DataFrame:
    # find the similarities between this user's profile and our article profiles.
    # return the strength/similarity of each article.
    cosine_similarities: numpy.ndarray = cosine_similarity(user_profiles[user_id], vectors)

    similar_indices = cosine_similarities.argsort().flatten()[-total:]

    similar_articles: list = [(article_ids[i], cosine_similarities[0, i]) for i in similar_indices]

    similar_articles: DataFrame = DataFrame(similar_articles, columns=['article_id', 'strength']) \
        .sort_values(by=['strength'], ascending=False, ignore_index=True)

    if exclude_interacted_articles:
        interacted_articles_ids = pandas.unique(interactions_train.loc[user_id]['article_id'])
        similar_articles = similar_articles.query('article_id not in @interacted_articles_ids').reset_index(drop=True)

    return similar_articles


print(f"Ready. Startup time: {round(APP_READY - APP_START, 3)}s")

while True:
    # TODO: What if the user has seen all articles? wouldn't that make the recommendation list empty?
    user_id = int(input('Input the User ID: '))
    recommendation_count = int(input('How many recommendation do you want? '))

    # Tell user's interacted articles
    interacted_article_ids = interactions_train.loc[user_id]['article_id']
    interacted_articles = articles.query('id in @interacted_article_ids')

    print("You've interacted with these articles in the past:")
    print(interacted_articles[['id', 'title']])
    print("")

    print("Those articles contain these keywords:")
    print(get_user_relevance_tokens(user_id, recommendation_count, user_profiles, feature_names))
    print("")

    # Give article recommendations
    recommendations: DataFrame = create_recommendation(
        article_ids=articles['id'],
        vectors=vectors,
        user_profiles=user_profiles,
        interactions_train=interactions_train,
        user_id=user_id,
        total=recommendation_count,
        exclude_interacted_articles=True
    )
    recommendations_total = len(recommendations)

    if recommendations_total > 0:
        print("Therefore, you might be interested in these other similar articles:")
        for i in range(recommendations_total):
            recommendation: DataFrame = recommendations.loc[i]
            article = articles[articles['id'] == recommendation['article_id']].iloc[0]
            print(f"- {article['id']}: {article['title']} ({recommendation['strength']})")
    else:
        print("But we have no other similar content left :(")
