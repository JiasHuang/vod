#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os, sys
import xdef, xplay, vod
import json

from optparse import OptionParser

def main():

    parser = OptionParser()
    parser.add_option('-j', '--json', action='store', default=xdef.json)
    parser.add_option('-s', '--src', action='store', default='')
    parser.add_option('-r', '--ref', action='store', default='')
    parser.add_option('-u', '--url', action='store', default='')
    (options, args) = parser.parse_args(sys.argv[1:])

    src = options.src
    ref = options.ref
    url = options.url

    if src == '':
        with open(options.json, 'r') as fd:
            data = json.load(fd)
            src = data['src']
            ref = data['ref']

    if src != '':
        xplay.playURL(src, ref)
        return

    if url != '':
        vod.playURL(url, ref)
        return

if __name__ == '__main__':
    main()
