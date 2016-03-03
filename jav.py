#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import googlevideo, videomega, videowood

def getTxt(url):
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}
    r = requests.get(url, headers=headers)
    return r.text.encode('utf8')

def getIFrame(url):
    txt = getTxt(url)
    frm = re.search(r'<iframe ([^>]*)>', txt).group()
    src = re.search(r'src="([^"]*)"', frm).group(1)
    print '\n[jav][iframe][url]\n\n\t%s' %(url)
    print '\n[jav][iframe][src]\n\n\t%s' %(src)

    if re.search(r'(videowood|videomega|googlevideo|googleusercontent)', src):
        return src

    return getTxt(src)

def getSource(url):

    if url == '':
        print '\n[jav] invalid url'

    elif re.search(r'jav(68|pub)', url):

        if re.search('/movie/', url):
            url = re.search(r'http://([^/]*)/watch/([^"]*)', getTxt(url)).group()
            print '\n[jav][watch]\n\n\t%s' %(url)

        txt = getTxt(url)

        m = re.search(r'<strong>VIP</strong>.*?<a href="([^"]*)', txt)
        if m:
            txt = getTxt(m.group(1))
            ref = googlevideo.search(txt)
            if ref:
                return ref

        m = re.search(r'<strong>Wood</strong>.*?<a href="([^"]*)', txt)
        if m:
            txt = getIFrame(m.group(1))
            ref = videowood.search(txt)
            if ref:
                return ref

        m = re.search(r'<strong>Mega</strong>.*?<a href="([^"]*)', txt)
        if m:
            txt = getIFrame(m.group(1))
            ref = videomega.search(txt)
            if ref:
                return ref

    return ''


