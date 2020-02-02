#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import jsunpack

VALID_URL = r'videomega\.tv'

def getSource(url):
    txt = jsunpack.unpackURL(url) or ''
    m = re.search(r'http://([^"]+)', txt)
    return m.group() if m else None

