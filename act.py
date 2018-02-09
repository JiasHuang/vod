#!/usr/bin/env python
# -*- coding: utf-8 -*-

import xarg
import xplay

from optparse import OptionParser

def main():

    act = None
    val = None

    parser = OptionParser()
    parser.add_option("-p", "--player", dest="player")
    parser.add_option("--buffering", dest="buffering", action='store_true')
    (options, args) = parser.parse_args()

    if options.player:
        xarg.player = options.player

    if options.buffering:
        xarg.buffering = True

    if len(args) >= 1:
        act = args[0]

    if len(args) >= 2:
        val = args[1]

    if act:
        xplay.setAct(act, val)

    return

if __name__ == '__main__':
    main()
