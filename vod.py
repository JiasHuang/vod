#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib
import sys
import traceback

import xarg
import xdef
import xplay
import xsrc

from optparse import OptionParser

def main():

    url = None
    ref = None

    os.chdir(xdef.workdir)

    parser = OptionParser()
    parser.add_option("-p", "--player", dest="player")
    parser.add_option("-f", "--format", dest="format")
    parser.add_option("--autosub", dest="autosub")
    parser.add_option("--pagelist", dest="pagelist")
    parser.add_option("--playbackMode", dest="playbackMode")
    parser.add_option("--buffering", dest="buffering", action='store_true')
    parser.add_option("--dl-threads", dest="dl_threads")
    (options, args) = parser.parse_args()

    if options.player:
        xarg.player = options.player

    if options.format:
        xarg.ytdlfmt = options.format

    if options.autosub:
        xarg.autosub = options.autosub

    if options.pagelist:
        xarg.pagelist = options.pagelist

    if options.playbackMode:
        xarg.playbackMode = options.playbackMode

    if options.buffering:
        xarg.buffering = True

    if options.dl_threads:
        xarg.dl_threads = options.dl_threads

    if len(args) >= 1:
        url = args[0].strip()
        m = re.search(r'view.py\?(v|url)=(.*)', url)
        if m:
            url = urllib.unquote(m.group(2))

    if len(args) >= 2:
        ref = args[1].strip()

    # UGLY CODE
    if re.search(r'pangzitv', url):
        xarg.dl_threads = xarg.dl_threads or 4

    try:
        xplay.playURL(url, ref or url)
        return
    except:
        print(sys.exc_info())
        traceback.print_tb(sys.exc_info()[2])

    return

if __name__ == '__main__':
    main()
