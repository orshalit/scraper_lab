import twint
from data_base import db


def add_to_DB(db_name, col_name, data, client=db.client):
    for tweet in data:
        db.insert_new_data(client, db_name, col_name, tweet.__dict__)


def querySearch(query, lang, tweets_limit, start_date, end_date, dbName=None, colName=None, save_db=False):
    tweets = list()

    # Configure
    c = twint.Config()
    c.Search = query
    c.Lang = lang
    c.Limit = tweets_limit
    c.Store_object = True
    c.Since = start_date
    c.Until = end_date

    c.Store_object_tweets_list = tweets  # var to save into the tweets
    # Run
    twint.run.Search(c)
    print(tweets)
    # db.insert_new_data(db.client, 'mydatabase', 'customers2', tweets[0].__dict__)

    if save_db is True and dbName is not None and colName is not None:
        add_to_DB(dbName, colName, tweets)
