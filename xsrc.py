#!/usr/bin/env python
# -*- coding: utf-8 -*-

import extractors
import xarg

def getSource(url, ref=None):

    src = None
    cookies = None

    if url == '':
        src = None

    elif url[0] == '/':
        src = url

    elif url[0:4] != 'http':
        src = None

    else:
        src, cookies, ref = extractors.getSource(url, xarg.ytdlfmt, ref)

    if src:
        return src, cookies, ref

    raise Exception('GetSourceError')
    return None, None, None

def getSub(url):
    return extractors.getSub(url, xarg.subtitle)

