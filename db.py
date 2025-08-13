from pymongo import MongoClient

# Change this to your MongoDB URI
client = MongoClient("mongodb://localhost:27017/")

db = client["mydatabase"]  # Database name
person_collection = db["persons"]  # Collection name
