#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import youtubedl
import xurl

VALID_URL = r'ok\.ru'

def getSource(url, fmt, ref):
    local_json = youtubedl.extractURL(url, dontParseJson=True)
    local_m3u8 = re.sub('.json', '.m3u8', local_json)
    m = re.search(r'"manifest_url": "([^"]*)"', xurl.readLocal(local_json))
    if m:
        manifest_url = m.group(1)
        xurl.curl(manifest_url, local=local_m3u8)
        return local_m3u8
    return None

