import requests
import pandas as pd
import pymongo

query = "" #Define Your Query
url = f"https://api.pushshift.io/reddit/search"
request = requests.get(url)
json_response = request.json()




def redditQuery(data_type='submission',q=None, after='7d' ,size=10 ,sort_type='score' ,sort='desc',aggs='subreddit'):
    """
    Gets data from the pushshift api.

    data_type can be 'comment' or 'submission' default is 'submission
    The rest of the args are interpreted as payload.

    Read more: https://github.com/pushshift/api
    """

    base_url = f"https://api.pushshift.io/reddit/search/{data_type}/"

    # build argument dict
    payload = locals()

    # clean dict from unwanted args
    del payload['data_type']
    del payload['base_url']

    # build URL
    request = requests.get(base_url, params=payload)
    data = request.json()
    data = data.get("data")

    # Select the columns you care about
    if data_type == 'comment':
      df = pd.DataFrame.from_records(data)[["author", "subreddit", "score", "body", "permalink"]]
    elif data_type == 'submission':
      df = pd.DataFrame.from_records(data)[["author", "subreddit", "score", "permalink"]]

    # Append the string to all the permalink entries so that we have a link to the comment
    df['permalink'] = "https://reddit.com" + df['permalink'].astype(str)

    # Create a function to make the link to be clickable and style the last column
    def make_clickable(val):
        """ Makes a pandas column clickable by wrapping it in some html.
        """
        return '<a href="{}">Link</a>'.format(val, val)

    df.style.format({'permalink': make_clickable})

# SAVE TO DB:::
    myclient = pymongo.MongoClient("mongodb://localhost:27017/")
    mydb = myclient["Reddit"]
    dblist = myclient.list_database_names()
    mycol = mydb['queries']
    collist = mydb.list_collection_names()
    df.reset_index(inplace=True)
    df_dict = df.to_dict('records')

    # save to DB with the query as index
    mycol.insert_one({"index": q, "data": df_dict})

    return data


"""test before we go into GUI"""
# data = redditQuery(data_type='comment',q='corona virus')