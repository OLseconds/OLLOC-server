import pymongo


class Db:
    def __init__(self, host, user, db, pwd):
        self.connection = pymongo.MongoClient('mongodb://%s:%s@%s/%s' % (user, pwd, host, db))
        self.db = self.connection['locations']
        self.user_coll = self.db.user
