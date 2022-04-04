# Recommender System Package

## Prerequisites
### System Requirements
The only requirements is Python >= 3.9. You can make use of Python Virtual Environment to quickly and easily switch between Python versions. 

### Data Structure
This package currently requires you to structure your data as follows:
- **articles** data is imported as [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) object and consists of:
  - id: int [[index]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html)
  - title: string
  - author: string
  - categories: list[string]
  - content: string
- **interactions** data is imported as [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) object and consists of:
  - user_id: int [[index]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html)
  - article_id: int
  - weight: int
  
## Installation
### From PyPI
TBD

### Local
1. Clone or download this repository. If you prefer to download, make sure to extract it.
2. Open your terminal and prepare your Python 3.9+ virtual environment  
3. Install the package using:
```shell
$ pip install -e /path/to/cloned/repository
```

## Usage Example
### Generate Recommendation
```python
import pandas
from rscb import RecommenderEngine
from rscb.algorithms import Tfidf

# First, load your processed articles and interactions data 
# as DataFrame objects
articles = pandas.read_json('articles.json')
interactions_train = pandas.read_json('interactions_train.json')

# Then, prepare the engine by feeding your data 
# and algorithm of your choice.
engine = RecommenderEngine(articles, interactions_train) \
    .set_algorithm(Tfidf) \
    .train()

# The recommender engine is now ready to use!
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
```
### Swapping Data or Algorithm
```python
# If you wish, you could swap the data
# while the code is running (runtime)
engine.set_articles(other_articles)
engine.set_interactions(other_interactions)

# you could even swap the algorithm:
engine.set_algorithm(OtherAlgorithm)

# then re-train the engine with your new data and/or algorithm:
engine.train()

# on the next iteration, it will use your newly trained engine!
```
### Available Algorithms
- `Tfidf`: `from rscb.algorithms import Tfidf`

## Development
### Manual Environment Setup (Conda)
```shell
$ cd /path/to/cloned/repo
$ conda env create -f environment.yml
```
### Adding New Algorithm
TBA

### Get Articles From Medium RSS Feed
```python
from rscb.kabarinformatika.medium import get_articles
from rscb.helper import save_as_json

articles: list[dict] = get_articles([
    'https://medium.com/feed/kabarinformatika/tagged/software-engineering',
    'https://medium.com/feed/kabarinformatika/tagged/startup',
])

save_as_json(articles, "articles.json")
```

### Interaction Seeding
```python
from rscb.kabarinformatika.seeder import generate_interactions
from rscb.helper import save_as_json

# load or get the articles
articles: list[dict] = get_articles([...])

# get article ids
article_ids: list[int] = [item['id'] for item in articles]

# generate random interactions for 100 users
interactions = generate_interactions(article_ids, 100)

save_as_json(interactions, "interactions.json")
```


### Build as Distributable Package
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
