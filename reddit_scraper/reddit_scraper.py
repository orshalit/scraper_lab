import requests
import pandas as pd
import pymongo
import json
import pprint
from data_base import db

pp = pprint.PrettyPrinter()

# query = ""  # Define Your Query
# url = f"https://api.pushshift.io/reddit/search"
# request = requests.get(url)
# json_response = request.json()


def redditQuery(data_type='submission', q=None, after='7d', size=10, sort_type='score', sort='desc', aggs='subreddit'):
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
    ans_data = request.json()
    ans_data = ans_data.get("data")

    # Select the columns you care about
    if data_type == 'comment':
        df = pd.DataFrame.from_records(ans_data)[["author", "subreddit", "score", "body", "permalink"]]
    elif data_type == 'submission':
        df = pd.DataFrame.from_records(ans_data)[["author", "subreddit", "score", "permalink"]]

    # Append the string to all the permalink entries so that we have a link to the comment
    df['permalink'] = "https://reddit.com" + df['permalink'].astype(str)

    # # Create a function to make the link to be clickable and style the last column
    # def make_clickable(val):
    #     """ Makes a pandas column clickable by wrapping it in some html.
    #     """
    #     return '<a href="{}">Link</a>'.format(val, val)
    #
    # df.style.format({'permalink': make_clickable})

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

    return ans_data


def redditQueryGUI(data_type, gui_data, save=False):
    def split_dict(gui_values):
        """
        :Input: The dict from the GUI window
        :Output: 2 dict objects
        1 - params - parameters for the request to the api
        2 - check_box - check box stats for the column chooser
        """
        params = dict()
        check_box_stat = dict()
        for key in gui_values.keys():
            if key.startswith('check'):
                check_box_stat[key] = gui_values[key]
            else:
                if key in ('after', 'before') and gui_values[key] == '0':
                    continue
                if isinstance(gui_values[key], str) and not len(gui_values[key]):  # checks if not empty string
                    continue
                else:
                    params[key] = gui_values[key]
        return params, check_box_stat

    # Record the values of database inputs
    db_name = gui_data['db_name']
    db_collection = gui_data['col_name']
    del gui_data['db_name']
    del gui_data['col_name']

    # If query empty
    if not len(gui_data['q']):
        print('Error - no query entered !')
        return

    # define end point to work on
    end_point = f'https://api.pushshift.io/reddit/search/{data_type}/'

    # build argument dict
    payload, check_box = split_dict(gui_data)
    payload['aggs'] = 'subreddit'

    # build URL
    request = requests.get(end_point, params=payload)
    ans_data = request.json()
    print(ans_data)

    # Data manipulation
    data = dict()

    # Store aggs data if Check box Meta-Data is Set
    if check_box['check_meta'] is True:
        data['aggs'] = ans_data.get('aggs').get('subreddit')
    # Store data
    column_selector = [key.replace('check_', '') for key in check_box.keys() if check_box[key] is True and key not in ('check_meta', 'check_data')]
    print(column_selector)

    # Convert to pandas data frame for easier column selections
    df = pd.DataFrame.from_records(ans_data.get('data'))[column_selector]
    df.reset_index(inplace=True)
    df_dict = df.to_dict('record')
    record = json.dumps(df_dict)
    pp.pprint(df_dict)
    data['record'] = df_dict

    if save is True:
        if not len(db_name) or not len(db_collection):
            print('ERROR - missing value')
            return
        db.insert_new_data(db.client, db_name + '_' + data_type, db_collection, data)

"""
test before we go into GUI
"""
# data = redditQuery(data_type='submission', q='corona virus')
