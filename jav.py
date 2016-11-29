#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib2
import base64
import hashlib
import xurl
import xdef
import googlevideo
import videomega
import videowood
import jsunpack

def load(url, local=None, options=None):
    return xurl.load2(url, local, options)

def getIFrame(url):
    txt = load(url)
    frm = re.search(r'<iframe ([^>]*)>', txt)
    if frm :
        src = re.search(r'src="([^"]*)"', frm.group()).group(1)
        if re.search(r'^//', src):
            src = 'http:'+src
        print('\n[jav][iframe][url]\n\n\t%s' %(url))
        print('\n[jav][iframe][src]\n\n\t%s' %(src))
        return src
    return None

def getSource(url):

    if url == '':
        print('\n[jav] invalid url')

    elif re.search(r'jav(68|pub)', url):

        if re.search('/movie/', url):
            url = re.search(r'http://([^/]*)/watch/([^"]*)', load(url)).group()
            print('\n[jav][watch]\n\n\t%s' %(url))

        txt = load(url)

        m = re.search(r'<strong>VIP</strong>.*?<a href="([^"]*)', txt)
        if m:
            txt = load(m.group(1))
            ref = googlevideo.search(txt)
            if ref:
                return ref

        m = re.search(r'<strong>Wood</strong>.*?<a href="([^"]*)', txt)
        if m:
            src = getIFrame(m.group(1))
            if src:
                ref = videowood.search(load(src))
                if ref:
                    return videowood.getSource(ref)

        m = re.search(r'<strong>Mega</strong>.*?<a href="([^"]*)', txt)
        if m:
            src = getIFrame(m.group(1))
            if src:
                ref = videomega.search(load(src))
                if ref:
                    return videomega.getSource(ref)

    elif re.search(r'porn2tube', url):
        src = getIFrame(url)
        if src:
            local = xdef.workdir+'vod_porn2tube_'+hashlib.md5(url).hexdigest()
            load(src, local, '--referer='+url)
            txt = jsunpack.unpackFILE(local) or ''
        else:
            txt = load(url)

        v = v1 = v2 = v3 = None
        for m in re.finditer(r'{file:([^,]*),label:([^,]*),type:([^,]*)}', txt):
            f, label, t = m.group(1), m.group(2), m.group(3)
            f = re.sub('["\']', '', f)
            m = re.search(r'window.atob(([^)]*))', f)
            if m:
                v = base64.b64decode(m.group(1))
            else:
                v = f
            if not re.search(r'^http', v):
                continue
            if re.search(r'1080p', label, re.IGNORECASE):
                v1 = v
            elif re.search(r'720p', label, re.IGNORECASE):
                v2 = v
            elif re.search(r'480p', label, re.IGNORECASE):
                v3 = v
        return v1 or v2 or v3 or v or ''

    return getIFrame(url) or ''


