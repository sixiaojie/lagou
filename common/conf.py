#!/usr/bin/env python
#coding:utf-8
import logging
from ConfigParser import ConfigParser
import redis
import MySQLdb

class MyConfigParser(ConfigParser):
    def __init__(self, defaults=None):
        ConfigParser.__init__(self, defaults=None)
    def optionxform(self, optionstr):
        return optionstr
class Setting(object):
    def __init__(self,file='../conf/basic.conf'):
        self.file = file
        self.parser = MyConfigParser()
        self.default = self.fault()
    def Item(self,name):
        try:
            self.parser.read(self.file)
            value = self.default[name]
            try:
                opts = self.parser.options(name)
                for item in opts:
                     value[item]= self.parser.get(name,item)
            except Exception,e:
                pass
        except Exception,e:
            print e.message
            print "%s can't find conf or can't find item in cache" %name
            exit(10)
        return value

###以后添加新的配置，需要在这里写下默认值，以防在配置文件中没有配置
    def fault(self):
        import platform
        import os
        mysql={'host':'127.0.0.1','port':3306}
        red = {'host':'127.0.0.1','port':6379}
        system = platform.architecture()
        if "Windows" in system[1]:
            logfile = 'G:\\eclipse\\4\\lagou\\logs\\access.log'
        else:
            logfile = '/var/log/monitor/error.log'
            os.system('mkdir -p /var/log/monitor/')
            os.system('touch /var/log/monitor/error.log')
        log = {'logfile':logfile}
        return {'mysql':mysql,'logfile':log,'redis':red}


def logset():
    setting = Setting('../conf/basic.conf')
    file = setting.Item('logfile')['logfile']
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',
                        filename=file,
                        filemode='a',)
    return logging

def mysql():
    setting = Setting()
    host=setting.Item('mysql')['host']
    port=setting.Item('mysql')['port']
    user=setting.Item('mysql')['user']
    password=setting.Item('mysql')['password']
    conn = MySQLdb.connect(host=host,port=int(port),user=user,passwd=password,use_unicode=True, charset="utf8")
    return conn.cursor()

def Redis():
    setting = Setting()
    host=setting.Item('redis')['host']
    port=setting.Item('redis')['port']
    re = redis.Redis(host=host, port=int(port))
    return re

'''
class logset(object):
    def __init__(self):
        setting = Setting()
        errorfile = setting.Item('logfile')['error']
        infofile = setting.Item('logfile')['info']
        self.err = self.ERROR()
        self.inf = self.INFO()


    def ERROR(self):
        logging.basicConfig(level=logging.error,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',
                        filename=self.errorfile,
                        filemode='a',)
        return logging


    def INFO(self):
        logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s %(filename)s [line:%(lineno)d] %(levelname)s %(message)s',
                        datefmt='%a,%d %b %Y %H:%M:%S',
                        filename=self.infofile,
                        filemode='a',)
        return logging

    def info(self,data):
        return self.inf.info(data)

    def error(self,data):
        self.inf.info(data)
        self.err.error(data)
'''
'''
mysql = mysql()
mysql.execute('select positionId,companyId from (select id from lagou.position order by id limit 0,100) b left join lagou.position a on b.id = a.id')
#mysql.execute('select id from lagou.position order by id desc limit 1')
a = mysql.fetchall()
print a
'''