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

def dl(src, target, bitrate):
    src = re.sub('.m3u8', '_%s.mp4.m3u8' %(bitrate), src)
    prefix, m3u8 = xurl.parse(src)
    txt = xurl.load(src)
    for m in re.finditer(r'(.*?).ts', txt):
        link, local = prefix+m.group(), xdef.workdir+m.group()
        xurl.wget(link, local)
    for m in re.finditer(r'(.*?).ts', txt):
        local = xdef.workdir+m.group()
        if os.path.exists(local):
            os.system('cat %s >> %s' %(local, target))
    return

def download():
    mmdd = datetime.datetime.now().strftime("%m%d")
    target = xdef.dldir+'studio_classroom_'+mmdd+'.ts'
    url = 'http://w2.goodtv.org/studio_classroom/'
    src = getSource(url)
    for bitrate in ['1200k', '500k', '350k']:
        if not os.path.exists(target):
            dl(src, target, bitrate)
    return

