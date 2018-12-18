#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess

import videomega
import videowood
import up2stream
import rapidvideo
import odnoklassniki
import xuite
import goodtv
import litv
import iqiyi
import pianku
import youtubedl
import xurl

def search(pattern, txt, flags=0):
    if not txt:
        return None
    m = re.search(pattern, txt, flags)
    if m:
        return m.group(1)
    return None

def parseParameters(url, key, ref):

    m = re.search(r'&__password__=(.*?)($|&__)', url)
    if m:
        key = m.group(1)

    m = re.search(r'&__referer__=(.*?)($|&__)', url)
    if m:
        ref = m.group(1)

    m = re.search(r'(.*?)&__', url)
    if m:
        url = m.group(1)

    return url, key, ref

def getRedirectLink(url):
    cmd = 'curl -I %s' %(url)
    output = subprocess.check_output(cmd, shell=True)
    m = re.search('Location: (.*?)\n', output)
    if m:
        return m.group(1)
    return url

def removeHashTag(url):
    m = re.search('(.*?)#', url)
    if m:
        return m.group(1)
    return url

def getSource(url, key=None, ref=None):

    src = None
    srcRef = None
    cookies = None

    if url == '':
        src = None

    elif url[0] == '/':
        src = url

    elif url[0:4] != 'http':
        src = None

    else:

        url, key, ref = parseParameters(url, key, ref)

        if re.search('xuite.net', url):
            src = xuite.getSource(url, key)

        elif re.search('goodtv.org', url):
            src = goodtv.getSource(url)

        elif re.search('videomega.tv', url):
            src = videomega.getSource(url)

        elif re.search('up2stream.com', url):
            src = up2stream.getSource(url)

        elif re.search('rapidvideo.com', url):
            src = rapidvideo.getSource(url, ref=ref)
            srcRef = url

        elif re.search('ok.ru', url):
            src = odnoklassniki.getSource(url)

        elif re.search('litv', url):
            src = litv.getSource(url)

        elif re.search('cache.video.iqiyi.com/.*?/dash', url):
            src = iqiyi.getSource(url)

        elif re.search(r'pianku.tv', url):
            src = pianku.getSource(url)

        elif not xurl.getContentType(url).startswith('text'):
            src = url

        else:
            src, cookies = youtubedl.extractURL(url, key=key, ref=ref)
            srcRef = url
            if re.search('dailymotion', src):
                src = getRedirectLink(src)
                src = removeHashTag(src)

    if not src:
        src = getIframeSrc(url)

    if src:
        return src, cookies, srcRef or ref

    raise Exception('GetSourceError')
    return None, None, None

def getSUB(url):
    if re.search(r'youtube.com/watch\?v=', url):
        return youtubedl.extractSUB(url)
    return None

def getIframeSrc(url):
    if url[0:4] != 'http':
        return None
    return search(r'<iframe.*?src="([^"]*)"', xurl.load(url))
