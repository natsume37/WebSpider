import pymongo
from bson import ObjectId

# pip install pymongo
client = pymongo.MongoClient(host='localhost', port=27017)
# client = pymongo.MongoClient('mongodb://localhost:27017')

db = client['test']
# db = client.test

collection = db['student']
# collection = db.student

student = {
    'id': '20250101',
    'name': 'xiaohua',
    'age': 20,
    'gender': 'male'
}

# 插入数据

# res = collection.insert_one(student)
#
# print(res)

# 查询数据
# res = collection.find_one({'name': 'xiaohua'})
# print(type(res))
# print(res)

# 根据objectID查询
# res = collection.find_one({'_id':ObjectId('6802056a471f2312fe87303a')})
# print(res)

# 查询age大于20的数据
res = collection.find({'age': {'$lte': 20}})
print(res)