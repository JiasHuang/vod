#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys
import xdef, vod
import json

from optparse import OptionParser

def main():

    parser = OptionParser()
    parser.add_option('-j', '--json', action='store', default=xdef.json)
    parser.add_option('-u', '--url', action='store', default='')
    (options, args) = parser.parse_args(sys.argv[1:])

    url = options.url

    if url == '':
        url = sys.argv[1]

    xdef.player = 'extractor'
    vod.playURL(url, '')

if __name__ == '__main__':
    main()
