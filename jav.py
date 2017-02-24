#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import base64
import hashlib

import xurl
import xdef
import jsunpack
import youtubedl

def load(url, local=None, options=None):
    return xurl.load2(url, local, options)

def str2int(s):
    return int(re.sub("[^0-9]", "", s))

def search(patten, txt):
    m = re.search(patten, txt)
    if m:
        return m.group(1)
    return None

def parseFileSource(txt):
    best_f = None
    best_l = None
    for m in re.finditer(r'{(.*?)}', txt):
        f = search(r'"file":"([^"]*)"', m.group())
        l = search(r'"label":"([^"]*)"', m.group())
        if f:
            encoded = re.search(r'window.atob(([^)]*))', f)
            if encoded:
                f = base64.b64decode(encoded.group(1))
            if not best_l:
                best_f = f
                best_l = l
            elif l and best_l and str2int(l) > str2int(best_l):
                best_f = f
                best_l = l
    return best_f

def decodeJSCode(url):
    for m in re.finditer(r'<script type="text/javascript">(.*?)</script>', load(url), re.DOTALL|re.MULTILINE):
        if re.search(r'document.writeln', m.group(1)):
            code = re.sub('document.writeln', 'console.log', m.group(1))
            src = re.search(r'src="([^"]*)"', jsunpack.executeJSCode(code))
            if src:
                return parseFileSource(jsunpack.unpackURL(src.group(1)))
    return None

def getSource(url):

    if url == '':
        print('\n[jav] invalid url')

    elif re.search(r'porn2tube', url):
        src = xurl.getFrame(url)
        if src:
            if youtubedl.checkURL(src):
                return src
            local = xdef.workdir+'vod_porn2tube_'+hashlib.md5(url).hexdigest()
            load(src, local, '--referer='+url)
            txt = jsunpack.unpackFILE(local) or ''
        else:
            txt = load(url)

        v = v1 = v2 = v3 = None
        for m in re.finditer(r'file:(.*?),label:([a-zA-Z0-9\']*)', txt):
            link, label, = m.group(1), m.group(2)
            link = re.sub('["\']', '', link)
            m = re.search(r'window.atob(([^)]*))', link)
            if m:
                v = base64.b64decode(m.group(1))
            else:
                v = link
            if not re.search(r'^http', v):
                continue
            if re.search(r'1080p', label, re.IGNORECASE):
                v1 = v
            elif re.search(r'720p', label, re.IGNORECASE):
                v2 = v
            elif re.search(r'480p', label, re.IGNORECASE):
                v3 = v
        return v1 or v2 or v3 or v or ''

    elif re.search(r'javpub', url):
        for m in re.finditer(r'href="([^"]*)"', load(url)):
            if re.search(r'/watch/', m.group(1)):
                return decodeJSCode(m.group(1)) or ''

    return ''

