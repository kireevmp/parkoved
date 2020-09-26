import os

import pymongo

conn = pymongo.MongoClient(os.getenv("MONGO_URI"))
db = conn["parkoved"]
