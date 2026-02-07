from pymongo import MongoClient
import json

def export_mongodb_db(db_name: str) -> bytes:
    client = MongoClient("mongodb://mongo:27017")  # 🔥 ВАЖНО
    db = client[db_name]

    dump = {}

    for collection_name in db.list_collection_names():
        collection = db[collection_name]
        dump[collection_name] = list(collection.find({}, {"_id": 0}))

    return json.dumps(dump, ensure_ascii=False, indent=2).encode("utf-8")