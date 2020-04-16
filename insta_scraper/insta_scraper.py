import argparse
import os, json
import pymongo
import sys
import subprocess
import instalooter
import glob
from skimage.io import imread
import numpy as np


basefunc = 'python -m instalooter'
numofpic = '-n'
curdirectory = 'Instagramphotos'
directory_todb = 'C:/Users/allak/PycharmProjects/scraper_lab/GUI/Instagramphotos/*'


def instagram(name=None,mode='hashtag',num='10',mdata=True,pic=True):
    bashCommand = 'python -m instalooter login -u alla19021962 -p 123456abc'
    subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE).stdout.read()
    if mdata == True and pic == True:
        command = ' '.join([basefunc, '-d', mode, name, curdirectory, numofpic, num])
    elif mdata == True and pic == False:
        command = ' '.join([basefunc, '-D', mode, name, curdirectory, numofpic, num])
    elif mdata == False and pic == True:
        command = ' '.join([basefunc, mode, name, curdirectory, numofpic, num])
    print(f'Current command: {command}')
    subprocess.Popen(command, shell=True, stdout=subprocess.PIPE).stdout.read()

    bashCommand = 'python -m instalooter logout'
    subprocess.Popen(bashCommand, shell=True, stdout=subprocess.PIPE).stdout.read()
    save_db()


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["insta"]
dblist = myclient.list_database_names()
mycol = mydb['scrap']
collist = mydb.list_collection_names()



def save_db():
    data_p = []
    data_j = []
    for f in glob.glob(directory_todb):
        # print('file name:',f)
        if f.endswith(".json"):
            with open(f) as jfile:
                jfile = json.load(jfile)
                mycol.insert_one({"data": jfile})
            os.unlink(f)



