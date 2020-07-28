#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

import xurl

VALID_URL = r'bilibili\.com'

def getSource(url, fmt, ref):
    txt = xurl.curl(url)
    result = []
    m = re.search(r'video/(\w+)', url)
    bvid = m.group(1) if m else None
    m = re.search(r'\?p=(\d+)', url)
    p = m.group(1) if m else None
    if p:
        m = re.search(r'"cid":(\d+),"page":' + re.escape(p) + re.escape(','), txt)
    else:
        m = re.search(r'cid=(\d+)' , txt)
    cid = m.group(1) if m else None
    if bvid and cid:
        api_url = 'https://api.bilibili.com/x/player/playurl?bvid=%s&cid=%s&otype=json' %(bvid, cid)
        api_txt = xurl.curl(api_url)
        data = json.loads(api_txt)
        for d in data['data']['durl']:
            result.append(d['url'])
    local = xurl.genLocal(url, prefix='vod_list_', suffix='.m3u8')
    xurl.saveM3U8(local, result)
    return local

