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

    def push(self, url, title):
        try:
            self.db.insert(
                {
                    '_id': url,
                    'status': self.OUTSTANDING,
                    '主题': title
                }
            )
            print(url, u'插入队列成功')
        except errors.DuplicateKeyError as e:
            print(url, u'已经在队列中了')
            pass

    def push_imgurl(self, title, url):
        try:
            self.db.insert(
                {
                    '_id': title,
                    'status': self.OUTSTANDING,
                    'url':url
                }
            )
            print('图片地址插入成功')
        except errors.DuplicateKeyError as e:
            print(u'地址已经存在了')
            pass

    def pop(self):
        '''
        这个函数会查询队列中的所有状态为OUTSTANDING的值，
        更改状态，（query后面是查询）（update后面是更新）
        并返回_id（就是我们的ＵＲＬ），MongDB好使吧，^_^
        如果没有OUTSTANDING的值则调用repair()函数重置所有超时的状态为OUTSTANDING，
        $set是设置的意思，和MySQL的set语法一个意思
        :return:
        '''
        record = self.db.find_and_modify(
            query={'status': self.OUTSTANDING},
            update={
                '$set': {'status':self.PROCESSING, 'timestamp': datetime.now()}
            }
        )
        if record:
            return record['_id']
        else:
            self.repair()
            raise KeyError

    def pop_title(self, url):
        record = self.db.find_one(
            {'status': self.OUTSTANDING}
        )
        return record['_id']


