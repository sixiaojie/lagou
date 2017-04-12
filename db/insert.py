#!/usr/bin/env python
#coding:utf-8
import sys
import json
from common.conf import logset,mysql
mysql = mysql()
logger = logset()
import sys
reload(sys)
sys.setdefaultencoding('utf8')

def history(posi, city, num):
    try:
        mysql.execute('insert into lagou.history(search_position,city,total_num) values("%s","%s",%d)' % (posi, city, int(num)))
        mysql.execute('commit;')
        logger.info("插入%s %s 到history成功" %(posi,city))
    except Exception, e:
        logger.error(str(e))
        print 'inserto table history is failed ,error: %s' % (str(e))


def set_json(data):
    if type(data) is list:
        return json.dumps("".join(data), ensure_ascii=False).encode('utf8')
    elif type(data) is dict:
        pass
    else:
        return json.dumps(data, ensure_ascii=False).encode('utf8')


def position(data):
    try:
        mysql.execute("insert into lagou.position(positionId, positionName, companyId, companyShortName, salary, company_type, \
                      benifit, district, createTime, formatCreateTime, positionAdvantage, firstType, secondType, positionLables, businessZones) values(%d, '%s', %d, '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', %s)"
                      % (int(data[u'positionId']), data[u'positionName'], int(data[u'companyId']), data[u'companyShortName'], set_json(data[u'salary']),
                        set_json(data[u'industryField']), set_json(data[u'companyLabelList']), data[u'district'], data[u'createTime'], data[u'formatCreateTime'],
                        set_json(data[u'positionAdvantage']), set_json(data[u'firstType']), set_json(data[u'secondType']), set_json(data[u'positionLables']), set_json(data[u'businessZones'])))
        mysql.execute('commit')
        logger.info("%s %s 插入成功" % (data['positionName'], data['companyShortName']))
    except Exception,e:
        logger.error('find error in inserting to table position ,error: %s' % (str(e)))
        mysql.execute('rollback')
