#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import urllib2
import xdef

def load(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    return opener.open(url).read()

def listSource(txt):
    match = re.finditer(r'<source ([^>]*)>', txt)
    if match:
        for m in match:
            src = re.search(r'src="([^"]*)"', m.group(1)).group(1) 
            res = re.search(r'res="([^"]*)"', m.group(1)).group(1) 
            res = re.sub('p', '', res)
            print '\n[nbahd][src]\n\n\t%s (%s)' %(src, res)
            fd = open('temp_%s.m3u' %(res), 'a')
            fd.write(src+'\n')
            fd.close()
        return 0
    return -1

def listPart(url):
    txt1 = load(url)
    m = re.search('player.php?([^"]*)', txt1)
    if m:
        txt2 = load('http://nbahd.com/'+m.group())
        listSource(txt2)
    else:
        listSource(txt1)

def listURL(url):
    txt = load(url)
    match = re.finditer(r'<a href="([^"]*)" target="_blank"><img src=', txt)
    for m in match:
        print '\n[nbahd][part]\n\n\t%s' %(m.group(1))
        listPart(m.group(1))
    title = url
    title = re.sub('http://', '', title)
    title = re.sub('/', '_', title)
    title = re.sub('\.', '_', title)
    for res in ['720', '480', '360']:
        if os.path.exists('temp_%s.m3u' %(res)):
            os.system('mv temp_%s.m3u %s_%s.m3u' %(res, title, res))
            print '\n[nbahd][m3u]\n\n\t%s_%s.m3u' %(title, res)
            return '%s_%s.m3u' %(title, res)

    return None

def getSource(url):
    os.chdir(xdef.workdir)
    m3u = listURL(url)
    if m3u:
        return '%s%s' %(xdef.workdir, m3u)
    return ''
