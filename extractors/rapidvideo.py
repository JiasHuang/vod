#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import xurl

VALID_URL = r'rapidvideo\.com'

def getSource(url, ref=None):
    txt = xurl.curl(url, ref=ref)
    m = re.search('<source.*? src="([^"]*)"', txt)
    return m.group(1) if m else None

