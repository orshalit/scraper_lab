import os
import pickle
import pymongo


def save_db(dbClient, save_folder='saved_db'):
    """
    Saves all the data in the local mongo DB in save_db dir.
    :param dbClient: pymongo client
    :param save_folder: local directory, creates it if not exists
    :return: saves all the data to pickle format
    """
    # If save_folder not exists, create one
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    # Databases that wont be saved
    exclude = ['admin', 'config', 'local']
    database_list = dbClient.list_database_names()
    # Loop databases
    for dbName in database_list:
        if dbName not in exclude:
            # Create folder for each database to store collections
            database_folderPath = os.path.join(save_folder, dbName)
            if not os.path.exists(database_folderPath):
                os.mkdir(database_folderPath)
            # Loop collections in each database
            collection_names = dbClient[dbName].list_collection_names()
            for colName in collection_names:
                col_data = list(dbClient[dbName][colName].find())
                with open(os.path.join(database_folderPath, colName) + '.pickle', 'wb') as save_file:
                    pickle.dump(col_data, save_file)


def load_db(dbClient, dbname, load_folder='saved_db'):
    """
    Loads specific database to mongoDB
    :param dbClient: pymongo client
    :param dbname: data base to load
    :param load_folder: data base dir need to exist
    :return: Load the data to the database and creates it. If exists prints load fail and returns
    """
    if dbname in dbClient.list_database_names():
        print(dbname + ' exists. Load FAIL')
        return
    for r, d, f in os.walk(load_folder):
        if len(r) and dbname in r:
            db = dbClient[dbname]
            for file in f:
                if file.endswith('.pickle'):
                    with open(os.path.join(r, file), mode='rb') as read_file:
                        file_data = pickle.load(read_file)
                        db[file[:-7]].insert_many(file_data)


myclient = pymongo.MongoClient('mongodb://localhost:27017')
# save_db(myclient)
load_db(myclient, 'mydatabase')
# load_db(myclient, 'mydatabase')
mydb = myclient["mydatabase"]  # Add new data base
print(myclient.list_database_names())
dblist = myclient.list_database_names()  # Get list of data bases
if "mydatabase" in dblist:
    print("The database exists.")
mycol = mydb["address"]  # Collection
print(mydb.list_collection_names())
collist = mydb.list_collection_names()  # Get list of collections
if "customers" in collist:
    print("The collection exists.")
data = list(mycol.find())
print(data)
# mydict = { "name": "misha", "address": "ass" }
# x = mycol.insert_one(mydict)  # Insert new entry





