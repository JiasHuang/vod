#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import xdef
import xurl
import xsrc
import hashlib

def addEntry(m3u, part, link):
    print('\n[nbahd][entry]\n')
    print('\tpart: '+part)
    print('\tlink: '+link)
    fd = open(m3u, 'a')
    fd.write(link+'\n')
    fd.close()
    return

def listPart(m3u, url):
    txt = xurl.load2(url)
    for m in re.finditer(r'<a href="([^"]*)" target="_blank"><img src=', txt):
        part = m.group(1)
        if re.search('nbahd.net', part):
            for link in xsrc.findLink(part):
                addEntry(m3u, part, link)
    return

def lookup(m3u):
    if os.path.exists(m3u):
        return m3u
    return None

def listURL(url):
    m3u = xdef.workdir+'vod_list_'+hashlib.md5(url).hexdigest()+'.m3u'
    if lookup(m3u):
        return m3u
    listPart(m3u, url)
    return lookup(m3u)

def getSource(url):
    m3u = listURL(url)
    if m3u:
        return m3u
    return ''
