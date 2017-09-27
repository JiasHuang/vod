#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib

import xarg
import xdef
import xplay

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
        xarg,playbackMode = options.playbackMode

    if len(args) >= 1:
        url = args[0].strip()
        m = re.search(r'view.py\?(v|url)=(.*)', url)
        if m:
            url = urllib.unquote(m.group(2))

    if len(args) >= 2:
        ref = args[1].strip()

    xplay.playURL(url, ref or url)
    return

if __name__ == '__main__':
    main()
