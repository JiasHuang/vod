#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import youtubedl
import xurl

def getSource(url):
    txt = xurl.load2(url)
    result = []
    for m in re.finditer(r'"url":"([^"]*)"', txt):
        result.append(m.group(1))
    return youtubedl.genM3U(url, result)

