#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import xurl

def getSource(url):
    txt = xurl.load(url)
    m = re.search(r'/hls-vod/sc/([a-zA-Z0-9_]+).m3u8', txt)
    if m:
        return 'http://scvod1.goodtv.org'+m.group()
    return ''

