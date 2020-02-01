#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import jsunpack
import xurl

def getSource(url):
    txt = jsunpack.unpackURL(url) or ''
    m = re.search(r'MDCore.wurl="([^"]+)"', txt)
    return xurl.urljoin(url, m.group(1)) if m else None

