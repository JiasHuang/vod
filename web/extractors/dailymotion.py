#!/usr/bin/env python
# coding: utf-8

import re
import json

from .utils import *

VALID_URL = r'dailymotion'

def parseDailyMotionJSON(url):
    data = json.loads(load(url))
    log(json.dumps(data, indent=4))
    objs = []
    if 'list' not in data:
        return None
    for d in data['list']:
        try:
            vid, title = darg(d, 'id', 'title')
            link = 'http://www.dailymotion.com/video/'+vid
            image = 'http://www.dailymotion.com/thumbnail/video/'+vid
            seconds = d['duration']
            m, s = divmod(seconds, 60)
            h, m = divmod(m, 60)
            desc = '%d:%02d:%02d' %(h, m, s)
            objs.append(entryObj(link, title, image, desc))
        except:
            continue

    return objs

def extract(url):
    if url.startswith('https://api.dailymotion.com'):
        return parseDailyMotionJSON(url)
    else:
        return [obj.to_video() for obj in findImageLink(url)]

def search_dailymotion(q, x=None):
    url = 'https://api.dailymotion.com/videos/?search="'+q+'"&limit=100&fields=id,title,duration'
    return parseDailyMotionJSON(url)


