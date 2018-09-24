#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json

import xdef
import xurl

def getSource(url):
    txt = xurl.load2(url)
    m = re.search(r'"assetId":"(.*?)"', txt)
    if m:
        assetId = m.group(1)
        remote = 'https://www.litv.tv/vod/ajax/getMainUrlNoAuth'
        local = xdef.workdir+'litv.json'
        options = '--header=\'Content-Type:application/json\' --post-data \'{"assetId":"%s"}\'' %(assetId)
        xurl.wget(remote, local, options)
        m = re.search(r'"fullpath":"(.*?)"', xurl.readLocal(local))
        if m:
          return m.group(1)
    return None

