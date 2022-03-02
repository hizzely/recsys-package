import random


def select_random_events() -> set:
    return set(random.choices(
        ['REACT', 'COMMENT', 'SHARE'], weights=[3, 2, 1], k=random.choice([1, 2, 3])
    ))


def select_random_article_ids(article_ids: list) -> set:
    return set(random.choices(
        article_ids, k=random.choice(range(round(len(article_ids) / 2), len(article_ids), 2))
    ))


def generate_interactions(article_ids: list, user_count: int) -> list:
    interactions = []
    weights = {
        'REACT': 1,
        'COMMENT': 2,
        'SHARE': 3
    }

    for user_id in range(1, user_count + 1):
        for article_id in select_random_article_ids(article_ids):
            for event in select_random_events():
                interactions.append({
                    'user_id': user_id,
                    'article_id': article_id,
                    'event': event,
                    'weight': weights[event]
                })

    return interactions
