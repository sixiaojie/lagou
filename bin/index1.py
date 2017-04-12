#!/usr/bin/env python
#coding:utf-8
from common import conf
import urllib2
import cookielib
import urllib
from Cookie import SimpleCookie
import json
import sys
logger = conf.logset()

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

def  json_trans_dict(data=None):
    return json.loads(data)

kd=raw_input('please input job:').decode(sys.stdin.encoding)
city=raw_input('please input city:').decode(sys.stdin.encoding)
location={'city':city.encode('utf-8'),'needAddtionalResult':'false','px':'default'}
para = {'pn':1,'kd':kd.encode('utf-8'),'first':'false'}
url='https://www.lagou.com/jobs/positionAjax.json?'
get_url = url + urllib.urlencode(location)
print get_url
print city
print para
####这里最关键，urllib2使用post的方式提交，参考：http://blog.csdn.net/u012374229/article/details/46743877
####会出现json.dumps中文的错误，参考:http://blog.csdn.net/followingturing/article/details/8138365
#page = post(get_url,json.dumps(para),headers=headers,cookie=cookie)
page = post(get_url,urllib.urlencode(para),headers=headers,cookie=cookie)
#page = post(url,para,headers=headers,cookie=cookie)
#page = json.loads(page)
#for position in page['content']['hrInfoMap']:
    #print position
#print page['content']['positionResult']['result'][0].keys()

f = open('G:\\temp\\lagou.log','w')
f.write(page)
f.close()













