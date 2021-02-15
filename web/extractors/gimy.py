#!/usr/bin/env python
# coding: utf-8

import re

from .utils import *

VALID_URL = r'gimy\.co'

def extract(url):
    objs = []
    if re.search(r'/cat/', url):
        for m in re.finditer(r'data-original="([^"]*)" href="([^"]*)" title="([^"]*)"', load(url)):
            image = m.group(1)
            link = urljoin(url, m.group(2))
            title = m.group(3)
            objs.append(pageObj(link, title, image))
    elif re.search(r'/vod/', url):
        m = re.search(r'<div class="playlist">(.*?)</div>', load(url), re.DOTALL|re.MULTILINE)
        if m:
            playlist = m.group()
            for x in re.finditer(r'<li><a href="([^"]*)">(.*?)</a></li>', playlist):
                link = urljoin(url, x.group(1))
                title = x.group(2)
                objs.append(videoObj(link, title))
    return objs

def search_gimy(q, start=None):
    objs = []
    url = 'https://gimy.co/search/-------------.html?wd=%s' %(q)
    for m in re.finditer(r'href="([^"]*)" title="([^"]*)" data-original="([^"]*)"', load(url)):
        link = urljoin(url, m.group(1))
        title = m.group(2)
        image = m.group(3)
        objs.append(pageObj(link, title, image))
    return objs
