#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import googlevideo
import videowood
import videomega

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
    return getTxt(src)

def getSource(url):

    if url == '':
        print '\n[jav] invalid url'

    elif re.search(r'jav(68|pub)', url):

        if re.search('/movie/', url):
            url = re.search(r'http://([^/]*)/watch/([^"]*)', getTxt(url)).group()
            print '\n[jav][watch]\n\n\t%s' %(url)

        txt = getTxt(url)

        m = re.search(r'Server Free:.*?<a href="([^"]*)', txt)
        if m:
            txt = getTxt(m.group(1))
            return googlevideo.getSource(txt)

        '''
        m = re.search(r'<strong>Open</strong>.*?<a href="([^"]*)', txt)
        if m:
            txt = getIFrame(m.group(1))
            return googlevideo.getSource(txt)
        '''

        m = re.search(r'<strong>Wood</strong>.*?<a href="([^"]*)', txt)
        if m:
            txt = getIFrame(m.group(1))
            return videowood.getSource(txt)

        m = re.search(r'<strong>Mega</strong>.*?<a href="([^"]*)', txt)
        if m:
            txt = getIFrame(m.group(1))
            return videomega.getSource(txt)

    elif re.search('javcuteonline', url):
        txt = getTxt(url)
        return videomega.getSource(txt)

    return ''


