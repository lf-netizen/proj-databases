import os
import gridfs
from pymongo import MongoClient

MONGO_URI = os.environ["MONGO_URI"]
MONGO_DATABASE = os.environ["MONGO_DATABASE"]

client = MongoClient(MONGO_URI)
mongodb = client[MONGO_DATABASE]

mongofs = gridfs.GridFS(client[MONGO_DATABASE])
