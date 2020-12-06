#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xurl

VALID_URL = r'rapidvideo\.com'

def getSource(url, fmt, ref):
    txt = xurl.load(url)
    m = re.search('<source.*? src="([^"]*)"', txt)
    return m.group(1) if m else None

