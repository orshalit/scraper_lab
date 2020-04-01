import PySimpleGUI as sg
from twitter.twitter_scrap import querySearch
from data_base import db
import os

sg.change_look_and_feel('Dark Blue 3')

layout = [[sg.Frame(layout=
                    [[sg.Text('Search query: ', size=(10, 1)), sg.Input(key='search_query')],
                     [sg.Text('Language: ', size=(10, 1)), sg.Input(key='lang', default_text=('en'), size=(10, 1))],
                     [sg.Text('No. of tweets: ', size=(10, 1)),
                      sg.Spin(key='tweet_limit', values=[i for i in range(20, 1000, 20)], initial_value=100,
                              size=(6, 1))],
                     [sg.Text('Start Date: ', size=(10, 1)),
                      sg.Input(key='year' + 'start', default_text='YYYY', size=(5, 1)),
                      sg.Input(key='month' + 'start', default_text='MM', size=(3, 1)),
                      sg.Input(key='day' + 'start', default_text='DD', size=(3, 1)), sg.Text('End Date: '),
                      sg.Input(key='year' + 'end', default_text='YYYY', size=(5, 1)),
                      sg.Input(key='month' + 'end', default_text='MM', size=(3, 1)),
                      sg.Input(key='day' + 'end', default_text='DD', size=(3, 1))],
                     [sg.Button('Search!', key='search_q')]],
                    title='Query options', title_color='white', relief=sg.RELIEF_SUNKEN)],
          [sg.Frame(layout=
                    [[sg.Text('Data base name:', size=(15, 1)), sg.Input(key='db_name', size=(25, 1))],
                     [sg.Text('Collection name:', size=(15, 1)), sg.Input(key='col_name', size=(25, 1))],
                     [sg.Button('Search and Add to DB', key='searchAndSave'), sg.Button('Save DB', key='save_db')]],
                    title='Data Base Parameters', title_color='white', relief=sg.RELIEF_SUNKEN)]
          ]

window = sg.Window('Twitter Query', layout, font=("Helvetica", 12))

while True:
    event, values = window.read()
    print()
    if event in ('search_q', 'searchAndSave'):
        search_query = values['search_query']
        lang = values['lang']
        numberOfTweets = int(values['tweet_limit'])
        start_date = values['yearstart'] + '-' + values['monthstart'] + '-' + values['daystart']
        end_date = values['yearend'] + '-' + values['monthend'] + '-' + values['dayend']
        if event == 'searchAndSave':
            querySearch(search_query, lang, numberOfTweets, start_date, end_date, values['db_name'], values['col_name'],
                        save_db=True)
        else:
            querySearch(search_query, lang, numberOfTweets, start_date, end_date)
    if event == 'save_db':
        os.chdir(os.path.sep.join(os.getcwd().split(os.path.sep)[:-1]))
        db.save_db(db.client, save_folder='data_base/saved_db')
    if event is None:
        break

# region Date Layout
# date_layout = [sg.Input(key='year' + key, default_text='YYYY', size=(5, 1)),
#                sg.Input(key='month' + key, default_text='MM', size=(3, 1)),
#                sg.Input(key='day' + key, default_text='DD', size=(3, 1))]
# endregion
