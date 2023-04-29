from atexit import register
from json import load, dumps
from redis import StrictRedis
from redis_db import time

with open('sample.json') as data_file:
    data = load(data_file)

db_test = StrictRedis(host='localhost', port=6379)

register(db_test.flushall)

data_zset = {}
for i, d in enumerate(data):
    data_zset[dumps(d)] = i

data_list = []
for d in data:
    data_list.append(dumps(d))


def MeasureTime(meta, func):
    start = time()
    data__ = func()
    end = time()
    print(meta, end - start)
    return data__


print("Downloading:")
MeasureTime("string:", lambda: db_test.set('str', dumps(data)))
MeasureTime("hset:", lambda: db_test.hset('hset', 'test', dumps(data)))
zset = MeasureTime("zset:", lambda: db_test.zadd('zset', data_zset))
llist = MeasureTime("list:", lambda: db_test.lpush('list', *data_list))

print("Geting:")
MeasureTime("string:", lambda: db_test.get('str'))
MeasureTime("hset:", lambda: db_test.hget('hset', 'test'))
MeasureTime("zset:", lambda: db_test.zrangebyscore('zset', 0, zset))
MeasureTime("list:", lambda: db_test.lrange('list', 0, llist))
