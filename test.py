#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import sys

import xarg
import vod

def main():

    if len(sys.argv) < 2:
        return

    m = re.search(r'view.py\?v=(.*)', sys.argv[1])
    if m:
        url = m.group(1)
    else:
        url = sys.argv[1]

    xarg.player = 'dbg'
    vod.playURL(url, None)
    return

if __name__ == '__main__':
    main()
