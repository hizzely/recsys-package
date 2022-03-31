# RecSys Content-based Filtering Package

This repository contains the code from Recommender System Content-based Filtering thesis.
This package needs Python >= 3.9 to run.

## Before Use

Currently, this package has strong assumption on how your data are structured.
If you wish to use this, please make sure that:

- Your **articles** data is imported as [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) object and consists of, in no particular order:
  - id: int [[index]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html)
  - title: string
  - author: string
  - categories: list[string]
  - content: string
- Your **interactions** data is imported as [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) object and consists of, in no particular order:
  - user_id: int [[index]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html)
  - article_id: int
  - weight: int
  
## Installation
### From PyPI
TBD

### From cloned repository (local src)
```shell
$ pip install -e <path-to-cloned-repo-dir>
```

## Usage Example
```python
import pandas
from rscb import RecommenderEngine
from rscb.algorithms import Tfidf

# Load articles and interactions data as DataFrame object
articles = pandas.read_json('articles.json')
interactions_train = pandas.read_json('interactions_train.json')

# Instantiate the engine with your data, set the algorithm 
# and begin the training
engine = RecommenderEngine(articles, interactions_train) \
    .set_algorithm(Tfidf) \
    .train()

while True:
    # Ask for User ID
    user_id = int(input('User ID: '))
    
    # Get top-10 recommendation list
    rec_articles = engine.get_recommendation(user_id, top_n=10)
    print(rec_articles)
    """
    [
        [6, 0.44964621922670145],
        [5, 0.44681090276765234],
        [13, 0.422595724105032], 
        [4, 0.4102558133893252], 
        [20, 0.37241621122757607], 
        [21, 0.338862085090948], 
        [19, 0.338152993132529], 
        [3, 0.30724768322975554], 
        [18, 0.21848086296148467], 
        [16, 0.2174022565527912]
    ]
    """

    # If you wish, you could swap the data at this point:
    # engine.set_articles(other_articles)
    # engine.set_interactions(other_interactions)
    #
    # ... or even swap the algorithm:
    # engine.set_algorithm(OtherAlgorithm)
    # 
    # ... then re-train the engine with your new data and/or algorithm:
    # engine.train()
    #
    # on the next iteration, it will use your newly trained engine!
```

## Development
### Adding New Algorithm
TBA

### Build the package as distributable
- On Windows
```shell
$ pip install --upgrade build
$ py -m build
```
- On Linux or Mac
```shell
$ python3 -m pip install --upgrade build
$ python3 -m build
```
More on the [documentation](https://packaging.python.org/en/latest/tutorials/packaging-projects/#generating-distribution-archives).


## License

MIT
