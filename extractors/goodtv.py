#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xurl

VALID_URL = r'goodtv\.org'

def getSource(url, fmt, ref):
    txt = xurl.load(url)
    for m in re.finditer(r'source src="([^"]*)"', txt):
        src = m.group(1)
        if not src.endswith('.m4a.m3u8'):
            print('[src] %s' %(src))
            return src
    return url

