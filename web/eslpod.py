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

def loadWord(req, url):

    dictCambridge = 'http://dictionary.cambridge.org/dictionary/english-chinese-traditional/'
    dictWebster = 'http://www.merriam-webster.com/dictionary/'
    dictYahoo = 'https://tw.dictionary.yahoo.com/dictionary?p='

    txt = load('%s' %(url))
    match = re.finditer(r'<b>([^<]*)</b>', txt)

    req.write('<ul>')
    req.write('<font size=6>')

    for m in match:
        q = m.group(1)
        q = q.replace('\n', '')
        q = q.replace('\r', '')
        q = q.replace(' ', '+')
        req.write('<li>%s <a href=%s>[Cambridge]</a> <a href=%s>[Webster]</a> <a href=%s>[Yahoo]</a>'
            %(q, dictCambridge+q, dictWebster+q, dictYahoo+q))

    req.write('</ul>')
