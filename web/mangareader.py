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

def load2(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    return opener.open(url).read()

def loadFile(filename):
    f = open(os.path.dirname(os.path.abspath(__file__))+'/'+filename, 'r')
    return f.read()

def render(req, filename, result):
    html = loadFile(filename+'.html')
    if result:
        txt = ''
        for img in result:
            txt += '<li><img src=%s />\n' %(img)
        html = re.sub('<!--result-->', txt, html)
    req.write(html)

def loadImage(req, url):
    result = []
    i = 1
    while i < 30:
        txt = load('%s/%d' %(url, i))
        m = re.search(r'<img id="img" .*? name="img" />', txt)
        if m:
            img = re.search(r'src="([^"]*)"', m.group())
            if img:
                result.append(img.group(1))
            i+=1
        else:
            break

    render(req, 'list', result)

