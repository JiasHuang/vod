#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import xurl

def getSource(url):
    txt = xurl.load(url)
    m = re.search(r'source src="([^"]*)"', txt)
    if m:
        return m.group()
    return url

