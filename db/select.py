#coding:utf-8
__author__ = 'Administrator'
from common.conf import mysql,logset
mysql = mysql()
logger = logset()


####查询mysql中数据的个数
def total_count():
    count = 0
    last=0
    try:
        mysql.execute('select count(*) from lagou.position;')
        count = mysql.fetchone()[0]
        mysql.execute('select id from lagou.position order by id desc limit 1')
        last = mysql.fetchone()[0]
    except Exception,e:
        logger.error('查询所有数据出现错误')
    position = [count,last]
    return position


def execute(sql):
    if not sql:
        return None
    try:
        mysql.execute(sql)
        return mysql.fetchall()
    except Exception,e:
        logger.error(str(e))


