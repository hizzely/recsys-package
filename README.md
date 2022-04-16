# Recommender System Package

## Prerequisites
### System Requirements
The only requirements is Python >= 3.9. You can make use of Python Virtual Environment to quickly and easily switch between Python versions. 

### Data Structure
This package currently requires you to structure your data as follows:
- **articles** data is imported as [DataFrame](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.html) object and consists of:
  - [0]: id: int [[index]](https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.set_index.html)
  - [1]: feature: string
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
### Dataset Seeding
If you don't have your own dataset in hand and just want to get started quickly, this code will help you by grabbing Kabar Informatika's articles on Medium, generate random interactions data and then do some processing. It's basically acts like the missing layers below the Recommender Engine.
```python
from pandas import DataFrame
from rscb.helper import save_as_json
from rscb.kabarinformatika import medium, processing, seeder

# Grab articles from Medium
articles: list[dict] = medium.get_articles([
    'https://medium.com/feed/kabarinformatika/tagged/software-engineering',
    'https://medium.com/feed/kabarinformatika/tagged/startup',
    'https://medium.com/feed/kabarinformatika/tagged/Artificial%20Intelligence',
    'https://medium.com/feed/kabarinformatika/tagged/multimedia',
    'https://medium.com/feed/kabarinformatika/tagged/lessons%20learned'
])

# Generate 20 users random interactions
article_ids = [article['id'] for article in articles]
interactions: list[dict] = seeder.generate_interactions(article_ids, 20)

# Perform some preprocessing
articles: DataFrame = processing.prepare_articles(articles)
interactions: DataFrame = processing.prepare_interactions(interactions)

# Export the result, so we can reuse them 
# without repeating the process 
save_as_json(articles.to_dict(), 'articles.json')
save_as_json(interactions.to_dict(), 'interactions.json')
```
Your datasets are now ready, you can remove the code above and follow the example below.

### Generate Recommendation
```python
import pandas
from rscb import RecommenderEngine
from rscb.algorithms import Tfidf

# First, load your processed articles and interactions data 
# as DataFrame objects
articles = pandas.read_json('articles.json')
interactions_train = pandas.read_json('interactions.json')

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
1. Create a new class in `src/rscb/algorithms` using `snake_case` style for file name and `PascalCase` style for class name.
```shell
$ touch ./src/rscb/algorithms/your_algorithm.py
```
2. Extend the `AbstractAlgorithm` class and implements the abstract methods.
```python
from __future__ import annotations
from typing import List
from . import AbstractAlgorithm

class YourAlgorithm(AbstractAlgorithm):
    # Here, you have access to the "articles" and "interactions" 
    # DataFrame properties within parent class.
    
    def get_recommendation(self, user_id: int) -> List[List[any, float]]:
        # put code that generates recommendation here 
        return [[1, 0.91211]]

    def is_trained(self) -> bool:
        # put code that checks whether your algorithm
        # is ready to generate recommendation here
        return False

    def train(self) -> YourAlgorithm:
        # put code that prepares your algorithm here 
        return self
```
3. Optional: Override the DataFrame input setter methods  
If for some reason you need to handle the `articles` and `interactions` DataFrame input by yourself, you can override the methods like so:
```python
...
from pandas import DataFrame

class YourAlgorithm(AbstractAlgorithm):
    ...
    def set_articles(self, articles: DataFrame) -> YourAlgorithm:
        # put your handling code here
        # self.articles = articles
        return self

    def set_interactions(self, interactions: DataFrame) -> YourAlgorithm:
        # put your handling code here
        # self.interactions = interactions
        return self
```
4. Pretty Import  
In order for the consumer to be able to directly import the class instead of module (file) and then the actual class, you have to import the class within the `./src/rscb/algorithms/__init__.py` file. For example:
```python
...
from .your_algorithm import YourAlgorithm
```
5. Your new algorithm is now ready for prime time!
```python
...
from rscb import RecommenderEngine
from rscb.algorithms import YourAlgorithm

...
engine = RecommenderEngine(articles, interactions_train) \
    .set_algorithm(YourAlgorithm) \
    .train()
...
```
6. If you would like to contribute back, please document your new algorithm in the `README.md` and send a pull request!
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
