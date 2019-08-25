#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import json
import hashlib
import subprocess

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

def getDashURL(url):
    cmd = 'google-chrome-stable --headless --disable-gpu --enable-logging --v=1 \'%s\'' %(url)
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    m = re.search(r'https://cache.video.iqiyi.com/dash.*', output)
    if m:
        return m.group(0)
    return None

def getSource(url):
    dashURL = getDashURL(url)
    if dashURL:
        return loadM3U8(dashURL)
    return None
