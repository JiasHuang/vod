#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xurl

VALID_URL = r'litv\.tv'

def getSource(url, fmt, ref):
    txt = xurl.load(url)
    m = re.search(r'"assetId":"(.*?)"', txt)
    if m:
        assetId = m.group(1)
        remote = 'https://www.litv.tv/vod/ajax/getUrl'
        local = xurl.genLocal(url, suffix='.json')
        opts = []
        opts.append('-H \'Content-Type: application/json\'')
        opts.append('-d \'{"assetId":"%s","type":"noauth"}\'' %(assetId))
        xurl.load(remote, local, opts)
        m = re.search(r'"fullpath":"(.*?)"', xurl.readLocal(local))
        if m:
          return m.group(1)
    return None

