#!/usr/bin/env python3
""" Python module """
from pymongo import MongoClient

if __name__ == "__main__":
    """
    Provides some stats about Nginx logs stored in MongoDB
    """
    client = MongoClient('mongodb://127.0.0.1:27017')
    nginx_collection = client.logs.nginx

    print("{} logs".format(nginx_collection.count_documents({})))

    methods = ["GET", "POST", "PUT", "PATCH", "DELETE"]
    print("Methods:")
    for method in methods:
        count = len(list(nginx_collection.find({'method': method})))
        print("\tmethod {}: {}".format(method, count))

    status_check = len(list(nginx_collection.find(
          {"method": "GET", "path": "/status"})))
    print("{} status_check".format(status check))
