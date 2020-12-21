#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xurl

VALID_URL = r'tiktokvideodown\.com'

def getSource(url, fmt, ref):
    if re.search(r'vod-play-id', url):
        try:
            txt = xurl.load(url)
            m = re.search(r'"url":"([^"]*)"', txt)
            url_m3u8 = m.group(1).replace('\\', '')
            txt_m3u8 = xurl.load(url_m3u8)
            m = re.search(r'(.*?\.m3u8)\s*', txt_m3u8)
            if m:
                return xurl.urljoin(url_m3u8, m.group(1))
            else:
                return url_m3u8
        except:
            print('Exception')
    return None

