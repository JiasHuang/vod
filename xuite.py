#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import re
import xurl
import xdef

def parseParameters(url):
    match = re.search(r'(.*?)&ytdl_password=(.*?)$', url)
    if match:
        return match.group(1), match.group(2)
    return url, None

def getSource(url):
    url, key = parseParameters(url)
    mURL = None
    if re.search(r'^http://vlog.xuite.net/play/', url):
        txt = xurl.load(url)
        m = re.search(r'http://m.xuite.net/vlog/([^"]*)', txt)
        if m:
            mURL = m.group(0)

    if mURL == None:
        return ''

    if key:
        txt = xurl.post(mURL, {'pwInput': key})
    else:
        txt = xurl.load(mURL)
    m = re.search(r'data-original="([^"]*)"', txt)
    if m:
        src = m.group(1)
        hd = re.search(r'<button id="page-video-quality" data-hdsize="([^"]*)">', txt)
        if hd:
            src = re.sub('q=360', 'q='+hd.group(1), src)
        print('\n[xuite][src]\n\n\t'+src)
        return src
    return ''

