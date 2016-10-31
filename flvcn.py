#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import base64
import xurl

from xml.etree import ElementTree
from selenium import webdriver

class xmlobj:
    title = ''
    count = 0
    furl = []
    ftype = []
    size = []

def encode64_flvcn(url):
    url = base64.b64encode(url.replace("//", "##"))
    url = url.replace("+", "-")
    url = url.replace("/", "_")
    return url

def genXMLObject(path):

    text = open(path).read()
    root = ElementTree.fromstring(text)
    node_video = root.find('video')
    node_files = node_video.find('files')
    node_file = node_files.getiterator('file')

    obj = xmlobj()
    obj.title = re.sub(' ', '_', node_video.find("title").text)
    for node in node_file:
        obj.furl.append(node.find('furl').text)
        obj.ftype.append(node.find('ftype').text)
        try:
            obj.size.append((int)(node.find('size').text))
        except:
            obj.size.append(0)
        obj.count += 1

    return obj

def genPlayList(path, playlist):
    obj = genXMLObject(path)
    local = open(playlist, 'w')
    for i in range(0, obj.count):
            local.write("%s\n" %(obj.furl[i]))
    local.close()
    return 0

def searchRegex(regex, text, result):
    m = re.search(regex, text)
    if m:
        result.append(m.group())
        return 0
    return -1

def searchVerify(path, verify):

    text = open(path, 'r').read()

    if searchRegex('http://([\w\./=]+)/quality/base64:5YiG5q61X-i2hea4hV9NUDQ=/verify/(\w+)/t/(\d+)', text, verify) != -1:
        print('[flvcn] 分段_超清_MP4')
        return 0

    if searchRegex('http://([\w\./=]+)/quality/base64:5YiG5q61X-i2hea4hV9GTFY=/verify/(\w+)/t/(\d+)', text, verify) != -1:
        print('[flvcn] 分段_超清_FLV')
        return 0

    if searchRegex('http://([\w\./=]+)/quality/base64:5YiG5q61X-mrmOa4hV9NUDQ=/verify/(\w+)/t/(\d+)', text, verify) != -1:
        print('[flvcn] 分段_高清_MP4')
        return 0

    if searchRegex('http://([\w\./=]+)/quality/base64:5YiG5q61X-mrmOa4hV9GTFY=/verify/(\w+)/t/(\d+)', text, verify) != -1:
        print('[flvcn] 分段_高清_FLV')
        return 0

    if searchRegex('http://([\w\./=]+)/quality/base64:5YiG5q61X-agh-a4hV9NUDQ=/verify/(\w+)/t/(\d+)', text, verify) != -1:
        print('[flvcn] 分段_标清_MP4')
        return 0

    if searchRegex('http://([\w\./=]+)/quality/base64:5Y2V5q61X-i2hea4hV9NUDQ=/verify/(\w+)/t/(\d+)', text, verify) != -1:
        print('[flvcn] 单段_超清_MP4')
        return 0

    if searchRegex('http://([\w\./=]+)/quality/base64:5Y2V5q61X-mrmOa4hV9NUDQ=/verify/(\w+)/t/(\d+)', text, verify) != -1:
        print('[flvcn] 单段_高清_MP4')
        return 0

    if searchRegex('http://([\w\./=]+)/quality/base64:5Y2V5q61X-agh-a4hV9NUDQ=/verify/(\w+)/t/(\d+)', text, verify) != -1:
        print('[flvcn] 单段_标清_MP4')
        return 0

    if searchRegex('http://([\w\./=]+)/quality/base64:([\w=-]+)/verify/(\w+)/t/(\d+)', text, verify) != -1:
        print('[flvcn] ???')
        return 0

    print('[flvcn] searchVerify FAIL')
    return -1

def getXML(url, xml):

    # http://www.flvxz.com/api/url/aHR0cDojI3YueW91a3UuY29tL3Zfc2hvdy9pZF9YT0RJMU16WTFORGMyLmh0bWw=
    # /quality/base64:5YiG5q61X-i2hea4hV9GTFY=/verify/83746ae152e00260caa98c3bb1b1dce3/t/1423028918

    encode64 = encode64_flvcn(url)
    remote = 'http://flv.cn/?url=%s' %(encode64)
    result = 'temp.htm'
    verify = []

    xurl.webkit(remote, result)
    if searchVerify(result, verify) != -1:
        xurl.get(verify[0], xml)
        return 0

    xurl.webdrv(remote, result)
    if searchVerify(result, verify) != -1:
        xurl.get(verify[0], xml)
        return 0

    xurl.engine = 'Firefox'
    xurl.webdrv(remote, result)
    if searchVerify(result, verify) != -1:
        xurl.get(verify[0], xml)
        return 0

    print('[flvcn] getXML FAIL')
    return -1
 
