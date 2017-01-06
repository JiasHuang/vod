#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import random

from optparse import OptionParser
from mod_python import util

import page
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


def genDB():
    return

def outDB(out, key=None):

    links = []
    db = os.path.dirname(os.path.realpath(__file__)) + '/db/'

    for f in os.listdir(db):
        fd = open(db+f, 'r')
        lines = fd.readlines()
        if key:
            for l in lines:
                if re.search(key, l):
                    links.append(l)
        else:
            rand = random.randint(1, len(lines))
            link = lines[rand-1]
            links.append(link)
        fd.close()

    if len(links):
        for link in links:
            print(link)
            page.listURL(out, link)

    return

def index(req):
    req.content_type = 'text/html; charset=utf-8'
    arg  = util.FieldStorage(req)
    k    = arg.get('k', None)
    outDB(req, k)
    return

def main():

    parser = OptionParser()
    parser.add_option("-g", help='gen', dest="gen", action="store_true", default=False)
    parser.add_option("-o", help='out', dest="out")
    parser.add_option("-k", help='key', dest="key")

    options, args = parser.parse_args()

    out = options.out or 'output.html'

    if options.gen == True:
        genDB()
    else:
        fd = open(out, "w")
        outDB(options.out, options.key)
        fd.close()

    return

if __name__ == '__main__':
    main()
