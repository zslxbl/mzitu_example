from datetime import datetime, timedelta
from pymongo import MongoClient, errors

class MogoQueue():
    OUTSTANDING = 1
    PROCESSING = 2
    COMPLATE = 3

    def __int__(self, db, collection, timeout=300):
        self.client = MongoClient()
        self.Client = self.client[db]
        self.db = self.Client[collection]
        self.timeout = timeout

    def __bool__(self):
        '''
        这个函数的，我的理解是如果下面的表达式为真，则整个类为真
        :return:
        '''

        record = self.db.find_one(
            {'status': {'$ne': self.COMPLATE}}
        )
        return True if record else False

