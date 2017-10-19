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

def search(pattern, txt, flags=0):
    if not txt:
        return None
    m = re.search(pattern, txt, flags)
    if m:
        return m.group(1)
    return None

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

    src, cookies = youtubedl.extractURL(url, key)
    if src:
        return src, cookies

    raise Exception('GetSourceError')
    return None, None

def getSUB(url):
    if re.search(r'youtube.com/watch\?v=', url):
        return youtubedl.extractSUB(url)
    return None

def getIframeSrc(url):
    if url[0:4] != 'http':
        return None
    return search(r'<iframe.*?src="([^"]*)"', xurl.load(url))
