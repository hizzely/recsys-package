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
  - event: string
  - weight: int

## Installation

TBA

## Usage

TBA

## License

MIT
