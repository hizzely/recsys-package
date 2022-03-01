# RecSys Content-based Filtering Package

This repository contains the code from Recommender System Content-based Filtering thesis.
This package needs Python >= 3.9 to run.

## Before Use

Currently, this package has strong assumption on how your data is structured.
If you wish to use this, please make sure that:

- Your **articles** data is imported as [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) object and consists of, in no particular order:
  - id: int [[index]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html)
  - title: string
  - author: string
  - categories: list
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

# Load articles and interactions data as DataFrame object
articles: pandas.DataFrame = pandas.read_json('articles.json')
interactions_train: pandas.DataFrame = pandas.read_json('interactions_train.json')

# Instantiate the engine, feed your data, and begin the training
engine = RecommenderEngine().load(articles, interactions_train).train()

while True:
    # Ask for User ID
    user_id = int(input('User ID: '))
    
    # Get list of top-10 recommendation for them
    rec_articles = engine.recommend(user_id, top_n=10)
    print(rec_articles)
    
    # Get list of 10 most relevant tokens for them
    rec_tokens = engine.recommend_tokens(user_id, top_n=10)
    print(rec_tokens)
```

## Development
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
