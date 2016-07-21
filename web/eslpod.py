#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests, urllib2
import meta

def loadWord(req, url):

    dictCambridge = 'http://dictionary.cambridge.org/dictionary/english-chinese-traditional/'
    dictWebster = 'http://www.merriam-webster.com/dictionary/'
    dictYahoo = 'https://tw.dictionary.yahoo.com/dictionary?p='

    req.write('<ul>')
    req.write('<font size=6>')

    for m in re.finditer(r'<b>([^<]*)</b>', meta.load(url)):
        q = m.group(1)
        q = q.replace('\n', '')
        q = q.replace('\r', '')
        q = q.replace(' ', '+')

        s = '<li>%s' %(q)
        s = s + '<a target="_blank" href=%s> [Cambridge] </a>' %(dictCambridge+q)
        s = s + '<a target="_blank" href=%s> [Webster] </a>' %(dictWebster+q)
        s = s + '<a target="_blank" href=%s> [Yahoo] </a>' %(dictYahoo+q)

        req.write(s)

    req.write('</ul>')
