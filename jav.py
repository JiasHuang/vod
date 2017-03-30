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
    try:
        return int(re.sub("[^0-9]", "", s))
    except:
        return 0

def search(patten, txt):
    m = re.search(patten, txt)
    if m:
        return m.group(1)
    return None

def parseFileSource(txt):
    best_f = None
    best_l = None
    for m in re.finditer(r'{(.*?)}', txt, re.DOTALL|re.MULTILINE):
        t = re.sub('\'', '"', m.group())
        f = search(r'file"?:\s*"([^"]*)', t)
        l = search(r'label"?:\s*"([^"]*)', t)
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

def decodeJSCode_javfinder(url):
    m = re.search(r'<script>(.*?)</script>', load(url), re.DOTALL|re.MULTILINE)
    if m:
        data = m.group(1)
        fake = 'function jwplayer(a){this.setup=function(a){console.log(a);process.exit();};return this;}'
        main = load('https://cdn.javfinder.com/v1/player/main.js?v=4')
        main = re.sub('window.location.pathname', '""', main);
        srcs = jsunpack.executeJSCode(data+fake+main)
        return parseFileSource(srcs)
    return None

def getFrame(url):
    src = xurl.getFrame(url)
    if src and re.search(r'video.php', src):
        return decodeJSCode_javfinder(src) or src
    return src

def searchWatch(url):
    watch = []
    if re.search(r'/watch/', url):
        watch.append(url)
    for m in re.finditer(r'href="([^"]*)"', load(url)):
        if re.search(r'/watch/', m.group(1)):
            if m.group(1) not in watch:
                watch.append(m.group(1))
    return watch

def searchMovieWatch(url):
    watch = searchWatch(url)
    if len(watch) > 0:
        return watch[0]
    return url

def getWatchSource(url):
    if re.search(r'/movie/', url):
        url = searchMovieWatch(url)
    watch = searchWatch(url)
    print('\n[jav][watch][all]\n\n\t'+'\n\t'.join(watch))
    for w in watch:
        print('\n[jav][watch]\n\n\t'+w)
        src = decodeJSCode(w) or getFrame(w)
        if src and not re.search(r'/ads/', src):
            print('\n[jav][src]\n\n\t'+src)
            return src
    return None

def getSource(url):

    if url == '':
        print('\n[jav] invalid url')

    elif re.search(r'porn2tube', url):
        src = getFrame(url)
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
        return getWatchSource(url) or ''

    return ''

