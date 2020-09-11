#!/usr/bin/env python
# coding: utf-8

import re

import xurl
from .utils import *

VALID_URL = r'pianku\.tv'

def extract(url):
    objs = []
    basename = url.split('/')[-1]
    if len(basename) == 15:
        url_tv = 'https://www.pianku.tv/ajax/downurl/%s_tv/' %(basename[0:10])
        local_cookie = xurl.genLocal(url, suffix='.cookie')
        opts = []
        opts.append('-c %s' %(local_cookie))
        xurl.curl(url, opts=opts)
        opts = []
        opts.append('-b %s' %(local_cookie))
        opts.append('-H \'x-requested-with: XMLHttpRequest\'')
        opts.append('-H \'referer: %s\'' %(url))
        txt = xurl.curl(url_tv, opts=opts)
        for m in re.finditer(r'<li><a href="([^"]*)">(.*?)</a></li>', txt):
            link, title = urljoin(url, m.group(1)), m.group(2)
            objs.append(entryObj(link, title))
    else:
        for m in re.finditer(r'<a href="(.*?)" title="(.*?)" target="_blank"><img src="(.*?)"', load(url)):
            link, title, img = urljoin(url, m.group(1)), m.group(2), urljoin(url, m.group(3))
            objs.append(pageObj(link, title, img))

    return objs
