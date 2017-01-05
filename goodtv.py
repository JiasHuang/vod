#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import datetime

import xurl
import xdef

def getSource(url):
    txt = xurl.load(url)
    m = re.search(r'source src="([^"]*)"', txt)
    if m:
        return m.group(1)
    return url

def download(url=None):
    mmdd = datetime.datetime.now().strftime("%m%d")
    target = xdef.dldir+'studio_classroom_'+mmdd+'.ts'
    if not url:
        url = 'http://w2.goodtv.org/studio_classroom/'
    if not os.path.exists(target):
        src = re.sub('.m3u8', '_1200k.mp4.m3u8', getSource(url))
        prefix, m3u8 = xurl.parse(src)
        xurl.wget(src, m3u8)
        for m in re.finditer(r'(.*?).ts', xurl.readLocal(m3u8)):
            xurl.wget(prefix+m.group(), m.group(), '--referer='+url)
            os.system('cat %s >> %s' %(m.group(), target))
    return

