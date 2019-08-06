#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xurl

def getSource(url):
    txt = xurl.curl(url)
    m = re.search(r'url: \'(.*?)\'', txt)
    if m:
        return m.group(1)
    return None

