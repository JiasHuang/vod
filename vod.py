#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import re
import urllib
import sys
import traceback
import ast

import xarg
import xdef
import xplay
import xsrc
import xurl

from optparse import OptionParser

def getSettingDefs():
    local = os.path.dirname(os.path.abspath(__file__)) + '/settings.js'
    m = re.search(r'var settings = ({.*?});', xurl.readLocal(local), re.DOTALL | re.MULTILINE)
    if m:
        return ast.literal_eval(m.group(1))
    return None

def main():

    url = None
    ref = None

    defs = getSettingDefs()
    os.chdir(xdef.workdir)

    parser = OptionParser()
    parser.add_option("-p", "--player", dest="player")
    parser.add_option("-f", "--format", dest="format")
    parser.add_option("--autosub", dest="autosub")
    parser.add_option("--pagelist", dest="pagelist")
    parser.add_option("--playbackMode", dest="playbackMode")
    parser.add_option("--dl-threads", dest="dl_threads")
    parser.add_option("--dlconf", dest="dlconf")
    (options, args) = parser.parse_args()

    if options.player:
        xarg.player = options.player

    if options.pagelist:
        xarg.pagelist = options.pagelist

    if options.playbackMode:
        xarg.playbackMode = options.playbackMode

    if options.dl_threads:
        xarg.dl_threads = options.dl_threads

    xarg.ytdlfmt = options.format or defs['format']['defs']
    xarg.autosub = options.autosub or defs['autosub']['defs']
    xarg.dlconf = options.dlconf or defs['dlconf']['defs']

    if len(args) >= 1:
        url = args[0].strip()
        m = re.search(r'view.py\?(v|url)=(.*)', url)
        if m:
            url = urllib.unquote(m.group(2))

    if len(args) >= 2:
        ref = args[1].strip()

    if xarg.dlconf and not xarg.dl_threads:
        for conf in xarg.dlconf.split(','):
            try:
                c = conf.split('=')
                key = c[0]
                val = c[1]
                if re.search(re.escape(key), url):
                    xarg.dl_threads = val
            except:
                continue

    try:
        xplay.playURL(url, ref or url)
        return
    except:
        print(sys.exc_info())
        traceback.print_tb(sys.exc_info()[2])

    return

if __name__ == '__main__':
    main()
