#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess

import xurl
import xdef

def getSource(url):
    txt = '/tmp/videowoodtv.txt'
    xurl.get(url, txt)
    cmd = 'LANG=zh_TW.UTF-8 js %svideowoodtv.site.js %s' %(xdef.codedir, txt)
    src = subprocess.check_output(cmd, shell=True).rstrip('\n')
    return src

def search(txt):
    m = re.search(r'http://videowood.tv/([^"]*)', txt)
    if m:
        return m.group()
    return

