#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re

import videomega
import videowood
import up2stream
import xuite
import goodtv
import youtubedl
import xurl

def parseParameters(url):
    m = re.search(r'(.*?)&ytdl_password=(.*?)$', url)
    if m:
        return m.group(1), m.group(2)
    return url, None

def getSource(url, key=None):

    if url == '':
        return None, None

    if url[0] == '/':
        return url, None

    if url[0:4] != 'http':
        return None, None

    url, key = parseParameters(url)

    if re.search('xuite.net', url):
        return xuite.getSource(url, key), None

    if re.search('goodtv.org', url):
        return goodtv.getSource(url), None

    if re.search('videomega.tv', url):
        return videomega.getSource(url), None

    if re.search('videowood.tv', url):
        return videowood.getSource(url), None

    if re.search('up2stream.com', url):
        return up2stream.getSource(url), None

    if xurl.getContentType(url) != 'text/html':
        return url, None

    return youtubedl.extractURL(url, key)

def getSUB(url):
    if re.search(r'youtube.com/watch\?v=', url):
        return youtubedl.extractSUB(url)
    return None