#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import xdef
import xurl
import xsrc
import hashlib

def addEntry(m3u8, part, link):
    print('\n[nbahd][entry]\n')
    print('\tpart: '+part)
    print('\tlink: '+link)
    fd = open(m3u8, 'a')
    fd.write(link+'\n')
    fd.close()
    return

def listPart(m3u8, url):
    txt = xurl.load2(url)
    for m in re.finditer(r'<a href="([^"]*)" target="_blank"><img src=', txt):
        part = m.group(1)
        if re.search('nbahd.net', part):
            for link in xsrc.findLink(part):
                addEntry(m3u8, part, link)
    return

def lookup(m3u8):
    if os.path.exists(m3u8):
        return m3u8
    return None

def listURL(url):
    m3u8 = xdef.workdir+'list_'+hashlib.md5(url).hexdigest()+'.m3u8'
    if lookup(m3u8):
        return m3u8
    listPart(m3u8, url)
    return lookup(m3u8)

def getSource(url):
    m3u8 = listURL(url)
    if m3u8:
        return m3u8
    return ''
