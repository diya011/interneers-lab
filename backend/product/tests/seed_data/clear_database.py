from mongoengine.connection import get_db

def clear_database():
    db = get_db()
    for collection_name in db.list_collection_names():
        db.drop_collection(collection_name)
