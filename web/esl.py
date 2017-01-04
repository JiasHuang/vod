#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import meta

def loadWord(req, url):
    return parseWord(req, meta.load(url))

def parseWord(req, txt):

    dictCambridge = 'http://dictionary.cambridge.org/dictionary/english-chinese-traditional/'
    dictWebster = 'http://www.merriam-webster.com/dictionary/'
    dictYahoo = 'https://tw.dictionary.yahoo.com/dictionary?p='

    req.write('<br><br><hr><ul>')
    req.write('<font size=5>')

    for m in re.finditer(r'<b>([^<]*)</b>', txt):
        q = m.group(1)
        q = q.replace('\n', '')
        q = q.replace('\r', '')
        q = q.replace(' ', '+')

        s = '<li>%s' %(q)
        s = s + '<a target="_cambridge" href=%s>[Cambridge]</a>' %(dictCambridge+q)
        s = s + '<a target="_webster" href=%s>[Webster]</a>' %(dictWebster+q)
        s = s + '<a target="_yahoo" href=%s>[Yahoo]</a>' %(dictYahoo+q)
        s = s + '\n'

        req.write(s)

    req.write('</ul><hr><br><br>')
