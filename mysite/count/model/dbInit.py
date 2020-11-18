import pymongo
from config import mongodbConfig

class db():
    def conn(self):
        conn = pymongo.MongoClient(mongodbConfig.host,mongodbConfig.port)[mongodbConfig.dbname]
        conn.authenticate(mongodbConfig.username,mongodbConfig.password,mechanism='SCRAM-SHA-1')  
        return conn
