#!/usr/bin/env python
# coding: utf-8

import re
import json
import time

from .utils import *

VALID_URL = r'bilibili'

def extract(url):
    objs = []
    txt = load(url)
    if re.search(r'/video/', url):
        m = re.search(r'__INITIAL_STATE__=(.*?});', txt);
        if m:
            data = json.loads(m.group(1))
            try:
                image = darg(data['videoData'], 'pic')
                for vp in data['videoData']['pages']:
                    if re.search(r'\?', url):
                        link = url+'&p='+str(vp['page'])
                    else:
                        link = url+'?p='+str(vp['page'])
                    title = darg(vp, 'part')
                    desc = time.strftime('%H:%M:%S', time.gmtime(vp['duration']))
                    objs.append(entryObj(link, title, image, desc))
            except:
                print('Exception:\n'+str(data))

        else:
            for m in re.finditer(r'"page":(\d+),"from":"[^"]*","part":"([^"]*)","duration":(\d+)', txt):
                if re.search(r'\?', url):
                    link = url+'&p='+m.group(1)
                else:
                    link = url+'?p='+m.group(1)
                title = m.group(2)
                desc = time.strftime('%H:%M:%S', time.gmtime(int(m.group(3))))
                objs.append(entryObj(link, title, desc=desc))

    return objs

def search_bilibili(q, x=None):
    objs = []
    url = 'https://api.bilibili.com/x/web-interface/search/type?jsonp=jsonp&search_type=video&keyword='+q
    jsonTxt = load(url)
    data = json.loads(jsonTxt)
    try:
        for res in data['data']['result']:
            arcurl, title, pic, duration = darg(res, 'arcurl', 'title', 'pic', 'duration')
            title = re.sub('<.*?>', '', title)
            title = re.sub('</.*?>', '', title)
            objs.append(pageObj(arcurl, title, pic, duration))
    except:
        print('Exception:\n'+str(data))

    return objs
