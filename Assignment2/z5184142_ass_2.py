import requests
from flask import Flask
from flask import request
from flask_restplus import Resource, Api
from flask_restplus import fields
from pymongo import MongoClient
import uuid
import time
from bs4 import BeautifulSoup
app = Flask(__name__)
api = Api(app,
          default="Ass2",
          title="Comp9321 Ass2",
)

indicator_model = api.model('indicator', {"indicator_id" : fields.String })


def sortmaxvalue(list, list_sort):
    dict = list[0]
    if dict['value'] == 'null':
        dict['value'] = -1
    for item in list:
        if item['value'] == 'null':
            item['value'] = -1
        if item['value'] > dict['value']:
            dict = item
    if dict['value'] == -1:
        dict['value'] = 'null'
    list_sort.append(dict)
    list.remove(dict)
    if list == []:
        return list_sort
    sortmaxvalue(list, list_sort)


def sortminvalue(list, list_sort):
    dict = list[0]
    if dict['value'] == 'null':
        dict['value'] = -1
    for item in list:
        if item['value'] == 'null':
            item['value'] = -1
        if item['value'] <= dict['value']:
            dict = item
    if dict['value'] == -1:
        dict['value'] = 'null'
    list_sort.append(dict)
    list.remove(dict)
    if list == []:
        return list_sort
    sortminvalue(list, list_sort)


@api.route('/worldbanks')
class Worldbanks(Resource):
    @api.doc(description="Retrieve the list of available collections")
    @api.response(200, 'Get Data Successful.')
    def get(self):
        connection = MongoClient('ds020208.mlab.com', 20208)
        db = connection['assignment2']
        db.authenticate('admin', 'LIjiachen0717')
        collection = db['worldbanks']
        collectiondata = collection.find()
        data_list = []
        for item in collectiondata:
            dict = {}
            dict["location"] = "/worldbanks/" + item["collection_id"]
            dict["collection_id"] = item["collection_id"]
            dict["creation_time"] = item["creation_time"]
            dict["indicator"] = item["indicator"]
            data_list.append(dict)
        connection.close()
        return data_list, 200

    @api.doc(description="Import a Collection from the data service")
    @api.expect(indicator_model, validate=True)
    @api.response(200, 'The Data of Indicator Has Been Imported.')
    @api.response(201, 'Insert Successful.')
    @api.response(404, 'Indicator Does Not Exist.')
    def post(self):
        indicator = request.json
        indicator = str(indicator).split("'")[3]
        connection = MongoClient('ds020208.mlab.com', 20208)
        db = connection['assignment2']
        db.authenticate('admin', 'LIjiachen0717')
        collection_id = db['indicators']
        collection = db['worldbanks']
        collectiondata = collection.find()
        for item in collectiondata:
            if item["indicator"] == indicator:
                return {"message":"The indicator {} has been imported".format(indicator)},200
        collectionindicator = collection_id.find_one({'id' : 'indicators'})['entries']
        if indicator not in collectionindicator:
            return {"message": "The input is Invalid Indicators"}, 404
        else:
            content = requests.get(f'http://api.worldbank.org/v2/countries/all/indicators/{indicator}?date=2012:2017&format=json&per_page=2000').json()
            data_dict = {}
            data_list = []
            for i in range(len(content[1])):
                dict={}
                dict["country"]=str(content[1][i]["country"]["value"])
                dict["date"]=str(content[1][i]["date"])
                dict["value"] = str(content[1][i]["value"])
                if dict["value"] == 'None':
                    dict["value"] = 'null'
                if dict["value"] != 'null':
                    dict["value"]=float(dict["value"])
                data_list.append(dict)
            id = uuid.uuid4()
            data_dict["collection_id"] = str(id)
            data_dict["indicator"] = indicator
            data_dict["indicator_value"] = str(content[1][0]["indicator"]["value"])
            data_dict["creation_time"] = time.strftime("%Y-%m-%d %H:%M:%S")
            data_dict["entries"] = data_list
            collection.insert_one(data_dict)
            connection.close()
            return { "location" : "/worldbanks/{}".format(id),
                 "collection_id" : "{}".format(id),
                 "creation_time" : "{}".format(data_dict["creation_time"]),
                 "indicator" : "{}".format(indicator)
                }, 201

    @api.route('/worldbanks/<string:collection_id>')
    class Worldbanks(Resource):
        @api.doc(descrpition="Retrieve a collection")
        @api.response(404,'The Data of the collection_id Does Not In the Database')
        @api.response(200,'Getting The Data successfully')
        def get(self, collection_id):
            connection = MongoClient('ds020208.mlab.com', 20208)
            db = connection['assignment2']
            db.authenticate('admin', 'LIjiachen0717')
            collection = db['worldbanks']
            data = collection.find_one({"collection_id" : collection_id})
            if data is None:
                {"message": "Collection {} doesn't exist.".format(collection_id)}, 404
            connection.close()
            dict = {}
            dict['collection_id'] = data['collection_id']
            dict["indicator"] = data["indicator"]
            dict["indicator_value"] = data["indicator_value"]
            dict["creation_time"] = data["creation_time"]
            dict["entries"] = data["entries"]
            return dict, 200

        @api.doc(description="Deleting a collection with the data service")
        def delete(self, collection_id):
            connection = MongoClient('ds020208.mlab.com', 20208)
            db = connection['assignment2']
            db.authenticate('admin', 'LIjiachen0717')
            collection = db['worldbanks']
            if collection.find_one({'collection_id': collection_id}) == None:
                connection.close()
                return {"message": "Collection {} doesn't exist.".format(collection_id)}, 404
            collection.delete_one({'collection_id' : collection_id})
            connection.close()
            return {"message" :"Collection = {} is removed from the database!".format(collection_id)}, 200


    @api.route('/worldbanks/<string:collection_id>/<int:year>/<string:country>')
    class WorldBanks(Resource):
        @api.doc(description="Retrieve economic indicator value for given country and a year")
        @api.response(200, 'Query Successful.')
        @api.response(404, 'The Data of The Collection Does Not Exist In The Database.')
        def get(self, collection_id,year,country):
            connection = MongoClient('ds020208.mlab.com', 20208)
            db = connection['assignment2']
            db.authenticate('admin', 'LIjiachen0717')
            collection = db['worldbanks']
            data = collection.find_one({'collection_id' : collection_id})
            dict = {}
            if data is None:
                {"message": "Collection {} doesn't exist.".format(collection_id)}, 404
            for item in data["entries"]:
                if (item['country'] == country) and (item['date'] == str(year)):
                    dict['collection_id'] = collection_id
                    dict['indicator'] = data['indicator']
                    dict['country'] = country
                    dict['year'] = year
                    dict['value'] = item['value']
            connection.close()
            return dict, 200

    @api.route('/worldbanks/<string:collection_id>/<int:year>')
    @api.param('q','Use topN or bottom N for query')
    class WorldBanks(Resource):
        @api.doc(description="Retrieve economic indicator value for given country and a year.")
        @api.response(400, 'Query not meet the format.')
        @api.response(200, 'Query Successful.')
        @api.response(404, 'The Data of Collection_id Does Not In The Database.')
        def get(self, collection_id, year):
            query =request.args.get('q')
            if (query[0:3].lower() != 'top') and (query[0:6].lower() != 'bottom'):
                return {"message": "Query {} do not meet format.".format(query)}, 400
            connection = MongoClient('ds020208.mlab.com', 20208)
            db = connection['assignment2']
            db.authenticate('admin', 'LIjiachen0717')
            collection = db['worldbanks']
            data = collection.find_one({"collection_id": collection_id})
            dict = {}
            if data is None:
                return {"message": "Collection {} doesn't exist.".format(collection_id)}, 404
            LL = []
            L= []
            dict['indicator'] = data['indicator']
            dict['indicator_value'] = data['indicator_value']
            for item in data['entries']:
                if item['date'] == str(year):
                    LL.append(item)
            number = ''
            for item in query:
                if item.isdigit():
                    number += item
            number = int(number)
            if query[0:3].lower() == 'top':
                sortmaxvalue(LL,L)
            else:
                sortminvalue(LL,L)
            LL.clear()
            for i in range(0,number):
                if i > len(L)-1:
                    break
                else:
                    LL.append(L[i])
            dict["entries"] = LL
            return dict,200


if __name__ == '__main__':
    #Check whether the indicator_id has been imported to the database or not.
    connection = MongoClient('ds020208.mlab.com', 20208)
    db = connection['assignment2']
    db.authenticate('admin', 'LIjiachen0717')
    collection = db['indicators']
    if collection.find_one({'id' : 'indicators'}) is None:
        content = requests.get('http://api.worldbank.org/v2/indicators?per_page=10000').content
        soup = BeautifulSoup(content, 'xml')
        LL = []
        for item in soup.find_all('wb:indicator'):
            LL.append(str(item).split('\n')[0].split('"')[1])
        dict = {}
        dict['id'] = 'indicators'
        dict['entries'] = LL
        collection.insert_one(dict)
    connection.close()
    app.run(debug=True)


