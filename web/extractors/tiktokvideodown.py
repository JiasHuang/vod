#!/usr/bin/env python
# coding: utf-8

import re

from .utils import *

VALID_URL = r'tiktokvideodown'

class defs:
    domain = 'http://www.tiktokvideodown.com'

def extract(url):
    objs = []
    if re.search(r'vod-read-id', url):
        for m in re.finditer(r'href="(/.*?vod-play-id-[^"]*)" title="(.*?)"', load(url)):
            link, title = defs.domain + m.group(1), m.group(2)
            objs.append(entryObj(link, title))
    elif re.search(r'(list-read-id|list-select-id)', url):
        for m in re.finditer(r'<h5><a href="(.*?)" title=".*?">(.*?)</a></h5>', load(url)):
            link, title = defs.domain + m.group(1), m.group(2)
            objs.append(pageObj(link, title))

    return objs

def search_tiktokvideodown(q, start=None):
    objs = []
    url = defs.domain + '/vod-search-wd-%s.html' %(q)
    for m in re.finditer(r'<h5><a href="(.*?)" title=".*?">(.*?)</a></h5>', load(url)):
        link, title = defs.domain + m.group(1), m.group(2)
        objs.append(pageObj(link, title))

    return objs

