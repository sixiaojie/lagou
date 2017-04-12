#coding:utf-8
from conf import Redis
from conf import logset
logger = logset()
import json
redis = Redis()
class RedisSetkey_Error(Exception):
    pass
class RedisGetkey_Error(Exception):
    pass

status = {'code':False,'count':0}
def check_redis_insert(data):
    if not data:
        logger.info('数据为空，跳出')
    for item in data:
        key = str(item[2]) + '_' + str(item[4])
        try:
            if check(key):
                print key
            else:
                if not insert(key,json.dumps(item)):
                    return status
                status['count'] = status['count'] + 1
        except Exception,e:
            print str(e)
            logger.error(str(e))
            print "发生错误"
    status['code'] = True
    return status

def check(key):
    if not key:
        return True
    try:
        return redis.get(key)
    except Exception,e:
        print str(e)
        raise RedisGetkey_Error

def insert(key,value):
    try:
        redis.set(key,value)
        return True
    except Exception,e:
        logger.error('插入到redis失败，错误:%s' %(str(e)))
        return False