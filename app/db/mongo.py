import os
import certifi
from pymongo import MongoClient


MONGO_URI = os.getenv('MONGO_URI')

if not MONGO_URI:
    raise RuntimeError("MONGO_URI not set")


# client = MongoClient(MONGO_URI, tls=True, tlsCAFile=certifi.where(), serverSelectionTimeoutMS=5000)

client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000) #local docker mongo
# client.admin.command("ping")

db = client['cis']
analysis_collection = db['analysis_jobs']