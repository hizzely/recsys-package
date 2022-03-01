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
    """
       article_id  strength
    0           5  0.510365
    1           6  0.471760
    2           3  0.405593
    3           4  0.396926
    4          16  0.360467
    5          13  0.332750
    6          19  0.295908
    7          20  0.254306
    8          17  0.224291
    9          11  0.190918
    """
    
    # Get list of 10 most relevant tokens for them
    rec_tokens = engine.recommend_tokens(user_id, top_n=10)
    print(rec_tokens)
    """
                   token  relevance
    0         programmer   0.271327
    1         netiquette   0.231728
    2           software   0.190719
    3        programming   0.173984
    4           engineer   0.138856
    5             petruk   0.114394
    6  software engineer   0.110435
    7                end   0.099107
    8               data   0.097384
    9             bahasa   0.092796
    """
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
