from pymongo import MongoClient
import uuid
import time
import pandas as pd
import xlrd
def datatakenbyCityName(CityName):
    connection = MongoClient('ds020208.mlab.com', 20208)
    db = connection['assignment2']
    db.authenticate('admin', 'LIjiachen0717')
    collection = db['City']
    collectiondata = collection.find({'collection_id' : 'Cities Data'})
    LL = collectiondata['entries']
    LL_City = []
    for item in LL:
        if item['Cities'] == CityName:
            LL_City.append(item)
    return LL_City

def datatakenbyCityNameandYear(CityName, Year):
    connection = MongoClient('ds020208.mlab.com', 20208)
    db = connection['assignment2']
    db.authenticate('admin', 'LIjiachen0717')
    collection = db['City']
    collectiondata = collection.find({'collection_id': 'Cities Data'})
    LL = collectiondata['entries']
    LL_City = []
    for item in LL:
        if item['Cities'] == CityName and item['year'] == Year:
            LL_City.append(item)
    return LL_City


def datainsertCityData(df2):
    connection = MongoClient('ds020208.mlab.com', 20208)
    db = connection['assignment2']
    db.authenticate('admin', 'LIjiachen0717')
    collection = db['City']
    data_list = []
    data_dict = {}

    for i in range(0,df2.shape[0]):
        dict = {}
        dict['Cities'] = str(df2.loc[i]['Cities'])
        dict['Population'] = int(df2.loc[i]['Population'])
        dict['Public Transport Service Mark']=float(df2.loc[i]['mark for High public transport accessibility'])
        dict['Education Service'] = float(df2.loc[i]['mark for High education accessibility'])
        dict['Health Service'] = float(df2.loc[i]['mark for High health accessibility'])
        dict['Shopping Service'] = float(df2.loc[i]['mark for High shopping accessibility'])
        dict['Employment rate']=float(df2.loc[i]['Employment rate'])
        dict['year'] = int(df2.loc[i]['Year'])
        dict['GDP per capita'] = int(df2.loc[i]['GDP per capita'])
        data_list.append(dict)
    data_dict['collection_id'] = 'Cities Data'
    data_dict['creation_time'] = time.strftime("%Y-%m-%d %H:%M:%S")
    data_dict['entries'] = data_list
    collection.insert_one(data_dict)
    connection.close()




if __name__ == '__main__':
    #df1 = pd.read_csv('9321.csv', index_col=0, skiprows=1)
    df2 = pd.read_excel('Book3.xlsx', skiprows=1)
    #print(df1)
    datainsertCityData(df2)