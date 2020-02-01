#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import youtubedl
import xurl

def getSource(url):
    txt = xurl.curl(url)
    result = []
    m = re.search(r'av(\d+)', url)
    avid = m.group(1) if m else None
    m = re.search(r'"cid":(\d+)', txt)
    cid = m.group(1) if m else None
    if avid and cid:
        api_url = 'https://api.bilibili.com/x/player/playurl?cid=%s&avid=%s&otype=json' %(cid, avid)
        for m in re.finditer(r'"url":"([^"]*)"', xurl.curl(api_url)):
            result.append(m.group(1).decode('unicode_escape'))
    return youtubedl.genM3U(url, result)

