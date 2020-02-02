#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xurl

VALID_URL = r'bilibili\.com'

def getSource(url):
    txt = xurl.curl(url)
    result = []
    m = re.search(r'av(\d+)', url)
    avid = m.group(1) if m else None
    m = re.search(r'cid=(\d+)', txt)
    cid = m.group(1) if m else None
    if avid and cid:
        api_url = 'https://api.bilibili.com/x/player/playurl?avid=%s&cid=%s&otype=json' %(avid, cid)
        for m in re.finditer(r'"url":"([^"]*)"', xurl.curl(api_url)):
            result.append(m.group(1).decode('unicode_escape'))
    local = xurl.genLocal(url, prefix='vod_list_', suffix='.m3u8')
    xurl.saveM3U8(local, result)
    return local

