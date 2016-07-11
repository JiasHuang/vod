#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xdef
import vod

def testvod(url):
    xdef.player = 'dbg'
    vod.playURL(url, None)

if __name__ == '__main__':
    if (len(sys.argv)) >= 2:
        testvod(sys.argv[1])
