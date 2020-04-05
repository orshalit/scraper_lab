"""
Author: Tzvi puchinsky
"""

import PySimpleGUI as sg
from reddit_scraper import reddit_scraper as rs
from datetime import datetime

date = str(datetime.date(datetime.now())).replace('-', '_')  # Get current date and put in collection default name

in_size = 45  # size of the input fields: query and author

sg.change_look_and_feel('Dark Blue 3')

submission_tab_layout = [
    [sg.Text('Query Search:', size=(10, 1)), sg.Input(key='s_q', size=(in_size, 1))],
    [sg.Text('Author:', size=(10, 1)), sg.Input(key='s_author', size=(in_size, 1))],
    [sg.Text('Size:', size=(5, 1)), sg.Spin(key='s_size', values=[i for i in range(10, 1000, 10)], initial_value=10), sg.Text('After:', size=(5, 1)), sg.Spin(key='s_after', values=[i for i in range(1, 100)], initial_value=0),
     sg.Text('Before:', size=(5, 1)), sg.Spin(key='s_before', values=[i for i in range(1, 100)], initial_value=0)],
    [sg.Checkbox('Meta-Data', size=(12, 1), key='s_check_meta', default=True),
     sg.Checkbox('Data', key='s_check_data', default=True)],
    [sg.Frame(layout=
              [[sg.Checkbox('Author', size=(10, 1), key='s_check_author', default=True),
                sg.Checkbox('Number of Comments', size=(20, 1), key='s_check_num_comments', default=True),
                sg.Checkbox('Self text', size=(10, 1), key='s_check_selftext', default=True)],
               [sg.Checkbox('Score', size=(10, 1), key='s_check_score', default=True),
                sg.Checkbox('Subreddit', size=(10, 1), key='s_check_subreddit', default=True),
                sg.Checkbox('Title', size=(7, 1), key='s_check_title', default=True),
                sg.Checkbox('Date', size=(8, 1), key='s_check_created_utc', default=True),
                sg.Checkbox('Full link', size=(10, 1), key='s_check_full_link', default=True)],
               ],
              title='Columns', title_color='white', relief=sg.RELIEF_SUNKEN)],
    [sg.Button('Search!', key='s_search_button')],
    [sg.Frame(layout=
              [[sg.Text('Data base name:', size=(15, 1)), sg.Input(key='s_db_name', size=(25, 1), default_text='reddit')],
               [sg.Text('Collection name:', size=(15, 1)), sg.Input(key='s_col_name', size=(25, 1), default_text=date)],
               [sg.Button('Search & Save', key='s_searchSave_button')]],
              title='Data Base Parameters', title_color='white', relief=sg.RELIEF_SUNKEN, element_justification='center')]
]

comment_tab_layout = [
    [sg.Text('Query Search:', size=(10, 1)), sg.Input(key='c_q', size=(in_size, 1))],
    [sg.Text('Author:', size=(10, 1)), sg.Input(key='c_author', size=(in_size, 1))],
    [sg.Text('Size:', size=(5, 1)), sg.Spin(key='c_size', values=[i for i in range(10, 1000, 10)], initial_value=10), sg.Text('After:', size=(5, 1)), sg.Spin(key='c_after', values=[i for i in range(1, 100)], initial_value=0),
     sg.Text('Before:', size=(5, 1)), sg.Spin(key='c_before', values=[i for i in range(1, 100)], initial_value=0)],
    [sg.Checkbox('Meta-Data', size=(12, 1), key='c_check_meta', default=True),
     sg.Checkbox('Data', key='c_check_data', default=True)],
    [sg.Frame(layout=
              [[sg.Checkbox('Author', size=(10, 1), key='c_check_author', default=True),
                sg.Checkbox('Body', size=(10, 1), key='c_check_body', default=True)],
               [sg.Checkbox('Score', size=(10, 1), key='c_check_score', default=True),
                sg.Checkbox('Date', size=(10, 1), key='c_check_created_utc', default=True), sg.Checkbox('Permalink', size=(10, 1), key='c_check_permalink', default=True)],
               ],
              title='Columns', title_color='white', relief=sg.RELIEF_SUNKEN)],
    [sg.Button('Search!', key='c_search_button')],
    [sg.Frame(layout=
              [[sg.Text('Data base name:', size=(15, 1)), sg.Input(key='c_db_name', size=(25, 1), default_text='reddit')],
               [sg.Text('Collection name:', size=(15, 1)), sg.Input(key='c_col_name', size=(25, 1), default_text=date)],
               [sg.Button('Search & Save', key='c_searchSave_button')]],
              title='Data Base Parameters', title_color='white', relief=sg.RELIEF_SUNKEN, element_justification='center')]
]

master_layout = [
    [sg.TabGroup([[sg.Tab('Submission', submission_tab_layout, element_justification='center'), sg.Tab('Comment', comment_tab_layout, element_justification='center')]])]
]

window = sg.Window('Reddit Query', master_layout, font=("Helvetica", 12), element_justification='center')


def split_value_dict(arg, value):
    """
    Possible Inputs to arg: s_ for submission OR c_ for comment
    This functions takes the whole values dict from the GUI input and returns
    new dict with the only relevant keys (without the s_ or c_)
    """
    new_dict = dict()
    for key in value.keys():
        if key.startswith(arg):
            new_dict[key[2:]] = value[key]
    return new_dict


while True:
    event, values = window.read()
    # If used the submission tab
    if event is 's_search_button' or event is 's_searchSave_button':
        save = False
        if event is 's_searchSave_button':
            save = True
        rs.redditQueryGUI('submission', split_value_dict('s_', values), save=save)
    # If used the comment tab
    if event is 'c_search_button' or event is 'c_searchSave_button':
        save = False
        if event is 'c_searchSave_button':
            save = True
        rs.redditQueryGUI('comment', split_value_dict('c_', values), save=save)
    if event is None:  # always,  always give a way out!
        break
