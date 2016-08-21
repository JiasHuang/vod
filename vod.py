#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, sys, time
import xdef, xurl, xplay
import videomega, videowood, openload, up2stream
import xuite, jav, nbahd, letv, goodtv
import youtubedl

from optparse import OptionParser

def processURL1(url): 

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

    if re.search('openload.co', url):
        src = openload.getSource(url)
        xplay.playURL(src, url)
        return 0

    if re.search('up2stream.com', url):
        src = up2stream.getSource(url)
        xplay.playURL(src, url)
        return 0

    if re.search('nbahd.net', url):
        src = nbahd.getSource(url)
        xplay.playURL(src, '')
        return 0

    if re.search('letv.com', url):
        src = letv.getSource(url)
        xplay.playURL(src, '')
        return 0

    if youtubedl.checkURL(url):
        xplay.playURL(url, url)
        return 0

    return -1

def processURL2(url):

    print '\n[vod] Search context'
 
    txt = xurl.load(url)

    m = re.search(r'http://(videomega|videowood).tv/[^"]*', txt)
    if m:
        return processURL1(m.group())

    m = re.search(r'https:/openload.co/[^"]*', txt)
    if m:
        return processURL1(m.group())

    m = re.search(r'www.dailymotion.com/[^"]*', txt)
    if m:
        return processURL1(m.group())

    m = re.search(r'https://.*?.googleusercontent.com/([^"]*)', txt)
    if m:
        return processURL1(m.group())

    m = re.search(r'https://redirector.googlevideo.com/([^"]*)', txt)
    if m:
        return processURL1(m.group())

    print '\n[vod] Not Found'
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

    if re.search(r'jav(68|pub|cuteonline)', url):
        url = jav.getSource(url)
        print '\n[vod][jav]\n\n\t%s\n' %(url)

    if url == '':
        return

    if processURL1(url) != -1:
        return

    if processURL2(url) != -1:
        return

    src = youtubedl.extractURL(url)
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

    if len(args) == 0:
        xplay.runIdle()
        return

    if len(args) >= 1:
        url = args[0]
        m = re.search(r'view.py?v=(.*)', url)
        if m:
            url = m.group(1)

    if len(args) >= 2:
        ref = args[1]

    playURL(url, ref)


if __name__ == '__main__':
    main()
