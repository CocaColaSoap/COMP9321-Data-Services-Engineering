import pymongo
from pymongo import MongoClient
import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
import io
import base64
def data_extract(cityname, factor1, factor2, factor3):
    connection = MongoClient('ds020208.mlab.com', 20208)
    db = connection['assignment2']
    db.authenticate('admin', 'LIjiachen0717')
    collection = db['City']
    collectiondata = collection.find({'collection_id': 'Cities Data'})
    cities = []
    for doc in collectiondata:
        for data in doc['entries']:
            cities.append(data['Cities'])
    cities = list(set(cities))

    cities_dict = {}

    connection = MongoClient('ds020208.mlab.com', 20208)
    db = connection['assignment2']
    db.authenticate('admin', 'LIjiachen0717')
    collection = db['City']
    collectiondata = collection.find({'collection_id': 'Cities Data'})
    for doc in collectiondata:
        for city in cities:
            list1 = []
            for data in doc['entries']:
                list2 = []
                if city == data['Cities']:
                    list2.append(data[factor1])
                    list2.append(data[factor2])
                    list2.append(data[factor3])
                    # list2.append(data['Health Service Mark'])
                    # list2.append(data['Shoppingg Service Mark'])
                    # list2.append(data['Employment rate'])
                    list2.append(data['GDP per capita'])
                if list2:
                    list1.append(list2)
            cities_dict[city] = list1
    # for ele in cities_dict:
    #     print(ele)
    #     for ele2 in cities_dict[ele]:
    #         print(ele2)
    cities_dict[cityname].reverse()
    return cities_dict[cityname]

def predict(data_lst,years_ahead):
    print(data_lst)
    matrix = np.array(data_lst)
    n = matrix.shape[0]
    prediction = []
    for year_ahead in range(1,years_ahead+1):
        X = matrix[:n - year_ahead, 0:3]
        y = matrix[year_ahead:n, 3:4]
        x = matrix[-1:, 0:3]
        prediction.append(regression(X,y,x))
    return prediction

def regression(X,y,x):
    reg = LinearRegression().fit(X,y)
    y = reg.predict(x)
    return round(y[0][0],3)

def main(city,factor1,factor2,factor3,years_ahead):
    img = io.BytesIO()

    data_lst = data_extract(city, factor1, factor2, factor3)
    prediction_lst = predict(data_lst,years_ahead)
    x = list()
    for i in range(2019,2019+years_ahead):
        x.append(i)
    plt.plot(x,prediction_lst)
    plt.xticks(x)
    plt.ylabel('GDP($AUD) per capita')
    plt.xlabel('Year')
    for a,b in zip(x, prediction_lst): 
        plt.text(a, b, str(b))
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    img.close()
    plt.close()
    return plot_url

def analysisbycityname(city):
    img = io.BytesIO()
    data_lst = data_extract(city, "Health Service Mark", 'Shoppingg Service Mark', 'Employment rate')
    prediction_lst = predict(data_lst, 5)
    x = list()
    for i in range(2019, 2019 + 5):
        x.append(i)
    plt.plot(x, prediction_lst)
    plt.xticks(x)
    plt.ylabel('GDP($AUD) per capita')
    plt.xlabel('Year')
    for a, b in zip(x, prediction_lst):
        plt.text(a, b, str(b))
    plt.savefig(img, format='png')
    img.seek(0)
    plot_url = base64.b64encode(img.getvalue()).decode()
    img.close()
    plt.close()
    return plot_url
#main("Perth","Health Service Mark",'Shoppingg Service Mark','Employment rate',5)

