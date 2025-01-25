from pkg.database import mongo

def register_mongodb():
    uri = ""
    db_name = ""
    mongo.MongoDB.get_instance(uri=uri, database_name=db_name)