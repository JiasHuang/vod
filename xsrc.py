#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import subprocess

import videomega
import videowood
import up2stream
import rapidvideo
import odnoklassniki
import goodtv
import litv
import iqiyi
import pianku
import pangzitv
import bilibili
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
    cmd = 'curl -I \"%s\"' %(url)
    output = subprocess.check_output(cmd, shell=True)
    cookies = []
    cookies_str = None
    for m in re.finditer('Set-Cookie: (.*?)(\n|\r)', output):
        cookies.append(m.group(1))
    if len(cookies) > 0:
        cookies_str = '; '.join(cookies)
    m = re.search('Location: (.*?)\n', output)
    if m:
        return m.group(1), cookies_str
    return url, None

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

        if re.search('goodtv.org', url):
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

        elif re.search('iqiyi\.com', url):
            src = iqiyi.getSource(url)

        elif re.search(r'pianku.tv', url):
            src = pianku.getSource(url)

        elif re.search(r'pangzitv', url):
            src = pangzitv.getSource(url)

        elif re.search(r'bilibili', url):
            src = bilibili.getSource(url)

        elif not xurl.getContentType(url).startswith('text'):
            src = url

        else:
            src, cookies = youtubedl.extractURL(url, key=key, ref=ref)
            srcRef = url
            if re.search('dailymotion', src):
                src, extra_cookies = getRedirectLink(src)
                src = removeHashTag(src)
                if extra_cookies:
                    cookies = extra_cookies

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
