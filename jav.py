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
        f = search(r'"file":"([^"]*)"', m.group()) or search(r'file:([^,]*)', m.group())
        l = search(r'"label":"([^"]*)"', m.group()) or search(r'label:([0-9]*)', m.group())
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

def searchFrame(url):
    txt = load(url)
    watch = []
    for m in re.finditer(r'href="([^"]*)"', txt):
        if re.search(r'/watch/', m.group(1)):
            if m.group(1) not in watch:
                watch.append(m.group(1))
    for w in watch:
        src = decodeJSCode(w) or xurl.getFrame(w)
        if src and not re.search(r'/ads/', src):
            return src
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
        return parseFileSource(txt)

    elif re.search(r'javpub', url):
        if re.search(r'/movie/', url):
            for m in re.finditer(r'href="([^"]*)"', load(url)):
                if re.search(r'/watch/', m.group(1)):
                    url = m.group(1)
                    break;
        return decodeJSCode(url) or xurl.getFrame(url) or searchFrame(url) or ''

    return ''

