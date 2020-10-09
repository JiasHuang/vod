#!/usr/bin/env python
# coding: utf-8

import re

from .utils import *

VALID_URL = r'zuidazy'

def extract(url):
    objs = []
    if re.search(r'vod-type-id', url):
        for m in re.finditer(r'<a href="([^"]*)".*?>(.*?)</a>', load(url)):
            link = urljoin(url, m.group(1))
            title = m.group(2)
            if re.search(r'vod-detail-id', link):
                objs.append(pageObj(link, title))
    elif re.search(r'vod-detail-id', url):
        for m in re.finditer(r'>([^>]*)\$(http[^<]*)<', load(url)):
            title = m.group(1)
            link = m.group(2)
            n = re.search('\.(\w+)$', link)
            if n:
                title = '[%s] %s' %(n.group(1), title)
            objs.append(videoObj(link, title))
    return objs
