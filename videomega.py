#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import jsunpack

def getSource(url):
    txt = jsunpack.unpackURL(url) or ''
    m = re.search(r'http://([^"]+)', txt)
    if m:
        m.group()
    return None

def search(txt):
    m = re.search(r'http://videomega.tv/([^"]*)', txt)
    if m:
        return m.group()
    return

