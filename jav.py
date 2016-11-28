#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib2
import base64
import hashlib
import xurl
import googlevideo
import videomega
import videowood
import xdef

def load(url, local=None):
    return xurl.load2(url, local)

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
            local_packed = xdef.workdir+'vod_porn2tube_packed_'+hashlib.md5(url).hexdigest()
            local_unpack = xdef.workdir+'vod_porn2tube_unpack_'+hashlib.md5(url).hexdigest()
            xurl.wget(src, local, '--referer='+url)
            packed = re.search('(eval\(function\(p,a,c,k,e,d\)\{.+\))', xurl.readLocal(local))
            if packed:
                fd = open(local_packed, "w")
                fd.write(packed.group())
                fd.close()
                os.system('js-beautify %s > %s' %(local_packed, local_unpack))
                txt = xurl.readLocal(local_unpack)
                print('\n[unpack]\n\n\t%s' %(txt))
        else:
            txt = load(url)

        v = v1 = v2 = v3 = None
        for m in re.finditer(r'file:([^"]*)"([^"]*)"([^}]*)', txt):
            if re.search(r'atob', m.group(1)):
                v = base64.b64decode(m.group(2))
            else:
                v = m.group(2)
            if not re.search(r'^http', v):
                continue
            if re.search(r'1080p', m.group(3), re.IGNORECASE):
                v1 = v
            elif re.search(r'720p', m.group(3), re.IGNORECASE):
                v2 = v
            elif re.search(r'480p', m.group(3), re.IGNORECASE):
                v3 = v
        return v1 or v2 or v3 or v or ''

    return getIFrame(url) or ''


