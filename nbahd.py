#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import xdef
import xurl
import xsrc
import base64

def addEntry(title, res, src):
    print('\n[nbahd][src][%s]\n\n\t%s' %(res, src))
    fd = open('%s_%s.m3u' %(title, res), 'a')
    fd.write(src+'\n')
    fd.close()
    return

def listPart(title, url):
    txt = xurl.load2(url)
    for m in re.finditer(r'<a href="([^"]*)" target="_blank"><img src=', txt):
        part = m.group(1)
        if re.search('nbahd.net', part):
            print('\n[nbahd][part]\n\n\t%s' %(part))
            for l in xsrc.findLink(part):
                addEntry(title, 'auto', l)
    return

def lookup(title):
    for res in ['auto', '720', '480', '360']:
        if os.path.exists('%s_%s.m3u' %(title, res)):
            print('\n[nbahd][m3u]\n\n\t%s_%s.m3u' %(title, res))
            return '%s_%s.m3u' %(title, res)
    return None

def listURL(url):
    title = base64.urlsafe_b64encode(url)
    ret = lookup(title)
    if ret:
        return ret
    listPart(title, url)
    return lookup(title)

def getSource(url):
    os.chdir(xdef.workdir)
    m3u = listURL(url)
    if m3u:
        return '%s%s' %(xdef.workdir, m3u)
    return ''
