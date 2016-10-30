#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import re
import xdef
import vod

def testvod(url):
    print('[testvod]\n\n\t'+url)
    xdef.player = 'dbg'
    vod.playURL(url, None)

def main():
    if (len(sys.argv)) >= 2:
        url = sys.argv[1]
        m = re.search(r'view.py\?v=(.*)', url)
        if m:
            url = m.group(1)
        testvod(url)
    return

if __name__ == '__main__':
    main()
