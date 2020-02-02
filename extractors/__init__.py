#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import glob

import youtubedl
import xurl

mods = []

files = glob.glob(os.path.join(os.path.dirname(__file__), "*.py"))
for f in files:
    if os.path.isfile(f) and not f.endswith('__.py'):
        name = os.path.basename(f)[:-3]
        __import__('%s.%s' %(__package__, name))
        mod = globals()[name]
        if hasattr(mod, 'VALID_URL') and hasattr(mod, 'getSource'):
            mods.append(mod)

def getSource(url, ref):
    for m in mods:
        if re.search(m.VALID_URL, url):
            ret = m.getSource(url)
            if type(ret) is xurl.xurlObj:
                return ret.url, ret.cookies, ret.ref
            return ret, None, None

    # apply youtubedl if no module matched
    src, cookies = youtubedl.extractURL(url, ref=ref)
    ref = url

    if not src:
        src = getIframeSrc(url)

    return src, cookies, ref

def getSub(url):
    return youtubedl.extractSUB(url)

def getIframeSrc(url):
    if url[0:4] != 'http':
        return None
    return search(r'<iframe.*?src="([^"]*)"', xurl.load(url))
