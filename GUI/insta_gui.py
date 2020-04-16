import PySimpleGUI as sg
from insta_scraper import insta_scraper
from datetime import datetime

date = str(datetime.date(datetime.now())).replace('-', '_')  # Get current date and put in collection default name

in_size = 45  # size of the input fields: query and author

sg.change_look_and_feel('Dark Blue 3')

layout = [
          [sg.Frame(layout=
                    [[sg.Text('Hashtag: ', size=(10, 1)), sg.Input(key='search_hashtag')],
                     [sg.Text('Num of pic: ', size=(10, 1)),
                      sg.Spin(key='hpic_limit', values=[i for i in range(1, 100, 1)], initial_value=10,
                              size=(6, 1))],
                     [sg.Button('Search&Save', key='search_h')],
                     [sg.Checkbox('Meta-Data', size=(12, 1), key='h_check_meta', default=True),
                      sg.Checkbox('Pictures', key='h_check_pic', default=True)]
                     ],
                    title='Query options', title_color='white', relief=sg.RELIEF_SUNKEN)],
          [sg.Frame(layout=
              [[sg.Text('User Name: ', size=(10, 1)), sg.Input(key='search_user')],
               [sg.Text('Num of pic: ', size=(10, 1)),
                sg.Spin(key='upic_limit', values=[i for i in range(1, 100, 1)], initial_value=10,
                        size=(6, 1))],
               [sg.Button('Search&Save', key='search_u')],
               [sg.Checkbox('Meta-Data', size=(12, 1), key='p_check_meta', default=True),
                sg.Checkbox('Pictures', key='p_check_pic', default=True)]
               ],
              title='Query options', title_color='white', relief=sg.RELIEF_SUNKEN)],
          [sg.Frame(layout=
                    [[sg.Text('Data base name:', size=(15, 1)),
                      sg.Input(key='s_db_name', size=(25, 1), default_text='insta')],
                     [sg.Text('Collection name:', size=(15, 1)),
                      sg.Input(key='s_col_name', size=(25, 1), default_text=date)]],
                    title='Data Base Parameters', title_color='white', relief=sg.RELIEF_SUNKEN,
                    element_justification='center')]
          ]

window = sg.Window('Instagram Query', layout, font=("Helvetica", 12), element_justification='center')


def split_value_dict(arg, value):

    new_dict = dict()
    for key in value.keys():
        if key.startswith(arg):
            new_dict[key[2:]] = value[key]
    return new_dict


while True:
    event, values = window.read()
    print()
    if event in ('search_h','search_u'):
        if event == 'search_h':
            search_query = values['search_hashtag']
            if search_query == '':
                break
            else:
                numberOfPictures = str(values['hpic_limit'])
                insta_scraper.instagram(search_query,'hashtag',numberOfPictures,values['h_check_meta'],values['h_check_pic'])
        if event == 'search_u':
            search_query = values['search_user']
            if search_query == '':
                break
            else:
                numberOfPictures = str(values['upic_limit'])
                insta_scraper.instagram(search_query,'user',numberOfPictures,values['p_check_meta'],values['p_check_pic'])
    if event is None:
        break


