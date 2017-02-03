#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys

import xdef
import xsrc
import vod

def main():
    if len(sys.argv) < 2:
        return
    url = xsrc.search(r'view.py\?v=(.*)', sys.argv[1]) or sys.argv[1]
    xdef.player = 'dbg'
    vod.playURL(url, None)
    return

if __name__ == '__main__':
    main()
