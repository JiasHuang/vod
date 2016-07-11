#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import requests
import urllib2

def load(url):
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}
    r = requests.get(url, headers=headers)
    return r.text.encode('utf8')

def loadImage(req, url):
    i = 1
    while i < 30:
        txt = load('%s/%d' %(url, i))
        m = re.search(r'<img id="img" .*? name="img" />', txt)
        if m:
            img = re.search(r'src="([^"]*)"', m.group())
            if img:
                req.write('<li><img src=%s/>\n' %(img.group(1)))
            i+=1
        else:
            break

