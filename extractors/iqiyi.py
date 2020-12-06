#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import hashlib
import subprocess

import xurl

VALID_URL = r'iqiyi\.com'

def loadM3U8(url):
    txt = xurl.load(url)
    txt = txt.replace('\/', '/')
    txt = txt.replace('\\n', '\n')
    m = re.search(r'"m3u8":"([^"]*)"', txt)
    if m:
        m3u8 = m.group(1)
        local = xurl.genLocal(url, prefix='vod_list_', suffix='.m3u8')
        xurl.saveLocal(local, m3u8)
        return local
    results = []
    for l in re.finditer(r'"l":"([^"]*)"', txt):
        part = l.group(1)
        if re.search(r'f4v\?', part):
            if part.startswith('http'):
                results.append(part)
            else:
                data_url = 'https://data.video.iqiyi.com/videos' + part
                for v in re.finditer(r'"l":"([^"]*)"', xurl.load(data_url)):
                    results.append(v.group(1))
    if len(results):
        local = xurl.genLocal(url, prefix='vod_list_', suffix='.m3u8')
        xurl.saveM3U8(local, results)
        return local
    return None

def getDashURL(url):
    cmd = 'google-chrome-stable --headless --disable-gpu --enable-logging --v=1 \'%s\'' %(url)
    output = subprocess.check_output(cmd, stderr=subprocess.STDOUT, shell=True)
    m = re.search(r'https://cache.video.iqiyi.com/dash.*', output)
    if m:
        return m.group(0)
    return None

def getSource(url, fmt, ref):
    if re.search(r'/dash\?', url):
        return loadM3U8(url)
    else:
        dashURL = getDashURL(url)
        if dashURL:
            return loadM3U8(dashURL)
    return None
