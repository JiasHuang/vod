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
        for m in re.finditer(r'file:(.*?),label:(.*?)', txt):
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

    return ''

