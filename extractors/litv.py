#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xdef
import xurl

VALID_URL = r'litv\.tv'

def getSource(url):
    txt = xurl.curl(url)
    m = re.search(r'"assetId":"(.*?)"', txt)
    if m:
        assetId = m.group(1)
        remote = 'https://www.litv.tv/vod/ajax/getMainUrlNoAuth'
        local = xdef.workdir+'litv.json'
        opts = []
        opts.append('-H \'Content-Type: application/json\'')
        opts.append('-d \'{"assetId":"%s"}\'' %(assetId))
        xurl.curl(remote, local, opts)
        m = re.search(r'"fullpath":"(.*?)"', xurl.readLocal(local))
        if m:
          return m.group(1)
    return None

