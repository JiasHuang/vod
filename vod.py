#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib

import xdef
import xurl
import xplay
import videomega
import videowood
import up2stream
import xuite
import jav
import nbahd
import goodtv
import youtubedl

from optparse import OptionParser

def processURL1(url): 

    if re.search('google(video|usercontent).com', url):
        xplay.playURL(url, url)
        return 0

    if re.search('xuite.net', url):
        src = xuite.getSource(url)
        xplay.playURL(src, url)
        return 0

    if re.search('goodtv.org', url):
        src = goodtv.getSource(url)
        xplay.playURL(src, url)
        return 0

    if re.search('videomega.tv', url):
        src = videomega.getSource(url)
        xplay.playURL(src, url)
        return 0

    if re.search('videowood.tv', url):
        src = videowood.getSource(url)
        xplay.playURL(src, url)
        return 0

    if re.search('up2stream.com', url):
        src = up2stream.getSource(url)
        xplay.playURL(src, url)
        return 0

    if re.search('nba([a-z]*).(com|net)', url):
        src = nbahd.getSource(url)
        xplay.playURL(src, src)
        return 0

    if re.search(r'porn2tube', url):
        src = jav.getSource(url)
        xplay.playURL(src, url)
        return 0

    if youtubedl.checkURL(url):
        xplay.playURL(url, url)
        return 0

    if xurl.getContentType(url) != 'text/html':
        xplay.playURL(url, url)
        return 0

    return -1

def processURL2(url):

    print('\n[vod] Search context')

    txt = xurl.load(url)

    m = re.search(r'"http(s|)://(www.|)(redirector.googlevideo|dailymotion|videomega|videowood|youtube|openload)(.com|.tv|.co)([^"]*)', txt)
    if m:
        return processURL1(m.group())

    m = re.search(r'http(s|)://([a-zA-Z-0-9]*).googlevideo.com/([^"]*)', txt)
    if m:
        return processURL1(m.group())

    print('\n[vod] Not Found')
    return -1

def playURL(url, ref):

    if ref:
        xplay.playURL(url, ref)
        return

    url = url.strip()

    m = re.search(r'view.py\?url=(.*)', url)
    if m:
        url = m.group(1)

    if url[0] == '/':
        xplay.playURL(url, '')
        return

    if url[0:4] != 'http':
        return

    if url == '':
        return

    if url.lower().endswith(('.mkv', '.mp4', '.avi', '.flv', '.f4v', '.m3u', '.m3u8', '.mp3', 'm4a')):
        xplay.playURL(url, '')
        return

    if processURL1(url) != -1:
        return

    if processURL2(url) != -1:
        return

    src = youtubedl.extractURL(url) or ''
    xplay.playURL(src, url)
    return


def main():

    url = None
    ref = None

    os.chdir(xdef.workdir)

    parser = OptionParser()
    parser.add_option("-p", "--player", dest="player")
    (options, args) = parser.parse_args()

    if options.player:
        xdef.player = options.player

    if len(args) >= 1:
        url = args[0]
        m = re.search(r'view.py\?(v|url)=(.*)', url)
        if m:
            url = urllib.unquote(m.group(2))

    if len(args) >= 2:
        ref = args[1]

    playURL(url, ref)


if __name__ == '__main__':
    main()
