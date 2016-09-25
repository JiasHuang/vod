#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import urllib2
import base64
import xurl, googlevideo, videomega, videowood

def load(url):
    headers={'User-Agent': 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0'}
    r = requests.get(url, headers=headers)
    return r.text.encode('utf8')

def load2(url):
    opener = urllib2.build_opener()
    opener.addheaders = [('User-agent', 'Mozilla/5.0 (X11; Linux i686; rv:10.0) Gecko/20100101 Firefox/33.0')]
    try:
        f = opener.open(url)
        if f.info().get('Content-Encoding') == 'gzip':
            buf = StringIO(f.read())
            return gzip.GzipFile(fileobj=buf).read()
        return f.read()
    except:
        return ''

def getIFrame(url):
    txt = load(url)
    frm = re.search(r'<iframe ([^>]*)>', txt)
    if frm :
        src = re.search(r'src="([^"]*)"', frm.group()).group(1)
        if re.search(r'^//', src):
            src = 'http:'+src
        print '\n[jav][iframe][url]\n\n\t%s' %(url)
        print '\n[jav][iframe][src]\n\n\t%s' %(src)
        return src
    return None

def getSource(url):

    if url == '':
        print '\n[jav] invalid url'

    elif re.search(r'jav(68|pub)', url):

        if re.search('/movie/', url):
            url = re.search(r'http://([^/]*)/watch/([^"]*)', load(url)).group()
            print '\n[jav][watch]\n\n\t%s' %(url)

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
            local = '/tmp/porn2tube_src_'+base64.urlsafe_b64encode(url)
            xurl.wget(src, local)
            txt = open(local, 'r').read()
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


