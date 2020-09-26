import pymongo

from .common import db

parks: pymongo.collection.Collection = db.parks
users: pymongo.collection.Collection = db.users
tickets: pymongo.collection.Collection = db.tickets
services: pymongo.collection.Collection = db.services

admins: pymongo.collection.Collection = db.admins
