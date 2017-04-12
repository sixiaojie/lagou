#!/usr/bin/env python
#coding:utf-8
import redis
import json
import sys
reload(sys)
sys.setdefaultencoding('utf8')
from db.select import total_count,execute
from common.conf import logset
from common.rsync import check_redis_insert
logger = logset()
first = '准备同步'
error="发现错误，请看日志"
second = "统计数据库的个数:"
third="开始同步"

step = 100
print first
logger.info(first)

result = total_count()
count = result[0]
last = result[1]
if count == 0:
    print error
    logger.error(error)
print second,count
logger.info(second+str(count))

print third
logger.info(third)

limit = 1
print last,count
times = last/step
if last%step:
    times = times + 1
n = 0
for i in range(times):
    if limit >= last:
        break
    try:
        print "这次将要搜索%d-%d" %(limit,limit + step)
        sql = "select * from (select id from lagou.position order by id limit %d ,%d) b left join lagou.position a on b.id = a.id" %(limit,step)
        print sql
        data = execute(sql)
        print data
        if not data:
            logger.error('无法从数据库中获取数据')
            continue
        status = check_redis_insert(data)
        n  = n + status['count']
        if not status['code']:
            logger.error('redis处理过程中发生错误')
        limit = limit + step
    except Exception,e:
        print "fount error:%s" %(e.message)
        logger.error("fount error:%s" %(e.message))
        print "同步到%d" %(limit)
        logger.info("同步到%d" %(limit))
        exit(20)
print "同步结束，这次共涉及了%d条数据，被同步的数据%d条" %(count,n)
logger.info("同步结束，这次共涉及了%d条数据，被同步的数据%d条" %(count,n))


