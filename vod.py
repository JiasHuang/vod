#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, re, sys, time
import xdef, xurl, xplay
import videowood, openload, xuite, jav, nbahd
import youtubedl

def getSource(url): 
    if re.search(r'jav(68|pub|cuteonline)', url):
        return jav.getSource(url)
    return url

def processURL1(url): 

    if re.search(r'jav(68|pub|cuteonline)', url):
        src = jav.getSource(url)
        xplay.playURL(src, src)
        return 0

    if re.search('http://m.xuite.net/vlog/', url):
        src = xuite.getSource(url)
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

    if re.search('nbahd.com', url):
        src = nbahd.getSource(url)
        xplay.playURL(src, '')
        return 0

    if re.search(r'(youtube|videomega|dailymotion|xuite|facebook|google)', url):
        xplay.playURL(url, url)
        return 0

    return -1

def processURL2(url):

    print '\n[vod] Search context'
 
    txt = xurl.load(url)

    with re.search(r'http://videomega.tv/[^"]*', txt) as m:
        return processURL1(m.group())

    with re.search(r'www.dailymotion.com/[^"]*', txt) as m:
        return processURL1(m.group())

    with re.search(r'https://.*?.googleusercontent.com/([^"]*)', txt) as m:
        return processURL1(m.group())

    with re.search(r'https://redirector.googlevideo.com/([^"]*)', txt) as m:
        return processURL1(m.group())

    print '\n[vod] Not Found'
    return -1

def playURL(url, ref):

    if ref:
        xplay.playURL(url, ref)
        return

    if url[0] == '/':
        xplay.playURL(url, '')
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

    if len(sys.argv) == 1:
        xplay.runIdle()
        return

    if len(sys.argv) >= 2:
        url = sys.argv[1]

    if len(sys.argv) >= 3:
        ref = sys.argv[2]

    playURL(url, ref)


if __name__ == '__main__':
    main()
