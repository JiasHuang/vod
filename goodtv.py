#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import datetime

import xurl
import xdef

def getSource(url):
    txt = xurl.load(url)
    for m in re.finditer(r'source src="([^"]*)"', txt):
        src = m.group(1)
        if not src.endswith('.m4a.m3u8'):
            print('[src] %s' %(src))
            return src
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
    if datetime.datetime.today().isoweekday() == 7:
        return
    yyyymmdd = datetime.datetime.now().strftime("%Y%m%d")
    target = xdef.dldir+'studio_classroom_'+yyyymmdd+'.ts'
    url = 'http://w2.goodtv.org/studio_classroom/'
    src = getSource(url)
    for bitrate in ['1200k', '500k', '350k']:
        if not os.path.exists(target):
            dl(src, target, bitrate)
    return

