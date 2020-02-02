#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys

path = os.path.realpath(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(path))

import extractors

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
        src, cookies, ref = extractors.getSource(url, ref)

    if src:
        return src, cookies, ref

    raise Exception('GetSourceError')
    return None, None, None

def getSub(url):
    return extractors.getSub(url)

