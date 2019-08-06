#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import hashlib

import xdef
import xurl

def loadM3U8(url):
    txt = xurl.curl(url)
    m = re.search(r'"m3u8":"([^"]*)"', txt)
    if m:
        m3u8 = m.group(1)
        m3u8 = m3u8.replace('\/', '/')
        m3u8 = m3u8.replace('\\n', '\n')
        local = xdef.workdir+'vod_list_'+hashlib.md5(url).hexdigest()+'.m3u8'
        xurl.saveLocal(local, m3u8)
        return local
    return None
