#!/usr/bin/env python
#coding:utf-8
from common import conf
import urllib2
import cookielib
import urllib
from Cookie import SimpleCookie
import json
import sys
import itertools
from db import insert
logger = conf.logset()
mysql = conf.mysql()
redis = conf.Redis()

cookie='user_trace_token=20170405235238-e516de34-1a17-11e7-9da8-525400f775ce;' \
       ' LGUID=20170405235238-e516e0ee-1a17-11e7-9da8-525400f775ce;' \
       ' JSESSIONID=42D225C6B7A65C834946CBBDB2A593CA;' \
       ' Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1491411399,1491411661,1491487400,1491487575;' \
       ' Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1491493351;' \
       ' PRE_UTM=; PRE_HOST=; PRE_SITE=https%3A%2F%2Fwww.lagou.com%2F;' \
       ' _ga=GA1.2.312126643.1491407581;' \
       ' TG-TRACK-CODE=search_code; SEARCH_ID=5b4153fc6a3143938036b80aa048bbc0'
headers = {'content-type': 'application/x-www-form-urlencoded; charset=UTF-8',
           'Accept-Encoding': 'gzip, deflate',
           'Accept-Language':'zh-CN,zh',
           'Host': 'www.lagou.com',
           'Origin': 'http://www.lagou.com',
           'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36',
           'X-Requested-With': 'XMLHttpRequest',
           'Referer': 'https://www.lagou.com/jobs/list_?labelWords=&fromSearch=true&suginput=',
           'Proxy-Connection': 'keep-alive',
           'X-Anit-Forge-Code': '0',
           'X-Anit-Forge-Token': None}


###这里参考:http://blog.csdn.net/sinat_33741547/article/details/54847950
def post(url,para,headers=None,cookie=None,proxy=None,timeOutRetry=5):
    print 'start............'
    data1=None
    if not url or not para:
        print "url or para is not null"
        logger.error('网址或参数不能为空')
        exit(10)
    logger.info('will post %s to server.......' %url)
    try:
        if not headers:
            print 'set header'
            headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/56.0.2924.87 Safari/537.36'}
        print 'set new opener'
        try:
            #cookie1 = cookielib.CookieJar()
            #cookie1.set_cookie(cookie)
            cookie1=build_opener_with_cookie_str(cookie,'.lagou.com')
            print 'set handler'
            handler=urllib2.HTTPCookieProcessor(cookie1)
            print 'set opener'
            opener = urllib2.build_opener(handler)
            req = urllib2.Request(url,data=para,headers=headers)
        except Exception,e:
            print str(e)
            print e.message
            exit(1)
        try:
            response = opener.open(req)
            print 'start load page'
            data1 = response.read()
        except urllib2.HTTPError, e:
            print "get error code"
            logger.error(str(e))
            logger.error('can not find the page,or page is not get')
            data1=None
    except Exception,e:
        logger.error(str(e))
        logger.error('find error')
        if timeOutRetry>0:
            print "try %d times" %(timeOutRetry)
            post(url,para,headers=headers,cookie=None,proxy=None,timeOutRetry=(timeOutRetry-1))
        else:
            print 'try 5 times,but can not get data'
            logger.error('try 5 times,but can not get data')
            data1 = None
    return data1

###这里是每个值都有domain,path等等的参数，所以将每个值分配这些session的值
###参考:http://blog.csdn.net/tycoon1988/article/details/40536605
def build_opener_with_cookie_str(cookie_str, domain, path='/'):
    simple_cookie = SimpleCookie(cookie_str)    # Parse Cookie from str
    cookiejar = cookielib.CookieJar()    # No cookies stored yet

    for c in simple_cookie:
        domain1=domain
        if c == 'JSESSIONID' or c=='SEARCH_ID' or c== 'TG-TRACK-CODE':
            domain1='www.lagou.com'
        cookie_item = cookielib.Cookie(
            version=0, name=c, value=str(simple_cookie[c].value),
                     port=None, port_specified=None,
                     domain=domain1, domain_specified=None, domain_initial_dot=None,
                     path=path, path_specified=None,
                     secure=None,
                     expires=None,
                     discard=None,
                     comment=None,
                     comment_url=None,
                     rest=None,
                     rfc2109=False,
            )
        ###这里将上面得到最新的like-session赋值到真正需要的session中
        cookiejar.set_cookie(cookie_item)    # Apply each cookie_item to cookiejar
    #return urllib2.build_opener(urllib2.HTTPCookieProcessor(cookiejar))
    return cookiejar

###这是得到职位的基本信息及其搜索的职位数
def json_get_result(data=None,click=False):
    if not data:
        logger.error("无法得到数据")
        exit(10)
    else:
        try:
            page = json.loads(data)
            if click:
                page_list={'result':page['content']['positionResult']['result'],'total_num':page['content']['positionResult']['totalCount'],'pagesize':page['content']['pageSize']}
            else:
                page_list={'result':page['content']['positionResult']['result'],'total_num':page['content']['positionResult']['totalCount']}
            page_list['code']=True
        except Exception,e:
            logger.error(e.message)
            page_list={'result':None,'total_num':page['content']['positionResult']['totalCount'],'pagesize':0,'code':False}
    return page_list


def insert_to_history(position,city,number):
    logger.info('准备插入搜索职位，城市，上海到history表中')
    insert.history(position, city, number)


def insert_to_position(data):
    logger.info('准备插入职业基本信息到position表中')
    for item in data:
        insert.position(item)


kd = raw_input('please input job:').decode(sys.stdin.encoding)
city = raw_input('please input city:').decode(sys.stdin.encoding)
location = {'city':city.encode('utf-8'),'needAddtionalResult':'false','px':'default'}
natuals = itertools.count(1)
count = 0
for i in natuals:
    if count !=0 and i >count:
        logger.info('解析所有的职位信息，系统将退出')
        exit(20)
    url = 'https://www.lagou.com/jobs/positionAjax.json?'
    para = {'pn':i,'kd':kd.encode('utf-8'),'first':'false'}
    get_url = url + urllib.urlencode(location)
####这里最关键，urllib2使用post的方式提交，参考：http://blog.csdn.net/u012374229/article/details/46743877
####会出现json.dumps中文的错误，参考:http://blog.csdn.net/followingturing/article/details/8138365
#page = post(get_url,json.dumps(para),headers=headers,cookie=cookie)
    page = post(get_url, urllib.urlencode(para), headers=headers, cookie=cookie)
#data = json_get_result(page)
    if i ==1:
        data = json_get_result(page,click=True)
    else:
        data = json_get_result(page)
    if not data['code']:
        logger.info('无法解析网页上的数据，遇见错误，退出')
        exit(10)
    for key, item in data.items():
        if key == "result":
            insert_to_position(item)
            pass
        elif key == "total_num" and i == 1:
            insert_to_history(kd, city, item)
            pass
        elif key=='pagesize':
            pagesize = int(item)
            if pagesize == 0:
                logger.error('无法爬取数据，退出')
                exit(10)
            total = data['total_num']
            count = total/pagesize
            if total%pagesize >0:
                count = count +1
            logger.info('本次搜索需要爬取%d个页面' %(count))















