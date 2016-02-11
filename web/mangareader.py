#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests, urllib2

def load(url):
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}
    r = requests.get(url, headers=headers)
    return r.text.encode('utf8')

def load2(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    return opener.open(url).read()

def loadImage(req, url):
    i = 1
    while i < 30:
        txt = load('%s/%d' %(url, i))
        m = re.search(r'<img id="img" .*? name="img" />', txt)
        if m:
            req.write('<li class="li">%s' %(m.group()))
            i+=1
        else:
            break
